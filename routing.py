from util import find_loops, calculate_route_costs, print_exceeded
from classes import DngResult, NgResult, NgMode
import time


def ng_routing(starting_node, nodes, costs_list, lower_bound):
    start = time.time()

    def retrace_optimal_path(buffer):

        full_path_buffer = dict((k, v) for k, v in buffer.items() if k[2] == n)
        path_key = min(full_path_buffer.keys(), key=lambda x: full_path_buffer[x][0])
        curr_node = path_key[0]
        optimal_cost, prev_node, ng_set_i = buffer[path_key]

        optimal_path = [curr_node, starting_node]
        k = n

        while prev_node is not None:
            curr_node = prev_node
            k -= 1
            path_key = (curr_node, ng_set_i, k)
            _, prev_node, ng_set_i = buffer[path_key]

            optimal_path = [curr_node] + optimal_path
        return optimal_path, optimal_cost

    all_dp_routes = {}
    node_objects = {node.number: node for node in nodes}
    n = len(node_objects)
    all_nodes = frozenset(list(node_objects.keys()))
    all_nodes = frozenset(all_nodes) - frozenset([starting_node])
    ng_set_i = frozenset()
    k = 1
    state = (starting_node, ng_set_i, k)
    all_dp_routes[state] = (0, None, frozenset())
    queue = [state]

    while queue:
        current_node, ng_set_i, k = queue.pop(0)
        prev_cost, _, _ = all_dp_routes[(current_node, ng_set_i, k)]
        node_object = nodes[current_node]

        neighbours = frozenset(node_object.neighbors)
        ng_set_j = frozenset.intersection(ng_set_i, neighbours)
        ng_set_j = frozenset().union(ng_set_j, frozenset([current_node]))
        k += 1

        to_visit = all_nodes - ng_set_j
        for new_curr_node in to_visit:
            new_cost = round((prev_cost + costs_list[current_node][new_curr_node]), 3)

            if new_cost > lower_bound:
                continue
            elif (new_curr_node, ng_set_j, k) not in all_dp_routes:
                all_dp_routes[(new_curr_node, ng_set_j, k)] = (new_cost, current_node, ng_set_i)
                queue += [(new_curr_node, ng_set_j, k)]
            elif new_cost < all_dp_routes[(new_curr_node, ng_set_j, k)][0]:
                all_dp_routes[(new_curr_node, ng_set_j, k)] = (new_cost, current_node, ng_set_i)

    full_path_buffer = dict((k, v) for k, v in all_dp_routes.items() if k[2] == n)

    for key in full_path_buffer.keys():
        cost, prev_node, ng_set_i = all_dp_routes[key]
        new_cost = cost + round((costs_list[key[0]][starting_node]), 3)
        all_dp_routes[key] = (new_cost, prev_node, ng_set_i)

    optimal_path, optimal_cost = retrace_optimal_path(all_dp_routes)

    loops = find_loops(optimal_path)
    possibilities = len(all_dp_routes)

    elementary = False
    if len(loops) == 0:
        elementary = True

    end = time.time()
    return NgResult(optimal_path, round(optimal_cost, 3), elementary, len(node_objects[0].neighbors), 0,
                    round(end - start, 3), possibilities)


def dynamic_ng_pathing(starting_node, nodeObjects, costs_list, delta2, lower_bound):
    start = time.time()
    i = 0

    results = []
    start_delta1 = len(nodeObjects[0].neighbors)
    max_delta1 = 0
    possibilities = 0

    while True:
        i += 1

        result = ng_routing(starting_node, nodeObjects, costs_list, lower_bound)

        possibilities += result.ng_iterations
        cost = result.cost
        best_route = result.best_route
        loops = find_loops(best_route)

        for node in nodeObjects:
            if len(node.neighbors) > max_delta1:
                max_delta1 = len(node.neighbors)

        if len(loops) == 0:
            print("")
            print("Best Route in iteration: " + str(i))
            print(best_route)
            print("Costs :", str(cost))
            end = time.time()
            result = DngResult(best_route, cost, loops, result.cardinality, start_delta1, max_delta1, delta2, False,
                               True, i, round(end - start, 3), possibilities)
            results.append(result)
            return result, results

        print("")
        print(str(i) + ". Iteration")
        print(best_route)
        print("Costs :", str(cost))
        print("Sub Routes:")
        print(loops)
        end = time.time()
        result = DngResult(best_route, cost, loops, result.cardinality, start_delta1, max_delta1, delta2, False, False,
                           i, round(end - start, 3), possibilities)
        results.append(result)

        loop_with_smallest_cardinality = min(loops, key=len)
        start_and_ending_node = loop_with_smallest_cardinality[0]
        loop_with_smallest_cardinality = loop_with_smallest_cardinality[1:-1]

        if len(loop_with_smallest_cardinality) >= delta2:
            print_exceeded(best_route, cost)
            end = time.time()
            result = DngResult(best_route, cost, loops, result.cardinality, start_delta1, max_delta1, delta2, True,
                               False, i, round(end - start, 3), possibilities)
            return result, results

        for node in nodeObjects:
            for route_node in loop_with_smallest_cardinality:
                if node.number == route_node and start_and_ending_node not in node.neighbors:
                    if len(node.neighbors) < delta2:
                        node.neighbors.append(start_and_ending_node)
                    else:
                        print_exceeded(best_route, cost)
                        end = time.time()
                        result = DngResult(best_route, cost, loops, result.cardinality, start_delta1, max_delta1,
                                           delta2, True, False, i, round(end - start, 3), possibilities)
                        return result, results
