import nntplib
import yaml
import sys
from operator import itemgetter
from pprint import pprint

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
                
                print(data['question']['english'])
                # print(data['answer'])
                
                print(data['question']['functional'])

                f_program = data['question']['functional']
                # print(f_program)
                aux = []

                for x in get_all_keys(f_program, 0):
                    aux.append(list(x))

                steps = max(aux, key=itemgetter(2))[2]

                for x in aux:
                    x[2] = steps - x[2]

                # print(aux)

                lp_program = []

                '''
                [['Count', [{'Unique': [{'Pluck': [{'Nodes': [{'Filter': [{'AllEdges': []}, 'line_id', {'Pick': [{'Line': [{'built': '90s', 'color': 'brown', 'has_aircon': True, 'id': '5d4d0bdf-2818-4a5f-86ce-2080686c9454', 'name': 'Brown Shaif', 'stroke': 'solid'}]}, 'id']}]}]}, 'architecture']}]}], 7], 
                ['Unique', [{'Pluck': [{'Nodes': [{'Filter': [{'AllEdges': []}, 'line_id', {'Pick': [{'Line': [{'built': '90s', 'color': 'brown', 'has_aircon': True, 'id': '5d4d0bdf-2818-4a5f-86ce-2080686c9454', 'name': 'Brown Shaif', 'stroke': 'solid'}]}, 'id']}]}]}, 'architecture']}], 6], 
                ['Pluck', [{'Nodes': [{'Filter': [{'AllEdges': []}, 'line_id', {'Pick': [{'Line': [{'built': '90s', 'color': 'brown', 'has_aircon': True, 'id': '5d4d0bdf-2818-4a5f-86ce-2080686c9454', 'name': 'Brown Shaif', 'stroke': 'solid'}]}, 'id']}]}]}, 'architecture'], 5], 
                ['Nodes', [{'Filter': [{'AllEdges': []}, 'line_id', {'Pick': [{'Line': [{'built': '90s', 'color': 'brown', 'has_aircon': True, 'id': '5d4d0bdf-2818-4a5f-86ce-2080686c9454', 'name': 'Brown Shaif', 'stroke': 'solid'}]}, 'id']}]}], 4], 
                ['Filter', [{'AllEdges': []}, 'line_id', {'Pick': [{'Line': [{'built': '90s', 'color': 'brown', 'has_aircon': True, 'id': '5d4d0bdf-2818-4a5f-86ce-2080686c9454', 'name': 'Brown Shaif', 'stroke': 'solid'}]}, 'id']}], 3], 
                ['AllEdges', [], 2], 
                ['Pick', [{'Line': [{'built': '90s', 'color': 'brown', 'has_aircon': True, 'id': '5d4d0bdf-2818-4a5f-86ce-2080686c9454', 'name': 'Brown Shaif', 'stroke': 'solid'}]}, 'id'], 2], 
                ['Line', [{'built': '90s', 'color': 'brown', 'has_aircon': True, 'id': '5d4d0bdf-2818-4a5f-86ce-2080686c9454', 'name': 'Brown Shaif', 'stroke': 'solid'}], 1], 
                ['built', '90s', 0], ['color', 'brown', 0], ['has_aircon', True, 0], ['id', '5d4d0bdf-2818-4a5f-86ce-2080686c9454', 0], ['name', 'Brown Shaif', 0], ['stroke', 'solid', 0]]
                '''
                # pprint(aux)
                lp_program.append("end({}).".format(aux[0][2]))           

                for step in aux:
                    if step[0] == 'Pick':
                        lp_program.append("pick_{}({},{}).".format(
                            step[1][1], step[2], step[2] - 1))
                    elif step[0] == 'Station':
                        lp_program.append("station({},{},{}).".format(
                            step[2], step[2] - 1, step[1][0]['name'].lower()))
                    elif step[0] == 'Line':
                        lp_program.append("line({},{},{}).".format(
                            step[2], step[2] - 1, step[1][0]['name'].replace(" ", "").lower()))
                    elif step[0] == 'AllEdges':
                        lp_program.append("allEdges({},{}).".format(
                            step[2], step[2] - 1))
                    elif step[0] == 'Filter':
                        # last_val = None
                        # if isinstance(step[1][-1], dict):
                        #     last_val = list(step[1][-1].values())[0][0]
                        # else:
                        #     last_val = step[1][-1]
                        lp_program.append("filter_{}({},{}).".format(
                            step[1][1], step[2], step[2] - 1))
                    elif step[0] == 'Nodes':
                        lp_program.append("nodes({},{}).".format(
                            step[2], step[2] - 1))
                    elif step[0] == 'Edges':
                        lp_program.append("edges({},{}).".format(
                            step[2], step[2] - 1))
                    elif step[0] == 'Pluck':
                        lp_program.append("pluck_{}({},{}).".format(
                            step[1][1], step[2], step[2] - 1))
                    elif step[0] == 'Unique':
                        lp_program.append("unique({},{}).".format(
                            step[2], step[2] - 1))
                    elif step[0] == 'Count':
                        lp_program.append("count({},{}).".format(
                            step[2], step[2] - 1))   
                    elif step[0] == 'CountIfEqual':
                        last_val = None
                        if isinstance(step[1][1], dict):
                            last_val = list(step[1][-1].values())[0][0]
                        else:
                            last_val = step[1][-1]

                        lp_program.append("countIfEqual({}, {}, {}).".format(
                            step[2], step[2] - 1, str(last_val).replace("-", "").replace(" ", "").lower()))    

                    elif step[0] == 'ShortestPathOnlyUsing':
                        lp_program.append("shortestPathOnlyUsing{}({}, {}, {}).".format(
                            step[1][2]['Without'][1], step[2], step[2] - 1, list(step[1][2]['Without'][2].values())[0][0].replace('-', '')))                           
                    elif step[0] == 'WithinHops':
                        lp_program.append("withinHops({},{}, {}).".format(
                            step[2], step[2] - 1, step[1][1]))   
                    elif step[0] == 'Paths':
                        lp_program.append("paths({},{}).".format(
                            step[2], step[2] - 1))   
                    elif step[0] == 'HasCycle':
                        lp_program.append("hasCycle({},{}).".format(
                            step[2], step[2] - 1))  
                    elif step[0] == 'ShortestPath':
                        lp_program.append("shortestPath({},{}).".format(
                            step[2], step[2] - 1))  
                    elif step[0] == 'Equal':
                        lp_program.append("equal({},{}, {}).".format(
                            step[2], step[2] - 1, step[1][1]))             
                    elif step[0] == 'HasIntersection':
                        lp_program.append("HasIntersection({},{}).".format(
                            step[2], step[2] - 1))     
                    elif step[0] == 'Mode':
                        lp_program.append("Mode({},{}).".format(
                            step[2], step[2] - 1))  


                #still many things to do
                    
                # if i == 33:
                #     break
                # i += 1
                # print(lp_program)
                questions.append(''.join(lp_program))
                questions_nl.append(data['question']['english'])
                answers.append(data['answer'])

    return questions, questions_nl, answers

            # break 
                # while isinstance(f_program, dict):
                #     keys = f_program.keys()
                #     for key in keys:

                # if f_program.keys()[0] == 'Pick':
                #     lp_program.append(('pick', f_program['Pick'][1]))
                # elif f_program.keys()[0] == 'Station':
                #     lp_program.append(f_program['Station'])
                # f_program = f_program

            # print(x['question']['english'])
            # print(x['question']['functional'])
            # print(x['answer'])

actions = {
    "Station": "station({T},{T1}, {name})",
    "Line": "station({T},{T1}, {name})",
    "Edge": "station({T},{T1}, {name})",
    "Pick": "pick_{}({T},{T1})",
    "AllEdges": "",
    "AllNodes": "",
    "Filter": "",
    "Nodes": "",
    "Pluck": "",
    "Count": "",
    "CountIfEqual": "",
    "ShortestPath": "",
    "Paths": "",
    "HasCycle": "",
}


def encode_question(program):
    pass


actions = {
    "scene": "scene({T},{T1}).",
    "unique": "unique({T},{T1}).",
    "relate": "relate_{val}({T},{T1}).",
    "count": "count({T},{T1}).",
    "exist": "exist({T},{T1}).",
    "filter_size": "filter_{val}({T},{T1}).",
    "filter_color": "filter_{val}({T},{T1}).",
    "filter_material": "filter_{val}({T},{T1}).",
    "filter_shape": "filter_{val}({T},{T1}).",
    "query_size": "query_size({T},{T1}).",
    "query_color": "query_color({T},{T1}).",
    "query_material": "query_material({T},{T1}).",
    "query_shape": "query_shape({T},{T1}).",
    "same_size": "same_size({T},{T1}).",
    "same_color": "same_color({T},{T1}).",
    "same_material": "same_material({T},{T1}).",
    "same_shape": "same_shape({T},{T1}).",
    "equal_integer": "equal_integer({T},{T1},{T2}).",
    "less_than": "less_than({T},{T1},{T2}).",
    "greater_than": "greater_than({T},{T1},{T2}).",
    "equal_size": "equal_size({T},{T1},{T2}).",
    "equal_color": "equal_color({T},{T1},{T2}).",
    "equal_material": "equal_material({T},{T1},{T2}).",
    "equal_shape": "equal_shape({T},{T1},{T2}).",
    "union": "or({T},{T1},{T2}).",
    "intersect": "and({T},{T1},{T2})."
}

func_type = {
    "unary": ["scene", "unique", "count", "exist", "query_size", "query_color", "query_material",
              "query_shape", "same_size", "same_color", "same_material", "same_shape"],
    "binary_val": ["relate", "filter_size", "filter_color", "filter_material", "filter_shape"],
    "binary_in": ["equal_integer", "less_than", "greater_than", "equal_size", "equal_color", "equal_shape",
                  "equal_material", "union", "intersect"]
}


def encode_question(program):
    # Holds action sequence
    action_atoms = []
    # Time
    t = 0

    # Iterate over functional program and translate every basic function into an action atom
    for i, func in enumerate(program):
        t = i
        func_name = func["function"]
        if func_name in func_type["unary"]:
            if func_name == "scene":
                action_atoms.append(actions[func_name].format(T=t, T1=0))
            else:
                action_atoms.append(actions[func_name].format(
                    T=t, T1=func["inputs"][0] + 1))
        elif func_name in func_type["binary_val"]:
            val = func["value_inputs"][0]
            action_atoms.append(actions[func_name].format(
                T=t, T1=func["inputs"][0] + 1, val=val))
        elif func_name in func_type["binary_in"]:
            t1 = func["inputs"][0]
            t2 = func["inputs"][1]
            if func_name in ["union", "intersect"]:
                action_atoms.append(actions[func_name].format(
                    T=t, T1=t1 + 1, T2=t2 + 1))
            else:
                action_atoms.append(
                    actions[func_name].format(T=t, T1=t1, T2=t2))
        else:
            print("Unknown function name: " + func_name)

    # Add end atom
    action_atoms.append(f"end({t}).")

    # Return action sequence as string
    return "\n".join(action_atoms)