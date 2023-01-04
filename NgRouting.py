from Classes import Node, NodeWithNeighbours
import pandas as pd
from NearestNeighbor import find_x_nearest_neighbours, find_nearest_neighbours_path
import time

start_time = time.time()

path = '/Users/lukas/Documents/Master Thesis/'
startingNode = 1
delta1 = 6
delta2 = 8

nodes_csv = pd.read_csv(path + 'nodes.csv', sep=',')
costs_csv = pd.read_csv(path + 'costs_euclidean.csv', sep=',')
costs_csv = costs_csv.iloc[:, 1:]

costsList = []
for ind in costs_csv.index:
    costsList.append(costs_csv.iloc[ind].to_numpy())

nodes = []
for ind in nodes_csv.index:
    temp = Node(nodes_csv['Number'][ind], nodes_csv['X'][ind], nodes_csv['Y'][ind])
    nodes.append(temp)

node_objects = []

for node in nodes:
    node_objects.append(
        NodeWithNeighbours(node.number, node.x, node.y, find_x_nearest_neighbours(costsList[node.number - 1], delta1)))


def calculate_route_costs(route):
    costs = 0
    for i in range(len(route) - 1):
        costs += costsList[route[i]][route[i + 1]]

    return round(costs, 2)


def find_loops(arr):
    # Initialize an empty dictionary to store the indices at which each element appears.
    indices = {}
    loops = []

    # Iterate through the array.
    for i, elem in enumerate(arr):
        # If the current element has already been seen, add the loop to the list of loops.
        if elem in indices:
            start_index = indices[elem]
            loop = arr[start_index:i+1]
            if len(loop) != len(arr):
                loops.append(loop)

        # Otherwise, store the current index in the dictionary.
        indices[elem] = i

    # Return the list of loops.
    return loops


# def ng_routing2(currentNode, nodeObjects, visited, allNodes, ngSetI, n):
#     node_object = next(x for x in nodeObjects if x.number == currentNode+1)
#     ng_set_j = list(set(ngSetI).intersection(set(node_object.neighbours)))
#
#     if currentNode not in ng_set_j:
#         ng_set_j.append(currentNode)
#
#     visited.append(currentNode)
#     to_visit = [x for x in allNodes if x not in ng_set_j]
#
#     if len(visited) == n:
#         costs = calculate_route_costs(visited)
#         # print(costs, visited)
#         all_ng_routes[costs] = visited
#         return
#
#     for item in to_visit:
#         ng_routing2(item, nodeObjects.copy(), visited.copy(), allNodes.copy(), ng_set_j.copy(), n)


def ng_routing(startingNode, nodeObjects, allNodes, ngSetI, n):
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
            costs = calculate_route_costs(visited)
            all_ng_routes[costs] = visited
            continue

        stack.extend((node, ng_set_j, visited.copy()) for node in to_visit)

    else:
        return all_ng_routes


def dynamic_ng_pathing(startingNode, nodeObjects, allNodes, ngSetI, n):
    i = 0

    while True:
        i += 1
        all_ng_routes = ng_routing(startingNode, nodeObjects, allNodes, ngSetI, n)
        min_value = min(all_ng_routes.keys())
        best_route = all_ng_routes[min_value]

        loops = find_loops(best_route)

        if len(loops) == 0:
            print("")
            print("Best Route:")
            print(best_route)
            print("Costs:")
            print(min_value)
            break

        print("")
        print(str(i) + ". Iteration")
        print(best_route)
        print("Sub Routes:")
        print(loops)
        loop_with_smallest_cardinality = min(loops, key=len)
        start_and_ending_node = loop_with_smallest_cardinality[0]
        loop_with_smallest_cardinality = loop_with_smallest_cardinality[1:-1]

        if len(loop_with_smallest_cardinality) >= delta2:
            print("")
            print("Delta 2 exceeded")
            print("Best Route:")
            print(best_route)
            print("Costs:")
            print(min_value)
            return

        for node in node_objects:
            for route_node in loop_with_smallest_cardinality:
                if node.number == route_node and start_and_ending_node not in node.neighbours:
                    if len(node.neighbours) < delta2:
                        node.neighbours.append(start_and_ending_node)
                    else:
                        print("")
                        print("Delta 2 exceeded")
                        print("Best Route:")
                        print(best_route)
                        print("Costs:")
                        print(min_value)
                        return


to_visit_param = list(range(0, len(nodes)))
to_visit_param.remove(startingNode)

dynamic_ng_pathing(startingNode, node_objects.copy(), to_visit_param.copy(), [], len(nodes))
print("--- %s seconds ---" % (time.time() - start_time))
