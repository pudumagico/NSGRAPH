import argparse
import os
import sys

import clingo

import easyocr

from parse_background_knowledge import fill_background_knowledge
from parse_image import parse_graph
from parse_question import parse_questions
# node_pred = f'node({architecture},{cleanliness},{disabled_access},{has_rail},{music},{name},{size})'
# edge_pred = f'edge({line_color}, {line_name}, {station1_name}, {station2_name})'

reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory


def main():
    data_filepath = sys.argv[1]

    yaml_file = [f for f in os.listdir(data_filepath) if f.endswith('.yaml')]
    if len(yaml_file) != 1:
        raise ValueError('should be only one yaml file in the directory')

    yaml_filename = yaml_file[0]

    png_files = [f for f in os.listdir(data_filepath) if f.endswith('.png')]

    main_encoding_file = open('main_encoding.lp', "r")
    main_encoding =  main_encoding_file.read()
    for graph in png_files:
        
        f = open(f'graph_encodings/{graph}.lp', "w")

        nodes, edges = parse_graph(os.path.abspath(data_filepath) + '/' + graph, reader)
        nodes, edges, lines = fill_background_knowledge(os.path.abspath(data_filepath) + '/' + yaml_filename, str(graph).strip('.png'), nodes, edges)
        print(nodes)
        print(edges)
        f.write(nodes)
        f.write(edges)
        f.write(lines)

        questions, questions_nl, answers = parse_questions(os.path.abspath(data_filepath) + '/' + yaml_filename, str(graph).strip('.png'))

        accuracy = 0
        total = len(questions)
        for i in range(len(questions)):
            ctl = clingo.Control(message_limit=0)

            print(i,questions_nl[i])
            print(i,questions[i])
            print(i,answers[i])

            ctl.add("base", [], nodes+edges+lines+questions[i])
            ctl.add("base", [], main_encoding)
            ctl.ground([("base", [])])
            # model = None
            with ctl.solve(yield_=True) as handle:
                for m in handle: 
                    print(m)
            
            # for atom in m.symbols(shown=True):
            #     print(atom)
                # if str(atom).split('(')[1].strip(')') == str(answers[i]).lower():
                #     print('OK')
                # else:
                #     print(atom)
                #     exit()

        f.close()

if __name__ == "__main__":
    main()