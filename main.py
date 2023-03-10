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
    total = 0
    incorrect = 0

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
        f.close()

        questions, questions_nl, answers = parse_questions(os.path.abspath(
            data_filepath) + '/' + yaml_filename, str(graph).strip('.png'))

        for i in range(len(questions)):
            ctl = clingo.Control(["--warn=none", "--opt-strategy=usc", "-n 0"])

            ctl.add("base", [], nodes+edges+lines+questions[i])
            ctl.add("base", [], theory)
            ctl.ground([("base", [])])
            models = []
            with ctl.solve(yield_=True) as handle:
                for m in handle:
                    # print(m)
                    models.append(m)
           
            if type(answers[i]) == list:
                answers[i].sort()
                current_ans = [str(x).replace(' ', '').replace('-', '').lower() for x in answers[i]]
            else:
                current_ans = str(answers[i]).replace(' ', '').replace('-', '').lower()

            ans_found = False
            model_ans = []
            for model in models:
                # print(model.symbols(shown=True))
                    for atom in model.symbols(shown=True):
                        if not ans_found:
                            if atom.name == 'ans':
                                model_ans.append(str(atom.arguments[0]))
                                if str(atom.arguments[0]) == current_ans:
                                # correct += 1
                                    ans_found = True
                                    # break
                                
            model_ans.sort()
            if not ans_found and model_ans == current_ans:
                # correct += 1
                ans_found = True

            len_models = len(models)
            if not ans_found and str(len_models) == current_ans:
                # correct += 1
                ans_found = True

            if not ans_found and not models and current_ans == 'false':
                # correct += 1
                ans_found = True

            if not ans_found:
                print(i, questions_nl[i])
                print(i, questions[i])
                print(i, str(answers[i]), current_ans)
                for m in models:
                    print(m.symbols(shown=True))
                incorrect += 1

            total+=1

        # print('Partial Total Questions:', total )
        # print('Partial Correct Answers:', total-incorrect)
        # print('Partial Accuracy:', (total-incorrect)/total * 100)

    print('Total Questions:', total )
    print('Correct Answers:', total-incorrect)
    print('Accuracy:', (total-incorrect)/total * 100)


if __name__ == "__main__":
    main()
