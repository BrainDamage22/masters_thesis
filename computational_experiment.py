from data_creation import create_data
from util import read_data, calculate_n_sets, save_ng_test_results, save_dng_test_results
from routing import dynamic_ng_pathing, ng_routing_recursion, ng_routing_iteration
from classes import NgMode


def test_delta1_for_ng_routing(path, amount, range_x, range_y, starting_node, iterations, mode):
    for i in range(0, iterations):
        create_data(amount, range_x, range_y, path + "temp/")
        costs_list, nodes = read_data(path + "temp/")

        to_visit = list(range(0, len(nodes)))
        to_visit.remove(starting_node)

        results = []

        for delta1 in range(1, len(nodes) + 1):
            node_objects = calculate_n_sets(costs_list, nodes, delta1)
            if mode == NgMode.recursion:
                result = ng_routing_recursion(starting_node, node_objects.copy(), costs_list)
                results.append(result)
            else:
                result = ng_routing_iteration(starting_node, node_objects.copy(), costs_list)
                results.append(result)

        save_ng_test_results(path, results, str(i + 1).zfill(3))
        print("Iteration " + str(i+1) + " done")


def test_delta1_and_delta2_for_dng_pathing(path, amount, range_x, range_y, starting_node, iterations, mode):
    for i in range(0, iterations):
        create_data(amount, range_x, range_y, path + "temp/")
        costs_list, nodes = read_data(path + "temp/")

        to_visit = list(range(0, len(nodes)))
        to_visit.remove(starting_node)

        results = []

        for delta1 in range(1, len(nodes) + 1):
            for delta2 in range(1, len(nodes) + 1):
                if delta2 < delta1:
                    continue
                else:
                    node_objects = calculate_n_sets(costs_list, nodes, delta1)
                    result, dng_results = dynamic_ng_pathing(starting_node, node_objects.copy(), costs_list, delta2, mode)
                    results.append(result)

        save_dng_test_results(path, results, str(i + 1).zfill(3))
