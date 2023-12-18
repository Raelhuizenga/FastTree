from node import Node
from profile_creation import form_profile
from neighbor_joining import top_hits


def fast_tree(sequences_dict):
    sequence_list = list(sequences_dict.values())
    n = len(sequence_list)
    total_profile = form_profile(sequence_list)
    total_up_distance = 0
    total_nodes = {}
    for label, seq in sequences_dict.items():
        total_nodes[label] = Node(0, form_profile([seq]), [], 0, label, [])
    top_hits(total_nodes, n)
    return total_nodes


def parse_input():
    data = open('../data/test-small.txt', 'r').read().split(">")
    sequence_dictionary = {}
    for seq in data[1::]:
        label, DNA = seq.splitlines()
        sequence_dictionary[label] = DNA
    return sequence_dictionary


if __name__ == '__main__':
    sequence_dict = parse_input()
    n = fast_tree(sequence_dict)
    for key, node in n.items():
        print(node.get_label())
        print(node.get_top_hits())
