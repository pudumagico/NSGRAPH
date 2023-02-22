import yaml
import re

def get_all_keys(d, i):
    for key, value in d.items():
        yield key, value, i
        if isinstance(value, list):
            for element in value:
                if isinstance(element, dict):
                    yield from get_all_keys(element, i + 1)
        else:
            if isinstance(value, dict):
                yield from get_all_keys(value, i + 1)

def parse_questions(yaml_filepath, graph_id):

    with open(yaml_filepath, "r") as file:
        docs = yaml.load_all(file, yaml.FullLoader)
        i = 0
        questions = []
        questions_nl = []
        answers = []
        for data in docs:
            if data['graph']['id'] == graph_id:
                question_nl = data['question']['english']
                questions_nl.append(questions_nl)
                answers.append(data['answer'])
                # f_program = data['question']['functional']
                
                for i, regex in enumerate(question_forms):
                    match = regex.match(question_nl)
                    if match:
                        args = list(match.groups())
                        asp_question = question_form_asp[i].format(*args)
                        print(asp_question)
                        questions.append(asp_question)
                        break
                        
                
                

    return questions, questions_nl, answers


question_forms = [

	# --------------------------------------------------------------------------
	# Station properties
	# --------------------------------------------------------------------------
		re.compile("How clean is ([a-zA-Z]+)\?"), 
		# (lambda s: Pick(s, "cleanliness")),
		# "StationPropertyCleanliness"),
		re.compile("What is the cleanliness level of ([a-zA-Z]+) station\?"), 
		# (lambda s: Pick(s, "cleanliness")),
		# "StationPropertyCleanliness2"),
		re.compile("How big is ([a-zA-Z]+)\?"), 
		# (lambda s: Pick(s, "size")),
		# "StationPropertySize"),
		re.compile("What size is ([a-zA-Z]+)\?"), 
		# (lambda s: Pick(s, "size")),
		# "StationPropertySize2"),
		re.compile("What music plays at ([a-zA-Z]+)\?"), 
		# (lambda s: Pick(s, "music")),
		# "StationPropertyMusic"),
		re.compile("At ([a-zA-Z]+) what sort of music plays\?"), 
		# (lambda s: Pick(s, "music")),
		# "StationPropertyMusic2"),
		re.compile("What architectural style is ([a-zA-Z]+)\?"), 
		# (lambda s: Pick(s, "architecture")),
		# "StationPropertyArchitecture"),
		re.compile("Describe ([a-zA-Z]+) station's architectural style."), 
		# (lambda s: Pick(s, "architecture")),
		# "StationPropertyArchitecture2"),
		re.compile("Does ([a-zA-Z]+) have disabled access\?"), 
		re.compile("Is there disabled access at ([a-zA-Z]+)\?"), 
		# (lambda s: Pick(s, "disabled_access")),
		# "StationPropertyDisabledAccess2"),
		re.compile("Does ([a-zA-Z]+) have rail connections\?"), 
		# (lambda s: Pick(s, "has_rail")),
		# "StationPropertyHasRail"),
		re.compile("Can you get rail connections at ([a-zA-Z]+)\?"), 
		# (lambda s: Pick(s, "has_rail")),
		# "StationPropertyHasRail2"),

	# ------------------------------------------------------------e--------------
	# Line questions
	# --------------------------------------------------------------------------
	
		re.compile("How many architectural styles does ([a-zA-Z]+) pass through\?"), 
		# (lambda l: Count(Unique(Pluck(Nodes(Filter(AllEdges(), "line_id", Pick(l, "id"))),
		# 						  "architecture"))) ),
		# "LineTotalArchitectureCount"),
		re.compile("How many music styles does ([a-zA-Z]+) pass through\?"), 
		# (lambda l: Count(Unique(Pluck(Nodes(Filter(AllEdges(), "line_id", Pick(l, "id"))),
		# 						  "music"))) ),
		# "LineTotalMusicCount"),
		re.compile("How many sizes of station does ([a-zA-Z]+) pass through\?"), 
		# (lambda l: Count(Unique(Pluck(Nodes(Filter(AllEdges(), "line_id", Pick(l, "id"))),
								#   "size"))) ),
		re.compile("How many stations playing ([a-zA-Z]+) does ([a-zA-Z]+) pass through\?"), 
		# lambda v, l: CountIfEqual(
		# 	Pluck(
		# 		Nodes(Filter(AllEdges(), "line_id", Pick(l, "id"))),
		# 		"music"
		# 	),
		# 	v
		# ),
		# "LineFilterMusicCount"),
		re.compile("How many ([a-zA-Z]+) stations does ([a-zA-Z]+) pass through\?"), 
		# lambda v, l: CountIfEqual(
		# 	Pluck(
		# 		Nodes(Filter(AllEdges(), "line_id", Pick(l, "id"))),
		# 		"size"
		# 	),
		# 	v
		# ),
		# "LineFilterSizeCount"),
		re.compile("How many stations with disabled access does ([a-zA-Z]+) pass through\?"), 
		# lambda l: CountIfEqual(
		# 	Pluck(
		# 		Nodes(Filter(AllEdges(), "line_id", Pick(l, "id"))),
		# 		"disabled_access"
		# 	),
		# 	True
		# ),
		# "LineFilterDisabledAccessCount"),
		re.compile("How many stations with rail connections does ([a-zA-Z]+) pass through\?"), 
		# lambda l: CountIfEqual(
		# 	Pluck(
		# 		Nodes(Filter(AllEdges(), "line_id", Pick(l, "id"))),
		# 		"has_rail"
		# 	),
		# 	True
		# ),
		# "LineFilterHasRailCount"),

	
	# --------------------------------------------------------------------------
	# MultiStep graph algorithms question set
	# --------------------------------------------------------------------------
		re.compile("How many stations are between ([a-zA-Z]+) and ([a-zA-Z]+)\?"), 
		# (lambda n1,n2: CountNodesBetween(ShortestPath(n1, n2, []))),
		# "StationShortestCount",
		# arguments_valid=lambda g, n1, n2: n1 != n2,
		# answer_valid=lambda g, a, n1, n2: a >= 0,
		# group="MultiStep"),
		re.compile("How many stations are on the shortest path between ([a-zA-Z]+) and ([a-zA-Z]+) avoiding ([a-zA-Z]+) stations\?"), 
		# (lambda n1, n2 ,c: CountNodesBetween(ShortestPathOnlyUsing(n1, n2, Without(AllNodes(), "cleanliness", c), []))),
		# "StationShortestAvoidingCount",
		# arguments_valid=lambda g, n1, n2, c: n1 != n2,
		# answer_valid=lambda g, a, n1, n2, c: a >= 0,
		# group="MultiStep"),
	# 'two hops away'
		re.compile("How many other stations are two stops or closer to ([a-zA-Z]+)\?"), 
		# (lambda a: Count(WithinHops(a, 2))),
		# "StationTwoHops",
		# group="MultiStep"),


		re.compile("What's the nearest station to ([a-zA-Z]+) with ([a-zA-Z]+) architecture\?"),
		# lambda x, a: Pick(MinBy(
		# 	FilterHasPathTo(Filter(AllNodes(), "architecture", a), x), 
		# 	lambda y: Count(ShortestPath(x, y, []))
		# ), "name"),
		# "NearestStationArchitecture",
		# group="MultiStep"),

		re.compile("How many distinct routes are there between ([a-zA-Z]+) and ([a-zA-Z]+)\?"),
		# lambda n1, n2: Count(Paths(n1, n2)),
		# "DistinctRoutes",
		# arguments_valid=lambda g, n1, n2: n1 != n2,
		# group="MultiStep"),


		re.compile("Is ([a-zA-Z]+) part of a cycle\?"),
		# lambda n1: HasCycle(n1),
		# "HasCycle",
		# group="MultiStep"),


		re.compile("Are ([a-zA-Z]+) and ([a-zA-Z]+) adjacent\?"), 
		# (lambda a,b: Adjacent(a,b)),
		# "StationAdjacent"),
		re.compile("Which station is adjacent to ([a-zA-Z]+) and ([a-zA-Z]+)\?"), 
		# lambda a,b: UnpackUnitList(Pluck(Sample(Intersection(Neighbors(a), Neighbors(b)), 1), "name")),
		# "StationPairAdjacent",
		# arguments_valid=lambda g, a, b: a != b,
		# answer_valid=lambda g, a, b, c: a != b and a != c),
		re.compile("Which ([a-zA-Z]+) station is adjacent to ([a-zA-Z]+)\?"), 
		# lambda a,b: UnpackUnitList(Pluck(Filter(Neighbors(b), "architecture", a), "name")),
		# "StationArchitectureAdjacent"),
		re.compile("Are ([a-zA-Z]+) and ([a-zA-Z]+) connected by the same station\?"), 
		# (lambda a,b: Equal(Count(ShortestPath(a, b, [])),3)),
		# "StationOneApart"),
		re.compile("Is there a station called ([a-zA-Z]+)\?"), 
		# (lambda a: Const(True)),
		# "StationExistence1"),
		re.compile("Is there a station called ([a-zA-Z]+)\?"), 
		# (lambda a: Const(False)),
		# "StationExistence2"),
		re.compile("Which lines is ([a-zA-Z]+) on\?"), 
		# (lambda a: GetLines(a)),
		# "StationLine"),
		re.compile("How many lines is ([a-zA-Z]+) on\?"), 
		# (lambda a: Count(GetLines(a))),
		# "StationLineCount"),
		re.compile("Are ([a-zA-Z]+) and ([a-zA-Z]+) on the same line\?"), 
		# (lambda a, b: HasIntersection(GetLines(a), GetLines(b)) ),
		# "StationSameLine",
		# arguments_valid=lambda g, a, b: a != b),
		re.compile("Which stations does ([a-zA-Z]+) pass through\?"), 
		# (lambda a: Pluck(Unique(Nodes(Filter(AllEdges(), "line_id", Pick(a, "id")))), "name")),
		# "LineStations"),
		re.compile("Which line has the most ([a-zA-Z]+) stations\?"),
		# (lambda a: Mode(Pluck(Edges(Filter(AllNodes(), "architecture", a)), "line_name")) ),
		# "LineMostArchitecture"),


]

question_form_asp = [
    # Stations
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
    
    # Lines
    
    'end(4).count(3).pluckArch(2).lineNodes(1).line(0,{}).',
    'end(4).count(3).pluckMusic(2).lineNodes(1).line(0,{}).',
    'end(4).count(3).pluckSize(2).lineNodes(1).line(0,{}).',
    
    'end(3).countIfEqual(2,{}).lineNodes(1).line(0,{}).',
    'end(3).countIfEqual(2,{}).lineNodes(1).line(0,{}).',
    
    'end(3).countIfEqual(2,da).lineNodes(1).line(0,{}).',
    'end(3).countIfEqual(2,ra).lineNodes(1).line(0,{}).',

    # Interesting
    'end(3).countNodesBetween(2).shortestPath(1).station(0,{}).station(0,{}).',
    'end(3).countNodesBetween(2).shortestPathAvoid(1, {}).station(0,{}).station(0,{}).',
    
    'end(3).countNodesBetween(2).withinHops(1, 2).station(0,{})',

    'end(3).countNodesBetween(2).closestArch(1, {}).station(0,{})',

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
