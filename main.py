import argparse
import os
import sys
import time

import easyocr
import clingo

from parse_image import parse_labels, parse_graph, gt_labels, gt_graph
from parse_question import parse_questions
from parse_background_knowledge import fill_background_knowledge, gt_data

reader = easyocr.Reader(['en'])


def main(fp, gt, ocrgt, ogrgt):
    data_filepath = fp

    USE_GT = gt
    USE_OCR_GT = ocrgt
    USE_OGR_GT = ogrgt

    yaml_file = [f for f in os.listdir(data_filepath) if f.endswith('.yaml')]
    if len(yaml_file) != 1:
        raise ValueError('should be only one yaml file in the directory')

    yaml_filename = yaml_file[0]

    png_files = [f for f in os.listdir(data_filepath) if f.endswith('.png')]

    theory = open('theory.lp', "r").read()
    total = 0
    incorrect = 0

    start = time.time()

    for graph in png_files:

        f = open('graph_encodings/{}.lp'.format(graph.strip('.png')), "w")

        if USE_GT:
            nodes, edges, lines = gt_data(os.path.abspath(
                data_filepath) + '/' + yaml_filename, str(graph).strip('.png'))
        else:
            try:
                if USE_OCR_GT:
                    name_dict = gt_labels(os.path.abspath(
                        data_filepath) + '/' + yaml_filename, str(graph).strip('.png'))

                else:
                    name_dict = parse_labels(os.path.abspath(
                        data_filepath) + '/' + graph, reader)

                if USE_OGR_GT:
                    nodes, edges = gt_graph(os.path.abspath(
                        data_filepath) + '/' + yaml_filename, str(graph).strip('.png'), name_dict)
                else:
                    nodes, edges = parse_graph(os.path.abspath(
                        data_filepath) + '/' + graph, name_dict)

                nodes, edges, lines = fill_background_knowledge(os.path.abspath(
                    data_filepath) + '/' + yaml_filename, str(graph).strip('.png'), nodes, edges)

            except:
                total += 1
                incorrect += 1
                print('EXCEPTION', graph)
                continue

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
                current_ans = [str(x).replace(' ', '').replace(
                    '-', '').lower() for x in answers[i]]
            else:
                current_ans = str(answers[i]).replace(
                    ' ', '').replace('-', '').lower()

            ans_found = False
            model_ans = []
            for model in models:
                for atom in model.symbols(shown=True):
                    if not ans_found:
                        if atom.name == 'ans':
                            model_ans.append(str(atom.arguments[0]))
                            if str(atom.arguments[0]) == current_ans:
                                ans_found = True

            model_ans.sort()
            if not ans_found and model_ans == current_ans:
                ans_found = True

            len_models = len(models)
            if not ans_found and str(len_models) == current_ans:
                ans_found = True

            if not ans_found and not models and current_ans == 'false':
                ans_found = True

            if not ans_found:
                incorrect += 1

            total += 1

        partial_end = time.time()
        print('Partial Correct Answers:', total-incorrect)
        print('Partial Total Questions:', total)
        print('Partial Accuracy:', (total-incorrect)/total * 100)
        print('Partial Time:', partial_end - start)

    end = time.time()

    print('Correct Answers:', total-incorrect)
    print('Total Questions:', total)
    print('Accuracy:', (total-incorrect)/total * 100)
    print('Time:', end - start)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-fp', '--folder_path', type=str,
                        help='Path to folder containing graph images and a single .yaml file', required=True)
    parser.add_argument('-fgt', '--full_ground_truth', type=bool,
                        help='Use full ground truth.', default=False)
    parser.add_argument('-ocrgt', '--ocr_ground_truth', type=bool,
                        help='Use OCR ground truth (labels)', default=False)
    parser.add_argument('-ogrgt', '--ogr_ground_truth', type=bool,
                        help='Use OGR ground truth (nodes and edges)', default=False)
    args = parser.parse_args()

    main(args.folder_path, args.full_ground_truth,
         args.ocr_ground_truth, args.ogr_ground_truth)
