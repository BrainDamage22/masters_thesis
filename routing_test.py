from util import find_loops
from classes import NgResult
import time


def ng_routing_test(starting_node, nodes, costs_list, upper_bound):
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

        neighbours = frozenset(nodes[current_node].neighbors)
        ng_set_j = frozenset.intersection(ng_set_i, neighbours)
        ng_set_j = frozenset().union(ng_set_j, frozenset([current_node]))
        k += 1

        if k > n:
            continue

        to_visit = all_nodes - ng_set_j
        for new_curr_node in to_visit:
            new_cost = round((prev_cost + ((n-k+2) * costs_list[current_node][new_curr_node])), 3)

            # found_dominating_state = False
            # for key in all_dp_routes.keys():
            #     cost, _, _ = all_dp_routes[key]
            #     if cost < new_cost and key[2] == k and ng_set_j.issubset(key[1]):
            #         found_dominating_state = True
            #         break
            #
            # if found_dominating_state:
            #     continue
            if new_cost > upper_bound:
                continue
            elif (new_curr_node, ng_set_j, k) not in all_dp_routes:
                all_dp_routes[(new_curr_node, ng_set_j, k)] = (new_cost, current_node, ng_set_i)
                queue += [(new_curr_node, ng_set_j, k)]
            elif new_cost < all_dp_routes[(new_curr_node, ng_set_j, k)][0]:
                all_dp_routes[(new_curr_node, ng_set_j, k)] = (new_cost, current_node, ng_set_i)

    full_path_buffer = dict((k, v) for k, v in all_dp_routes.items() if k[2] == n)

    for key in full_path_buffer.keys():
        cost, prev_node, ng_set_i = all_dp_routes[key]
        new_cost = round(cost + costs_list[key[0]][starting_node], 3)
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



