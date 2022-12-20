from Classes import Node, NodeWithNeighbours
import pandas as pd
from NearestNeighbor import find_x_nearest_neighbours, find_nearest_neighbours_path
import time

start_time = time.time()

path = '/Users/lukas/Documents/Master Thesis/'
startingNode = 1
delta1 = 4

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

all_ng_routes = {}

find_nearest_neighbours_path(nodes, costsList, startingNode)

def calculate_route_costs(route, listOfCosts):
    costs = 0
    for i in range(len(route) - 1):
        costs += listOfCosts[route[i]][route[i + 1]]

    return round(costs, 2)


def ng_routing(currentNode, nodeObjects, listOfCosts, visited, notVisited, ngSetI, numberOfNodes):
    n = numberOfNodes
    ng_set_j = list(set(ngSetI).intersection(set(nodeObjects[currentNode].neighbours)))
    ng_set_j.append(currentNode)
    visited.append(currentNode)
    to_visit = [x for x in notVisited if x not in ng_set_j]

    if len(visited) == n:
        costs = calculate_route_costs(visited, listOfCosts)
        all_ng_routes[costs] = visited
        return 0

    for item in to_visit:
        to_visit_in_next_step = notVisited.copy()
        to_visit_in_next_step.remove(item)

        ng_routing(item, nodeObjects.copy(), listOfCosts.copy(), visited.copy(), to_visit_in_next_step.copy(),
                   ng_set_j.copy(), n)


to_visit_param = list(range(0, len(nodes)))
to_visit_param.remove(startingNode)
ng_routing(startingNode, node_objects.copy(), costsList.copy(), [], to_visit_param.copy(), [], len(nodes))

# print(all_ng_routes.keys())
min_value = min(all_ng_routes.keys())
print(min_value)
print(all_ng_routes[min_value])
print("--- %s seconds ---" % (time.time() - start_time))
