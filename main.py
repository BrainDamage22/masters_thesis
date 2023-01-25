from data_creation import create_data
from util import read_data, calculate_n_sets
from routing import dynamic_ng_pathing
from util import read_data, calculate_n_sets, save_ng_result, save_dng_results
from routing import dynamic_ng_pathing, ng_routing_recursion, ng_routing_iteration
from computational_experiment import test_delta1_for_ng_routing, test_delta1_and_delta2_for_dng_pathing

path = '/Users/lukas/Documents/Master Thesis/'

# Data Creation Parameters
amount = 8
range_x = 20
range_y = 20

# Hyper Parameters
starting_node = 0
delta1 = 4
delta2 = 5

# Testing Parameters:
iterations_ng = 10
iterations_dng = 2

create_data(amount, range_x, range_y, path)
costs_list, nodes = read_data(path)
node_objects = calculate_n_sets(costs_list, nodes, delta1)

to_visit = list(range(0, len(nodes)))
to_visit.remove(starting_node)

# dynamic_ng_pathing(starting_node, node_objects.copy(), to_visit.copy(), [], len(nodes), delta2, costs_list, path)
# dng-pathing
# dng_result, results = dynamic_ng_pathing(starting_node, node_objects.copy(), to_visit.copy(), [], len(nodes), delta2, costs_list)
# save_dng_results(path, results)

# ng-routing
save_ng_result(path + "recursion/", ng_routing_recursion(starting_node, node_objects.copy(), costs_list))
save_ng_result(path + "iteration/", ng_routing_iteration(starting_node, node_objects.copy(), costs_list))
print()

# test delta1 for ng-routing
# test_delta1_for_ng_routing(path, amount, range_x, range_y, starting_node, iterations_ng)

# test delta1 and delta2 for dng-pathing
# test_delta1_and_delta2_for_dng_pathing(path, amount, range_x, range_y, starting_node, iterations_dng)
