from node import Node
from profile_creation import form_profile
from neighbor_joining import top_hits, best_hits, get_best_hit, create_join
from get_active_nodes import get_active_nodes, give_active_node
from newick_format import newick_format
from nearest_neighbor_interchanges import run_nearest_neighbor_interchanges


def fast_tree(sequences_dict: dict):
    """
    Constructs a tree from the sequences in sequences_dict using the FastTree algorithm.
    :param sequences_dict: dictionary with as key the label name and as value the sequence
    :type sequences_dict: dict(str, str)
    :return: evolutionary tree constructed from the sequences in Newick format
    """
    # Create initial topology
    sequence_list = list(sequences_dict.values())
    n = len(sequence_list)
    total_nodes = {}
    for label, seq in sequences_dict.items():
        # Initialize dictionary with all nodes
        total_nodes[label] = Node(0, form_profile([seq]), [], 0, label, [], True, None, 0, None)
    top_hits(total_nodes, n)
    # join n - 3 nodes
    for i in range(n-3):
        best_hits_list = best_hits(total_nodes)
        best_hit = get_best_hit(best_hits_list, total_nodes)
        best_hit_active = (give_active_node(best_hit[0], total_nodes), give_active_node(best_hit[1], total_nodes))
        create_join(best_hit_active, total_nodes)
    # Create the finals joins
    final_join = best_hits(total_nodes)[0]
    final_join = (give_active_node(final_join[0], total_nodes), give_active_node(final_join[1], total_nodes))
    create_join(final_join, total_nodes, False)
    final_nodes = list(get_active_nodes(total_nodes).keys())
    create_join(final_nodes, total_nodes, False)
    tree = list(get_active_nodes(total_nodes).keys())
    if len(tree) > 1:
        raise ValueError('tree not finished')
    # Interchange nearest neighbors
    run_nearest_neighbor_interchanges(n, total_nodes[tree[0]])
    # @ToDo branch lengths are sometimes negative
    return newick_format(total_nodes[tree[0]], total_nodes[tree[0]])


def parse_input(filename: str):
    """
    Reads an aln file with aligned sequences and puts the sequences in a dictionary.
    :return: dictionary with as key the label name and as value the sequence
    """
    data = open('../data/'+filename+'.aln', 'r').read().split(">")
    sequence_dictionary = {}
    for seq in data[1::]:
        label, DNA = seq.splitlines()
        sequence_dictionary[label] = DNA
    return sequence_dictionary


if __name__ == '__main__':
    input_option = input("For which file do you want to run fast tree? \n1: test small 2: fasttree input \n")
    if input_option == '1':
        file = 'test-small'
    elif input_option == '2':
        file = 'fasttree-input'
    else:
        raise ValueError("Please enter a valid input (1 or 2)")
    sequence_dict = parse_input(file)
    output_tree = fast_tree(sequence_dict)
    print(output_tree)
