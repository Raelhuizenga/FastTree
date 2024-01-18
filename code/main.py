from node import Node
from profile_creation import form_profile
from neighbor_joining import top_hits, best_hits, get_best_hit, create_join
from get_active_nodes import get_active_nodes, give_active_node
from newick_format import newick_format
from nearest_neighbor_interchanges import run_nearest_neighbor_interchanges


def fast_tree(sequences_dict):
    """
    Constructs a tree from the sequences in sequences_dict using the FastTree algorithm.
    :param sequences_dict: dictionary with as key the label name and as value the sequence
    :type sequences_dict: dict(str, str)
    :return: evolutionary tree constructed from the sequences in Newick format
    """
    sequence_list = list(sequences_dict.values())
    n = len(sequence_list)
    # @ToDo do we ever need total_profile and total_up_distance?
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
    final_join = (give_active_node(final_join[0], total_nodes), give_active_node(final_join[1], total_nodes))
    create_join(final_join, total_nodes, False)
    final_nodes = list(get_active_nodes(total_nodes).keys())
    create_join(final_nodes, total_nodes, False)
    # @ToDo Nearest Neighbor Interchanges
    tree = list(get_active_nodes(total_nodes).keys())
    if len(tree) > 1:
        raise ValueError('tree not finished')
    # @ToDo branch lengths are sometimes negative and zero for all leaves
    run_nearest_neighbor_interchanges(n, total_nodes[tree[0]])
    return newick_format(total_nodes[tree[0]], total_nodes[tree[0]])


def parse_input(filename):
    """
    Reads a text file with aligned sequences and puts the sequences in a dictionary.
    :return: dictionary with as key the label name and as value the sequence
    """
    data = open('../data/'+filename+'.txt', 'r').read().split(">")
    sequence_dictionary = {}
    for seq in data[1::]:
        label, DNA = seq.splitlines()
        sequence_dictionary[label] = DNA
    return sequence_dictionary


if __name__ == '__main__':
    filename = 'test-small'
    sequence_dict = parse_input(filename)
    tree = fast_tree(sequence_dict)
    print(tree)
    # for key, node in n.items():
    #     print(node.get_label())
    #     print(node.get_top_hits())
