from node import Node
from profile_creation import form_profile
from neighbor_joining import top_hits, best_hits, get_best_hit, create_join


def fast_tree(sequences_dict):
    """
    Constructs a tree from the sequences in sequences_dict using the FastTree algorithm.
    :param sequences_dict: dictionary with as key the label name and as value the sequence
    :type sequences_dict: dict(str, str)
    :return: evolutionary tree constructed from the sequences in Newick format
    """
    sequence_list = list(sequences_dict.values())
    n = len(sequence_list)
    total_profile = form_profile(sequence_list)
    total_up_distance = 0
    total_nodes = {}
    for label, seq in sequences_dict.items():
        total_nodes[label] = Node(0, form_profile([seq]), [], 0, label, [], True, None)
    top_hits(total_nodes, n)
    best_hits_list = best_hits(total_nodes)
    best_hit = get_best_hit(best_hits_list, total_nodes)
    create_join(best_hit, total_nodes)
    # while active nodes < n-3:
    #   join nodes
    return total_nodes


def parse_input():
    """
    Reads a text file with aligned sequences and puts the sequences in a dictionary.
    :return: dictionary with as key the label name and as value the sequence
    """
    data = open('../data/test-small.txt', 'r').read().split(">")
    sequence_dictionary = {}
    for seq in data[1::]:
        label, DNA = seq.splitlines()
        sequence_dictionary[label] = DNA
    return sequence_dictionary


if __name__ == '__main__':
    sequence_dict = parse_input()
    n = fast_tree(sequence_dict)
    print(n)
    # for key, node in n.items():
    #     print(node.get_label())
    #     print(node.get_top_hits())
