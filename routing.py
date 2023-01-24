from util import find_loops, calculate_route_costs, print_exceeded
from classes import DngResult, NgResult
import time


def ng_routing(startingNode, nodeObjects, allNodes, ngSetI, n, costsList):
    start = time.time()
    possibilities = 0
    all_ng_routes = {}

    node_objects = {node.number: node for node in nodeObjects}
    ng_set_i = set(ngSetI)
    stack = [(startingNode, ng_set_i, [])]

    while stack:
        possibilities += 1
        node, ng_set_i, visited = stack.pop()
        node_object = node_objects[node]
        neighbours = set(node_object.neighbors)
        ng_set_j = list(set(ng_set_i) & neighbours)
        ng_set_j.append(node)
        ng_set_j = list(set(ng_set_j))

        visited.append(node)
        to_visit = [node for node in allNodes if node not in ng_set_j]

        if len(visited) == n:
            visited.append(startingNode)
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


def dynamic_ng_pathing(startingNode, nodeObjects, allNodes, ngSetI, n, delta2, costsList):
    start = time.time()
    i = 0
    results = []
    start_delta1 = len(nodeObjects[0].neighbors)
    max_delta1 = 0
    possibilities = 0

    while True:
        i += 1
        result = ng_routing(startingNode, nodeObjects, allNodes, ngSetI, n, costsList)
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
            result = DngResult(best_route, cost, loops, result.cardinality, start_delta1, max_delta1, delta2, False, True, i, round(end - start, 3), possibilities)
            results.append(result)

            return result, results

        print("")
        print(str(i) + ". Iteration")
        print(best_route)
        print("Costs :", str(cost))
        print("Sub Routes:")
        print(loops)
        end = time.time()
        result = DngResult(best_route, cost, loops, result.cardinality, start_delta1, max_delta1, delta2, False, False, i, round(end - start, 3), possibilities)
        results.append(result)

        loop_with_smallest_cardinality = min(loops, key=len)
        start_and_ending_node = loop_with_smallest_cardinality[0]
        loop_with_smallest_cardinality = loop_with_smallest_cardinality[1:-1]

        if len(loop_with_smallest_cardinality) >= delta2:
            print_exceeded(best_route, cost)
            end = time.time()
            result = DngResult(best_route, cost, loops, result.cardinality, start_delta1, max_delta1, delta2, True, False, i, round(end - start, 3), possibilities)
            return result, results

        for node in nodeObjects:
            for route_node in loop_with_smallest_cardinality:
                if node.number == route_node and start_and_ending_node not in node.neighbors:
                    if len(node.neighbors) < delta2:
                        node.neighbors.append(start_and_ending_node)
                    else:
                        print_exceeded(best_route, cost)
                        end = time.time()
                        result = DngResult(best_route, cost, loops, result.cardinality, start_delta1, max_delta1, delta2, True, False, i, round(end - start, 3), possibilities)
                        return result, results
