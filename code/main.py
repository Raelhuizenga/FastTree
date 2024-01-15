from node import Node
from profile_creation import form_profile
from neighbor_joining import top_hits, best_hits, get_best_hit, create_join, create_final_joins
from get_active_nodes import get_active_nodes, give_active_node
from newick_format import newick_format


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
    for i in range(n-3):
        best_hits_list = best_hits(total_nodes)
        best_hit = get_best_hit(best_hits_list, total_nodes)
        best_hit_active = (give_active_node(best_hit[0], total_nodes), give_active_node(best_hit[1], total_nodes))
        create_join(best_hit_active, total_nodes)
    final_join = best_hits(total_nodes)[0]
    create_final_joins(final_join[0], final_join[1], total_nodes)
    final_nodes = list(get_active_nodes(total_nodes).keys())
    create_final_joins(final_nodes[0], final_nodes[1], total_nodes)
    print(get_active_nodes(total_nodes))
    # sometimes there are multiple active nodes left :(
    # so i just print them all but we need to fix this
    # TODO: why are there multiple active nodes left?
    for tree in list(get_active_nodes(total_nodes).keys()):
        print(newick_format(tree, total_nodes))
    # print(newick_format(list(get_active_nodes(total_nodes).keys())[0], total_nodes))
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
    # for key, node in n.items():
    #     print(node.get_label())
    #     print(node.get_top_hits())
