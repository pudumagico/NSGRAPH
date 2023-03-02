import os
import sys

import easyocr
import clingo

from parse_image import parse_graph
from parse_question import parse_questions
from parse_background_knowledge import fill_background_knowledge, gt_data

reader = easyocr.Reader(['en'])

USE_GT = True

def main():
    data_filepath = sys.argv[1]

    yaml_file = [f for f in os.listdir(data_filepath) if f.endswith('.yaml')]
    if len(yaml_file) != 1:
        raise ValueError('should be only one yaml file in the directory')

    yaml_filename = yaml_file[0]

    png_files = [f for f in os.listdir(data_filepath) if f.endswith('.png')]

    theory = open('theory.lp', "r").read()
    for graph in png_files:

        f = open('graph_encodings/{}.lp'.format(graph.strip('.png')), "w")

        nodes, edges = parse_graph(os.path.abspath(
            data_filepath) + '/' + graph, reader)
        if USE_GT:

            nodes, edges, lines = gt_data(os.path.abspath(
                data_filepath) + '/' + yaml_filename, str(graph).strip('.png'), nodes, edges)
        else:
            nodes, edges, lines = fill_background_knowledge(os.path.abspath(
                data_filepath) + '/' + yaml_filename, str(graph).strip('.png'), nodes, edges)

        f.write(nodes)
        f.write(edges)
        f.write(lines)

        questions, questions_nl, answers = parse_questions(os.path.abspath(
            data_filepath) + '/' + yaml_filename, str(graph).strip('.png'))

        total = len(questions)
        correct = 0
        for i in range(len(questions)):
            ctl = clingo.Control(["--warn=none", "-n 0"])

            # print(i, questions_nl[i])
            # print(i, questions[i])
            # print(i, answers[i])

            ctl.add("base", [], nodes+edges+lines+questions[i])
            ctl.add("base", [], theory)
            ctl.ground([("base", [])])
            models = []
            with ctl.solve(yield_=True) as handle:
                for m in handle:
                    models.append(m)

            ans_found = False

            for model in models:
                if not ans_found:
                    for atom in model.symbols(shown=True):
                        if str(atom.arguments[0]) == str(answers[i]).lower():
                            correct += 1
                            ans_found = True
                            break    
        f.close()
    print('Accuracy:', correct/total * 100)

if __name__ == "__main__":
    main()
