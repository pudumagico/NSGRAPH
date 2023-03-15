import sys

import easyocr
import cv2 as cv
from scipy.spatial import distance

from optical_graph_recognition.preprocessing import preprocess
from optical_graph_recognition.argsparser import parser, parse_argument
from optical_graph_recognition.segmentation import segment
from optical_graph_recognition.topology_recognition import recognize_topology
from optical_graph_recognition.postprocessing import postprocess


def find_closest_name(node, name_dict):
    selected_name = None
    for name in name_dict:
        if selected_name is None:
            selected_name = name
        else:
            if distance.euclidean([node[0], node[1]], name_dict[name]) < distance.euclidean([node[0], node[1]], name_dict[selected_name]):
                selected_name = name
    del name_dict[selected_name]
    return selected_name


def parse_graph(file_path, reader):

    names = reader.readtext(file_path)
    # print(names, len(names))
    total = 0
    # for n in names:
    #     if n[2] > 0.5:
    #         print(n)
    #         total+=1
    # print(total)
    name_dict = {}

    source = cv.imread(file_path)
    mode = 1

    for name in names:
        x_center = (name[0][0][0] + name[0][1][0])/2
        y_center = (name[0][0][1] + name[0][2][1])/2
        name_dict[name[1]] = [x_center, y_center]

        source[round(name[0][0][1]): round(name[0][2][1]), round(
            name[0][0][0]): round(name[0][1][0])] = [255, 255, 255]

    source, preprocessed, mode, is_rotated = preprocess(source, mode)



    vertices_list, visualised, preprocessed, edge_thickness = segment(
        source, preprocessed, mode)
    
    # cv.imshow('', visualised)
    # cv.waitKey(0)

    vertices_list = recognize_topology(
        vertices_list, preprocessed, visualised, edge_thickness, mode)
    
    # print(len(vertices_list))
    # exit()
    graph = postprocess(vertices_list, is_rotated)

    nodes = []
    edges = []
    for element in graph:
        node = [element.x, element.y, element.color]
        nodes.append(node)
        edges.append(element.adjacency_list)

    for node in nodes:
        name = find_closest_name(node, name_dict)
        node.append(name)
    return nodes, edges


if __name__ == "__main__":
    reader = easyocr.Reader(['en'])
    nodes, edges = parse_graph(sys.argv[1], reader)
    for n in nodes:
        print(n)
    print(len(nodes))
    for e in edges:
        print(e)