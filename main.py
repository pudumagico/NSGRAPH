import os
import sys

import easyocr
import clingo

from parse_image import parse_graph
from parse_question import parse_questions
from parse_background_knowledge import fill_background_knowledge

reader = easyocr.Reader(['en']) 

def main():
    data_filepath = sys.argv[1]

    yaml_file = [f for f in os.listdir(data_filepath) if f.endswith('.yaml')]
    if len(yaml_file) != 1:
        raise ValueError('should be only one yaml file in the directory')

    yaml_filename = yaml_file[0]

    png_files = [f for f in os.listdir(data_filepath) if f.endswith('.png')]

    theory = open('theory.lp', "r").read()
    for graph in png_files:
        
        f = open(f'graph_encodings/{graph}.lp', "w")

        nodes, edges = parse_graph(os.path.abspath(data_filepath) + '/' + graph, reader)
        nodes, edges, lines = fill_background_knowledge(os.path.abspath(data_filepath) + '/' + yaml_filename, str(graph).strip('.png'), nodes, edges)
        f.write(nodes)
        f.write(edges)
        f.write(lines)

        questions, questions_nl, answers = parse_questions(os.path.abspath(data_filepath) + '/' + yaml_filename, str(graph).strip('.png'))

        accuracy = 0
        total = len(questions)
        for i in range(len(questions)):
            ctl = clingo.Control(["--warn=none"])

            print(i,questions_nl[i])
            print(i,questions[i])
            print(i,answers[i])

            ctl.add("base", [], nodes+edges+lines+questions[i])
            ctl.add("base", [], theory)
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