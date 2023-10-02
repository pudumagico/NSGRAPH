# CSV to Python

import csv
import json
import os

OUTPUT_FILENAME = "graph_related_question_dataset_answers"
QUESTION_INDEXES = [8 + 2 * i for i in range(12)]
ANSWER_FORMATS = [
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

question_answers = []

with open("Graph_Related_Question_Dataset_Answers.csv", encoding="utf-8") as f:
    question_answers = [{"solution": solution, "questions": []} for i, solution in enumerate(ANSWER_FORMATS)]
    iterrows = iter(csv.reader(f, delimiter=",", quotechar="\""))
    next(iterrows)
    for row in iterrows:
        for i, question in enumerate([row[ri] for ri in QUESTION_INDEXES]):
            question_answers[i]["questions"].append(question.strip())

    fileindex = 1
    while os.path.exists(OUTPUT_FILENAME + str(fileindex) + ".json"): fileindex += 1
    with open(OUTPUT_FILENAME + str(fileindex) + ".json", "w") as wf:
        json.dump(question_answers, wf, indent=4, ensure_ascii=False)
