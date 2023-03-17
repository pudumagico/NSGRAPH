import yaml
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
    return selected_name


def parse_graph(file_path, name_dict):

    source = cv.imread(file_path)
    mode = 1

    source, preprocessed, mode, is_rotated = preprocess(source, mode)
    vertices_list, visualised, preprocessed, edge_thickness = segment(
        source, preprocessed, mode)
    vertices_list = recognize_topology(
        vertices_list, preprocessed, visualised, edge_thickness, mode)
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


def parse_labels(file_path, reader):

    names = reader.readtext(file_path)
    name_dict = {}
    for name in names:
        x_center = (name[0][0][0] + name[0][1][0])/2
        y_center = (name[0][0][1] + name[0][2][1])/2
        name_dict[name[1]] = [x_center, y_center]

    return name_dict

def gt_labels(file_path, graph_id, map_radius = 4):
    stream = open(file_path, "r")
    all_info = yaml.load_all(stream, yaml.FullLoader)
    incumbent_info = None
    for info in all_info:
        if info['graph']['id'] == str(graph_id):
            incumbent_info = info
            break
    
    gt_labels_dict = {}

    for bkg_info_node in incumbent_info['graph']['nodes']:
        x = (bkg_info_node['x'] + map_radius) * 1000/(map_radius*2)
        y = 1000 - (bkg_info_node['y'] + map_radius) * 1000/(map_radius*2)
        gt_labels_dict[bkg_info_node['name']] = [x,y]

    return gt_labels_dict

def gt_graph(file_path, graph_id, name_dict, map_radius = 50):
    stream = open(file_path, "r")
    all_info = yaml.load_all(stream, yaml.FullLoader)
    incumbent_info = None
    for info in all_info:
        if info['graph']['id'] == str(graph_id):
            incumbent_info = info
            break

    nodes = []
    edges = []

    node_index = 0
    node_index_dict = {}
    for bkg_info_node in incumbent_info['graph']['nodes']:
        node_index_dict[bkg_info_node['name']] = node_index
        # node_index.append([bkg_info_node['name'], node_index])
        node_index += 1
    
    for bkg_info_node in incumbent_info['graph']['nodes']:
        x = (bkg_info_node['x'] + map_radius) * 1000/(map_radius*2)
        y = 1000 - (bkg_info_node['y'] + map_radius) * 1000/(map_radius*2)
        
        adjacency_list = []
        for bkg_info_edge in incumbent_info['graph']['edges']:
            if bkg_info_node['name'] == bkg_info_edge['station1_name']:
                adjacency_list.append(node_index_dict[bkg_info_edge['station2_name']])
            elif bkg_info_node['name'] == bkg_info_edge['station2_name']:
                adjacency_list.append(node_index_dict[bkg_info_edge['station1_name']])

        node = [x, y, 0]
        nodes.append(node)
        edges.append(list(set(adjacency_list)))

    for node in nodes:
        name = find_closest_name(node, name_dict)
        node.append(name)

    return nodes, edges

