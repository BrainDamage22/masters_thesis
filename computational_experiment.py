from data_creation import create_data
from util import read_data, calculate_n_sets, save_ng_test_results, save_dng_test_results
from routing import dynamic_ng_pathing, ng_routing
import time


def test_delta1_for_ng_routing(path, amount, range_x, range_y, starting_node, iterations):
    save_path = path + "results/ng-test-results-" + time.strftime("%d%m%Y-%H%M%S")
    for i in range(0, iterations):
        create_data(amount, range_x, range_y, path)
        costs_list, nodes = read_data(path)

        to_visit = list(range(0, len(nodes)))
        to_visit.remove(starting_node)

        results = []

        for delta1 in range(1, len(nodes) + 1):
            node_objects = calculate_n_sets(costs_list, nodes, delta1)
            result = ng_routing(starting_node, node_objects.copy(), to_visit.copy(), [], len(nodes), costs_list)
            results.append(result)
            print("Done for Delta1 = " + str(delta1))

        save_ng_test_results(save_path, results, str(i + 1).zfill(3))


def test_delta1_and_delta2_for_dng_pathing(path, amount, range_x, range_y, starting_node, iterations):
    save_path = path + "results/dng-test-result-" + time.strftime("%d%m%Y-%H%M%S")
    for i in range(0, iterations):
        create_data(amount, range_x, range_y, path)
        costs_list, nodes = read_data(path)

        to_visit = list(range(0, len(nodes)))
        to_visit.remove(starting_node)

        results = []

        for delta1 in range(1, len(nodes) + 1):
            for delta2 in range(1, len(nodes) + 1):
                if delta2 < delta1:
                    continue
                else:
                    node_objects = calculate_n_sets(costs_list, nodes, delta1)
                    result, dng_results = dynamic_ng_pathing(starting_node, node_objects.copy(), to_visit.copy(), [], len(nodes), delta2, costs_list)
                    results.append(result)

        save_dng_test_results(save_path, results, str(i + 1).zfill(3))
