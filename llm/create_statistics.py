import os
import csv
import re
import json
from typing import Iterator
from itertools import chain, tee
from more_itertools import pairwise

FULL_MATCH = "full_match"
CONTAINS_SOLUTION = "contains_solution"
WRONG_CLASSIFICATION = "wrong_classification"
CONTAINS_PREDICATES = "contains_predicates"
TASK_MISSED = "task_missed"
NO_ANSWER = "no_answer"

CLASSES = [FULL_MATCH, CONTAINS_SOLUTION, WRONG_CLASSIFICATION, CONTAINS_PREDICATES, TASK_MISSED, NO_ANSWER]
MODELS = ["GPT 3.5", "GPT 4", "GPT4ALL", "Vicuna 13b", "Bard"]
MODELS += [m + "_survey" for m in MODELS]
ALL_SOLUTIONS = [
    "end(3).countNodesBetween(2).shortestPath(1).station(0,{}).station(0,{}).",
    "end(2).withinHops(1, 2).station(0,{}).",
    "end(2).paths(1).station(0,{}).station(0,{}).",
    "end(2).cycle(1).station(0,{}).",
    "end(2).adjacent(1).station(0,{}).station(0,{}).",
    "end(2).adjacentTo(1).station(0,{}).station(0,{}).",
    "end(2).commonStation(1).station(0,{}).station(0,{}).",
    "end(2).exist(1).station(0,{}).",
    "end(2).linesOnNames(1).station(0,{}).",
    "end(2).linesOnCount(1).station(0,{}).",
    "end(2).sameLine(1).station(0,{}).station(0,{}).",
    "end(2).stations(1).line(0,{})."
]
LOGS_PATH = "../logs"
stats_path = "../stats"


def all_files() -> Iterator[str]:
    return [f for f in os.listdir(LOGS_PATH) if f.endswith(".csv")]


def latest_files() -> Iterator[str]:
    files = os.listdir(LOGS_PATH)
    for model in MODELS:
        model_files = [{"version": int(file[len(model):-4]), "file": file} for file in files if file.startswith(model) and file[len(model):-4].isnumeric()]
        if not model_files:
            print(f"Skipping {model} as no csv was found")
            continue
        yield max(model_files, key=lambda x: x['version'])['file']


def delete_latest():
    if not os.path.exists(stats_path): return
    for f in os.listdir(stats_path):
        os.remove(os.path.join(stats_path, f))


def string_to_regex(input: str) -> str:
    return input.replace(".", "\\. *").replace("(", "\\(").replace(")", "\\)")


def summarize_file(filename: str):
    with open(os.path.join(LOGS_PATH, filename)) as file:
        class_count = {kw: [0, 0, 0] for kw in CLASSES}  # easy, medium, hard
        print(filename)
        try:
            (*_, (_, last_el)), iterrows = tee(pairwise(csv.reader(file, delimiter=";")))  # two iterators, one for the last element
        except ValueError:
            print(f"{filename} is empty")
            return
        _, (model_name, *_) = next(iterrows)  # get the name of the model and skip head
        all_lines = chain(iterrows, [(last_el[0], None)]) if last_el[0].count(';') == 5 else iterrows  # bugfixing
        for (*_, difficulty, solution, response), next_row in all_lines:
            difficulty, solution, response = int(difficulty), string_to_regex(solution.strip()), response.strip()

            while next_row == [] or next_row and next_row[0] != model_name:  # Append lines that aren't a new entry
                try: current_row, next_row = next(iterrows)
                except StopIteration: current_row, next_row = next_row, None
                response += current_row[0].strip() if len(current_row) >= 1 else ""

            full_match_pattern = re.compile("^"+solution.replace("{}", "[A-Za-z0-9\\\" ]+")+"$")
            contains_solution_pattern = re.compile(solution.replace("{}", "[A-Za-z0-9\\\" ]+"))
            wrong_classification_patterns = [re.compile(string_to_regex(cs).replace("{}", "[A-Za-z0-9\\\" ]+")) for cs in ALL_SOLUTIONS]
            contains_predicates_pattern = re.compile("([A-Za-z]*\([\"A-Za-z0-9 ]+\)\.)+")
            if response.strip() == "":
                class_count[NO_ANSWER][difficulty] += 1
            elif full_match_pattern.search(response):
                class_count[FULL_MATCH][difficulty] += 1
            elif contains_solution_pattern.search(response):
                class_count[CONTAINS_SOLUTION][difficulty] += 1
            elif any(pattern.search(response) for pattern in wrong_classification_patterns):
                class_count[WRONG_CLASSIFICATION][difficulty] += 1
            elif contains_predicates_pattern.search(response):
                class_count[CONTAINS_PREDICATES][difficulty] += 1
            else: class_count[TASK_MISSED][difficulty] += 1
        if not os.path.exists(stats_path): os.makedirs(stats_path)
        with open(os.path.join(stats_path, filename[:-4] + "_statistics.json"), "w+") as sf:
            json.dump({k: {"easy": e, "medium": m, "hard": h} for k, (e, m, h) in class_count.items()}, sf, indent=4)


def create_collective_summary():
    DATA_SOURCE = os.path.join("..", "stats", "latest")
    DATA_DEST = os.path.join("..", "stats", "collection")
    if not os.path.exists(DATA_SOURCE): print(f"Data source at {DATA_SOURCE} does not exist")
    if not os.path.exists(DATA_DEST): os.makedirs(DATA_DEST)
    fileindex = 1
    while os.path.exists(os.path.join(DATA_DEST, "summary" + str(fileindex) + ".csv")): fileindex += 1
    with open(os.path.join(DATA_DEST, "summary" + str(fileindex) + ".csv"), "w+") as wf:
        wf.write("model;dataset;" + ';'.join(CLASSES) + ";" + ';'.join([cl+'_'+dif for cl in CLASSES for dif in ["easy", "medium", "hard"]])+";total_answers\n")
        for file in os.listdir(DATA_SOURCE):
            survey = "survey" in file
            model = [x for x in MODELS if x in file and "survey" not in x][0]
            with open(os.path.join(DATA_SOURCE, file)) as df:
                content = json.load(df)
                collected_classes = [str(sum(content[cl].values())) for cl in CLASSES]
                detailed_classes = [str(content[cl][dif]) for cl in CLASSES for dif in ["easy", "medium", "hard"]]
                total_answers = str(sum(map(int,collected_classes)))
                wf.write(';'.join([model, "human" if survey else "standard", *collected_classes, *detailed_classes, total_answers])+"\n")
    print("Collected stats successfully")


def run(summarize_all_files: bool = False):
    global stats_path
    if not summarize_all_files:
        stats_path = os.path.join(stats_path, "latest")
        delete_latest()
    func = all_files if summarize_all_files else latest_files
    for file in func():
        summarize_file(file)
    create_collective_summary()


if __name__ == "__main__":
    run(summarize_all_files=False)
