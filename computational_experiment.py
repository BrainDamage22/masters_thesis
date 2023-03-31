from data_creation import create_data
from util import read_data, calculate_n_sets, save_ng_test_results, save_dng_test_results, calculate_route_costs_dmp
from routing import dynamic_ng_pathing, ng_routing, ng_routing_depr
from nearest_neighbor import find_nearest_neighbours_path


# This function tests the performance of routing algorithms by generating random data,
# calculating the upper bound using the nearest neighbor heuristic, and testing the
# routing algorithms with different delta1 values. It then saves the results and prints the progress.
def test_delta1_for_ng_routing(path, amount, range_x, range_y, starting_node, iterations, clean):
    # Run the test for the specified number of iterations
    for i in range(0, iterations):
        create_data(amount, range_x, range_y, path + "temp/")
        costs_list, nodes = read_data(path + "temp/")

        nn_route = find_nearest_neighbours_path(nodes.copy(), costs_list)
        upper_bound = calculate_route_costs_dmp(nn_route, costs_list)

        to_visit = list(range(0, len(nodes)))
        to_visit.remove(starting_node)

        results = []

        # Test routing algorithms with different delta1 values
        for delta1 in range(2, len(nodes) + 1):
            node_objects = calculate_n_sets(costs_list, nodes, delta1)

            # Run the appropriate routing algorithm based on the clean parameter
            if clean:
                result = ng_routing_depr(starting_node, node_objects.copy(), costs_list)
            else:
                result = ng_routing(starting_node, node_objects.copy(), costs_list, upper_bound)

            results.append(result)

        save_ng_test_results(path, results, str(i + 1).zfill(3))
        print("Iteration " + str(i + 1) + " done")


# This function tests the performance of dynamic routing algorithms by generating random data,
# calculating the upper bound using the nearest neighbor heuristic, and testing the routing
# algorithms with different combinations of delta1 and delta2 values. It then saves the results.
def test_delta1_and_delta2_for_dng_pathing(path, amount, range_x, range_y, starting_node, iterations):
    # Run the test for the specified number of iterations
    for i in range(0, iterations):
        create_data(amount, range_x, range_y, path + "temp/")
        costs_list, nodes = read_data(path + "temp/")

        nn_route = find_nearest_neighbours_path(nodes.copy(), costs_list, starting_node)
        upper_bound = calculate_route_costs_dmp(nn_route, costs_list)

        to_visit = list(range(0, len(nodes)))
        to_visit.remove(starting_node)

        results = []

        # Test routing algorithms with different combinations of delta1 and delta2 values
        for delta1 in range(2, len(nodes) + 1):
            for delta2 in range(2, len(nodes) + 1):
                if delta2 < delta1:
                    continue
                else:
                    node_objects = calculate_n_sets(costs_list, nodes, delta1)
                    result, dng_results = dynamic_ng_pathing(starting_node, node_objects.copy(), costs_list, delta2, upper_bound)
                    results.append(result)

        save_dng_test_results(path, results, str(i + 1).zfill(3))

