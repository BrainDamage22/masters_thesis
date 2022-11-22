from Classes import Node
import pandas as pd
import csv

path = '/Users/lukas/Documents/Master Thesis/'
startingNode = 1

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

costs = 0
visited = [startingNode]
routeOfCosts = []
currentNodeNumber = startingNode
notVisited = list(range(1, len(nodes)))

while True:

    notVisited.remove(currentNodeNumber)

    if len(notVisited) == 0:

        lastCosts = costsList[currentNodeNumber - 1][startingNode - 1]
        costs += lastCosts
        routeOfCosts.append(lastCosts)
        visited.append(startingNode)

        print("Total costs: " + str(round(costs, 2)))
        print("Route:")
        print(visited)
        print("Costs:")
        print(routeOfCosts)

        with open(path + 'nearest_neighbor.csv', 'w') as f:
            write = csv.writer(f)
            write.writerow(visited)
            write.writerow([costs])
        break

    possibleDestinations = {"Number": [], "Cost": []}
    currentNodeCosts = costsList[currentNodeNumber - 1]

    for node in notVisited:
        possibleDestinations["Number"].append(node)
        possibleDestinations["Cost"].append(currentNodeCosts[node - 1])

    minCosts = min(possibleDestinations["Cost"])
    minCostIndex = possibleDestinations["Cost"].index(minCosts)
    currentNodeNumber = possibleDestinations["Number"][minCostIndex]
    costs += minCosts
    visited.append(currentNodeNumber)
    routeOfCosts.append(minCosts)
