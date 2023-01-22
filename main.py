from data_creation import create_data
from util import read_data, calculate_n_sets
from routing import dynamic_ng_pathing

path = '/Users/lukas/Documents/Master Thesis/'
starting_node = 0
delta1 = 5
delta2 = 7

create_data(8, 20, 20, path)
costs_list, nodes = read_data(path)
node_objects = calculate_n_sets(costs_list, nodes, delta1)

to_visit = list(range(0, len(nodes)))
to_visit.remove(starting_node)

dynamic_ng_pathing(starting_node, node_objects.copy(), to_visit.copy(), [], len(nodes), delta2, costs_list)
