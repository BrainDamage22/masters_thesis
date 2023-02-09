from util import find_loops, calculate_route_costs, print_exceeded
from classes import DngResult, NgResult, NgMode
import time


def ng_routing_recursion(starting_node, nodeObjects, costs_list):
    start = time.time()
    possibilities = [0]

    all_ng_routes = {}
    node_objects = {node.number: node for node in nodeObjects}
    all_nodes = list(node_objects.keys())
    all_nodes.remove(starting_node)
    ng_set_i = set()

    def recursion(node, ng_set_before, visited):
        possibilities[0] += 1
        n = len(node_objects)
        node_object = node_objects[node]
        neighbours = set(node_object.neighbors)
        ng_set_j = list(set(ng_set_before) & neighbours)
        ng_set_j.append(node)
        ng_set_j = list(set(ng_set_j))
        visited.append(node)
        to_visit = [node for node in all_nodes if node not in ng_set_j]

        if len(visited) == n:
            visited.append(visited[0])
            costs = calculate_route_costs(visited, costs_list)
            all_ng_routes[costs] = visited
            return

        for node in to_visit:
            recursion(node, ng_set_j, visited.copy())

    recursion(starting_node, ng_set_i, [])

    cost = min(all_ng_routes.keys())
    best_route = all_ng_routes[cost]
    loops = find_loops(best_route)
    elementary = False
    cardinality = len(all_ng_routes)

    if len(loops) == 0:
        elementary = True

    end = time.time()
    return NgResult(best_route, cost, elementary, len(nodeObjects[0].neighbors), cardinality,
                    round(end - start, 3), len(possibilities))


def ng_routing_iteration(starting_node, nodeObjects, costsList):
    start = time.time()
    possibilities = 0

    all_ng_routes = {}
    node_objects = {node.number: node for node in nodeObjects}
    all_nodes = list(node_objects.keys())
    all_nodes.remove(starting_node)
    ng_set_i = set()
    n = len(node_objects)
    stack = [(starting_node, ng_set_i, [])]

    while stack:
        possibilities += 1
        node, ng_set_i, visited = stack.pop()
        node_object = node_objects[node]
        neighbours = set(node_object.neighbors)

        ng_set_j = list(set(ng_set_i) & neighbours)
        ng_set_j.append(node)
        ng_set_j = list(set(ng_set_j))

        visited.append(node)
        to_visit = [node for node in all_nodes if node not in ng_set_j]

        if len(visited) == n:
            visited.append(starting_node)
            costs = calculate_route_costs(visited, costsList)
            all_ng_routes[costs] = visited
            continue

        stack.extend((node, ng_set_j, visited.copy()) for node in to_visit)

    else:
        cost = min(all_ng_routes.keys())
        best_route = all_ng_routes[cost]
        loops = find_loops(best_route)
        elementary = False
        cardinality = len(all_ng_routes)

        if len(loops) == 0:
            elementary = True

        end = time.time()
        return NgResult(best_route, cost, elementary, len(nodeObjects[0].neighbors), cardinality,
                        round(end - start, 3), possibilities)


def dynamic_ng_pathing(starting_node, nodeObjects, costs_list, delta2, mode):
    start = time.time()
    i = 0

    results = []
    start_delta1 = len(nodeObjects[0].neighbors)
    max_delta1 = 0
    possibilities = 0

    while True:
        i += 1

        if mode == NgMode.iteration:
            result = ng_routing_iteration(starting_node, nodeObjects, costs_list)
        else:
            result = ng_routing_recursion(starting_node, nodeObjects, costs_list)

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
