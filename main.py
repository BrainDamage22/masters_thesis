from data_creation import create_data
from util import read_data, calculate_n_sets
from routing import dynamic_ng_pathing

path = '/Users/lukas/Documents/Master Thesis/'

# Data Creation Parameters
amount = 8
range_x = 20
range_y = 20

# Hyper Parameters
starting_node = 0
delta1 = 4
delta2 = 5

create_data(amount, range_x, range_y, path)
costs_list, nodes = read_data(path)
node_objects = calculate_n_sets(costs_list, nodes, delta1)

to_visit = list(range(0, len(nodes)))
to_visit.remove(starting_node)

dynamic_ng_pathing(starting_node, node_objects.copy(), to_visit.copy(), [], len(nodes), delta2, costs_list, path)
