from util import find_loops, calculate_route_costs, print_exceeded, save_results
from classes import IterationResult


def ng_routing(startingNode, nodeObjects, allNodes, ngSetI, n, costsList):
    all_ng_routes = {}

    node_objects = {node.number: node for node in nodeObjects}
    ng_set_i = set(ngSetI)
    stack = [(startingNode, ng_set_i, [])]

    while stack:
        node, ng_set_i, visited = stack.pop()
        node_object = node_objects[node]
        neighbours = set(node_object.neighbours)
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
        return all_ng_routes


def dynamic_ng_pathing(startingNode, nodeObjects, allNodes, ngSetI, n, delta2, costsList, path):
    i = 0
    results = []
    max_delta1 = 0

    while True:
        i += 1
        all_ng_routes = ng_routing(startingNode, nodeObjects, allNodes, ngSetI, n, costsList)
        min_value = min(all_ng_routes.keys())
        best_route = all_ng_routes[min_value]
        loops = find_loops(best_route)

        for node in nodeObjects:
            if len(node.neighbours) > max_delta1:
                max_delta1 = len(node.neighbours)

        if len(loops) == 0:
            print("")
            print("Best Route in iteration: " + str(i))
            print(best_route)
            print("Costs :", str(min_value))
            result = IterationResult(best_route, min_value, loops, len(all_ng_routes), max_delta1, delta2, False)
            results.append(result)
            save_results(path, results)
            break

        print("")
        print(str(i) + ". Iteration")
        print(best_route)
        print("Costs :", str(min_value))
        print("Sub Routes:")
        print(loops)
        result = IterationResult(best_route, min_value, loops, len(all_ng_routes), max_delta1, delta2, False)
        results.append(result)

        loop_with_smallest_cardinality = min(loops, key=len)
        start_and_ending_node = loop_with_smallest_cardinality[0]
        loop_with_smallest_cardinality = loop_with_smallest_cardinality[1:-1]

        if len(loop_with_smallest_cardinality) >= delta2:
            print_exceeded(best_route, min_value)
            result = IterationResult(best_route, min_value, loops, len(all_ng_routes), max_delta1, delta2, True)
            results.append(result)
            save_results(path, results)
            return

        for node in nodeObjects:
            for route_node in loop_with_smallest_cardinality:
                if node.number == route_node and start_and_ending_node not in node.neighbours:
                    if len(node.neighbours) < delta2:
                        node.neighbours.append(start_and_ending_node)
                    else:
                        print_exceeded(best_route, min_value)
                        result = IterationResult(best_route, min_value, loops, len(all_ng_routes), max_delta1, delta2,
                                                 True)
                        results.append(result)
                        save_results(path, results)
                        return
