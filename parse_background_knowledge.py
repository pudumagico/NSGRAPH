from platform import architecture
import sys
import yaml
import re

from difflib import SequenceMatcher

node_pred_template = 'node({architecture},{cleanliness},{disabled_access},{has_rail},{music},{name},{size}).\n'
edge_pred_template = 'edge({line_color},{line_id},{line_name},{station1},{station2}).\n'
line_pred_template = 'line({built},{color},{has_aircon},{id},{name}).\n'


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def fill_background_knowledge(file_path, graph_id, nodes, edges):

    node_preds = []
    edge_preds = []
    line_preds = []

    stream = open(file_path, "r")
    all_info = yaml.load_all(stream, yaml.FullLoader)
    incumbent_info = None
    for info in all_info:
        if info['graph']['id'] == str(graph_id):
            incumbent_info = info
            break

    for node in nodes:
        max_similarity = 0
        correspondent_info = None
        for bkg_info_node in incumbent_info['graph']['nodes']:
            similarity = similar(node[-1], bkg_info_node['name'])
            if max_similarity < similarity:
                max_similarity = similarity
                correspondent_info = bkg_info_node

        node_pred = node_pred_template.format(
            architecture=correspondent_info['architecture'].replace("-", ""),
            cleanliness=correspondent_info['cleanliness'].replace("-", ""),
            disabled_access=str(correspondent_info['disabled_access']).lower(),
            has_rail=str(correspondent_info['has_rail']).lower(),
            music=correspondent_info['music'].replace(" ", ""),
            name=correspondent_info['name'].lower(),
            size=correspondent_info['size'].replace("-", "")
        )
        node_preds.append(node_pred)

    for idx in range(len(edges)):
        for connection in edges[idx]:
            for bkg_info_edge in incumbent_info['graph']['edges']:

                if (node_preds[idx].split(',')[-2] == bkg_info_edge['station1_name'].lower() or node_preds[idx].split(',')[-2] == bkg_info_edge['station2_name'].lower()) and\
                        (node_preds[connection].split(',')[-2] == bkg_info_edge['station1_name'].lower() or node_preds[connection].split(',')[-2] == bkg_info_edge['station2_name'].lower()):

                    edge_pred = edge_pred_template.format(
                        line_color=bkg_info_edge['line_color'],
                        line_id='id'+bkg_info_edge['line_id'].replace("-", ""),
                        line_name=bkg_info_edge['line_name'].replace(
                            " ", "").lower(),
                        station1=bkg_info_edge['station1_name'].lower(),
                        station2=bkg_info_edge['station2_name'].lower(),
                    )

                    edge_preds.append(edge_pred)

    edge_preds = list(set(edge_preds))

    for line in incumbent_info['graph']['lines']:
        line_pred = line_pred_template.format(
            built=int(line['built'].replace(
                's', '').replace('recent', '2010')),
            color=line['color'],
            has_aircon=str(line['has_aircon']).lower(),
            id='id'+line['id'].replace("-", ""),
            name=line['name'].replace(" ", "").lower()
        )
        line_preds.append(line_pred)

    return ''.join(node_preds), ''.join(edge_preds), ''.join(line_preds)


def gt_data(file_path, graph_id):

    node_preds = []
    edge_preds = []
    line_preds = []

    stream = open(file_path, "r")
    all_info = yaml.load_all(stream, yaml.FullLoader)
    incumbent_info = None
    for info in all_info:
        if info['graph']['id'] == str(graph_id):
            incumbent_info = info
            break

    for bkg_info_node in incumbent_info['graph']['nodes']:

        node_pred = node_pred_template.format(
            architecture=bkg_info_node['architecture'].replace("-", ""),
            cleanliness=bkg_info_node['cleanliness'].replace("-", ""),
            disabled_access=str(bkg_info_node['disabled_access']).lower(),
            has_rail=str(bkg_info_node['has_rail']).lower(),
            music=bkg_info_node['music'].replace(" ", ""),
            name=bkg_info_node['name'].lower(),
            size=bkg_info_node['size'].replace("-", "")
        )
        node_preds.append(node_pred)

    for bkg_info_edge in incumbent_info['graph']['edges']:
        edge_pred = edge_pred_template.format(
            line_color=bkg_info_edge['line_color'],
            line_id='id'+bkg_info_edge['line_id'].replace("-", ""),
            line_name=bkg_info_edge['line_name'].replace(" ", "").lower(),
            station1=bkg_info_edge['station1_name'].lower(),
            station2=bkg_info_edge['station2_name'].lower(),
        )
        edge_preds.append(edge_pred)

    edge_preds = list(set(edge_preds))

    for line in incumbent_info['graph']['lines']:
        line_pred = line_pred_template.format(
            built=int(line['built'].replace(
                's', '').replace('recent', '2010')),
            color=line['color'],
            has_aircon=str(line['has_aircon']).lower(),
            id='id'+line['id'].replace("-", ""),
            name=line['name'].replace(" ", "").lower()
        )
        line_preds.append(line_pred)

    return ''.join(node_preds), ''.join(edge_preds), ''.join(line_preds)


vqa_node_pred_template = 'node({name},{color}).\n'
vqa_edge_pred_template = 'edge({station1},{station2},{color}).\n'
vqa_line_pred_template = 'line({color}).\n'


def aspify(nodes, edges):
    asp_nodes = ''

    for node in nodes:
        name = re.sub('\W+','', node[3]).lower()
        asp_node = vqa_node_pred_template.format(
            name=name, color=node[2])
        asp_nodes += asp_node

    asp_edges = ''
    asp_lines = ''
    for i, node_edges in enumerate(edges):
        station = nodes[i][3]
        color = nodes[i][2]
        for edge in node_edges:
            s1 = re.sub('\W+','', station).lower()
            s2 = re.sub('\W+','', nodes[edge][3]).lower()

            asp_edge = vqa_edge_pred_template.format(
                station1=s1, station2=s2, color=color)
            asp_edges += asp_edge

        asp_line = vqa_line_pred_template.format(color=color)
        asp_lines += asp_line

    return asp_nodes, asp_edges, asp_lines
