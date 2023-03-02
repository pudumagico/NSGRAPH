import yaml
import re


def parse_questions(yaml_filepath, graph_id):
    assert len(question_forms) == len(question_form_asp)
    with open(yaml_filepath, "r") as file:
        docs = yaml.load_all(file, yaml.FullLoader)
        i = 0
        questions = []
        questions_nl = []
        answers = []
        for data in docs:
            if data['graph']['id'] == graph_id:
                question_nl = data['question']['english']
                for i, regex in enumerate(question_forms):
                    match = regex.match(question_nl)
                    if match:
                        args = list(map(str.lower, list(match.groups())))
                        # args.reverse()
                        args = [x.replace(' ', '') for x in args]
                        answers.append(data['answer'])
                        asp_question = question_form_asp[i].format(*args)
                        questions.append(asp_question)
                        questions_nl.append(question_nl)
                        break

    return questions, questions_nl, answers


question_forms = [
    re.compile("How clean is ([a-zA-Z]+)\?"),
    re.compile("What is the cleanliness level of ([a-zA-Z]+) station\?"),
    re.compile("How big is ([a-zA-Z]+)\?"),
    re.compile("What size is ([a-zA-Z]+)\?"),
    re.compile("What music plays at ([a-zA-Z]+)\?"),
    re.compile("At ([a-zA-Z]+) what sort of music plays\?"),
    re.compile("What architectural style is ([a-zA-Z]+)\?"),
    re.compile("Describe ([a-zA-Z]+) station's architectural style."),
    re.compile("Does ([a-zA-Z]+) have disabled access\?"),
    re.compile("Is there disabled access at ([a-zA-Z]+)\?"),
    re.compile("Does ([a-zA-Z]+) have rail connections\?"),
    re.compile("Can you get rail connections at ([a-zA-Z]+)\?"),
    re.compile(
        "How many architectural styles does ([ a-zA-Z]+) pass through\?"),
    re.compile("How many music styles does ([ a-zA-Z]+) pass through\?"),
    re.compile("How many sizes of station does ([ a-zA-Z]+) pass through\?"),
    re.compile(
        "How many stations playing ([a-zA-Z]+) does ([ a-zA-Z]+) pass through\?"),
    re.compile(
        "How many ([a-zA-Z]+) stations does ([ a-zA-Z]+) pass through\?"),
    re.compile(
        "How many stations with disabled access does ([ a-zA-Z]+) pass through\?"),
    re.compile(
        "How many stations with rail connections does ([ a-zA-Z]+) pass through\?"),
    re.compile("How many stations are between ([a-zA-Z]+) and ([a-zA-Z]+)\?"),
    re.compile(
        "How many stations are on the shortest path between ([a-zA-Z]+) and ([a-zA-Z]+) avoiding ([a-zA-Z]+) stations\?"),
    re.compile(
        "How many other stations are two stops or closer to ([a-zA-Z]+)\?"),
    re.compile(
        "What's the nearest station to ([a-zA-Z]+) with ([a-zA-Z]+) architecture\?"),
    re.compile(
        "How many distinct routes are there between ([a-zA-Z]+) and ([a-zA-Z]+)\?"),
    re.compile("Is ([a-zA-Z]+) part of a cycle\?"),
    re.compile("Are ([a-zA-Z]+) and ([a-zA-Z]+) adjacent\?"),
    re.compile("Which station is adjacent to ([a-zA-Z]+) and ([a-zA-Z]+)\?"),
    re.compile("Which ([a-zA-Z]+) station is adjacent to ([a-zA-Z]+)\?"),
    re.compile(
        "Are ([a-zA-Z]+) and ([a-zA-Z]+) connected by the same station\?"),
    re.compile("Is there a station called ([a-zA-Z]+)\?"),
    re.compile("Is there a station called ([a-zA-Z]+)\?"),
    re.compile("Which lines is ([a-zA-Z]+) on\?"),
    re.compile("How many lines is ([a-zA-Z]+) on\?"),
    re.compile("Are ([a-zA-Z]+) and ([a-zA-Z]+) on the same line\?"),
    re.compile("Which stations does ([a-zA-Z]+) pass through\?"),
    re.compile("Which line has the most ([a-zA-Z]+) stations\?"),
]

question_form_asp = [
    'end(2).pickClean(1).station(0,{}).',
    'end(2).pickClean(1).station(0,{}).',
    'end(2).pickSize(1).station(0,{}).',
    'end(2).pickSize(1).station(0,{}).',
    'end(2).pickMusic(1).station(0,{}).',
    'end(2).pickMusic(1).station(0,{}).',
    'end(2).pickArch(1).station(0,{}).',
    'end(2).pickArch(1).station(0,{}).',
    'end(2).pickDA(1).station(0,{}).',
    'end(2).pickDA(1).station(0,{}).',
    'end(2).pickRA(1).station(0,{}).',
    'end(2).pickRA(1).station(0,{}).',
    'end(4).count(3).pluckArch(2).lineNodes(1).line(0,{}).',
    'end(4).count(3).pluckMusic(2).lineNodes(1).line(0,{}).',
    'end(4).count(3).pluckSize(2).lineNodes(1).line(0,{}).',
    'end(3).countIfEqual(2,{}).lineNodes(1).line(0,{}).',
    'end(3).countIfEqual(2,{}).lineNodes(1).line(0,{}).',
    'end(3).countIfEqual(2,da).lineNodes(1).line(0,{}).',
    'end(3).countIfEqual(2,ra).lineNodes(1).line(0,{}).',
    'end(3).countNodesBetween(2).shortestPath(1).station(0,{}).station(0,{}).',
    'end(3).countNodesBetween(2).shortestPathAvoid(1, {}).station(0,{}).station(0,{}).',
    'end(2).withinHops(1, 2).station(0,{}).',
    'end(2).closestArch(1, {}).station(0,{}).',
    'end(2).paths(1).station(0,{}).station(0,{}).',
    'end(2).cycle(1).station(0,{}).',
    'end(2).adjacent(1).station(0,{}).station(0,{}).',
    'end(2).adjacentTo(1).station(0,{}).station(0,{}).',
    'end(2).adjacentArch(1, {}).station(0,{}).',
    'end(2).commonStation(1).station(0,{}).station(0,{}).',
    'end(2).exist(1).station(0,{}).',
    'end(2).exist(1).station(0,{}).',
    'end(2).linesOn(1).station(0,{}).',
    'end(3).count(2).linesOn(1).station(0,{}).',
    'end(2).sameLine(1).station(0,{}).station(0,{}).',
    'end(2).stations(1).line(0,{}).',
    'end(2).mostArch(0,{}).',
]
