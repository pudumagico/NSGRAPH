import yaml
import cv2 as cv
import webcolors
import numpy as np
from scipy.spatial import distance


from optical_graph_recognition.preprocessing import preprocess
from optical_graph_recognition.argsparser import parser, parse_argument
from optical_graph_recognition.segmentation import segment
from optical_graph_recognition.topology_recognition import recognize_topology
from optical_graph_recognition.postprocessing import postprocess

# "color": ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'olive', 'cyan'],

colors_rgb = {
    'blue': (78, 121, 167),
    'orange': (242, 142, 43),
    'green': (89, 161, 79),
    'red': (225, 87, 89),
    'purple': (176, 122, 161),
    'brown': (156, 117, 95),
    'pink': (255, 157, 167),
    'olive': (237, 201, 72),
    'cyan': (118, 183, 178),
}

rgb_colors = {v: k for k, v in colors_rgb.items()}

def closest_color(colors,color):
    colors = np.array(colors)
    color = np.array(color)
    distances = np.sqrt(np.sum((colors-color)**2,axis=1))
    index_of_smallest = np.where(distances==np.amin(distances))
    smallest_distance = colors[index_of_smallest]
    return smallest_distance 



def find_closest_name(node, name_dict):
    selected_name = None
    for name in name_dict:
        if selected_name is None:
            selected_name = name
        else:
            if distance.euclidean([node[0], node[1]], name_dict[name]) < distance.euclidean([node[0], node[1]], name_dict[selected_name]):
                selected_name = name
    if selected_name:
        del name_dict[selected_name]
        
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
        color = closest_color(colors=list(rgb_colors.keys()), color= element.color[::-1])
        # print(tuple(color[0]))
        color = rgb_colors[tuple(color[0])]
        # print(color)
        # print(element.__dict__)
        # actual_name, closest_name = get_colour_name(element.color[::-1])
        # print("Actual colour name:", actual_name, ", closest colour name:", closest_name)
        node = [element.x, element.y, color]
        nodes.append(node)
        edges.append(element.adjacency_list)

    print(len(graph))

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
    print(name_dict, len(name_dict))
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


def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name
 

