import random
import pandas as pd
import csv
from Classes import Node
from Classes import NodeWithRoutes

path = '/Users/lukas/Documents/Stuff/'
nodes = pd.read_csv(path + 'nodes.csv', sep=',')
nodesWithoutRoutes = []

for ind in nodes.index:
    temp = Node(nodes['number'][ind], nodes['X'][ind], nodes['Y'][ind], nodes['Z'][ind])
    nodesWithoutRoutes.append(temp)

while True:
    nodesWithRoutes = []

    for node in nodesWithoutRoutes:
        amount = random.randrange(2, 8)
        nodeWithRoute = NodeWithRoutes(node.number, node.x, node.y, node.z)
        nodeWithRoute.routes = []

        for i in range(1, amount + 1):

            while True:
                randAmount = random.randrange(1, 101)
                if randAmount != nodeWithRoute.number and randAmount not in nodeWithRoute.routes:
                    break

            nodeWithRoute.routes.append(randAmount)
        nodesWithRoutes.append(nodeWithRoute)

    allRoutes = []
    for node in nodesWithRoutes:
        for route in node.routes:
            allRoutes.append(route)

    distinct = list(set(allRoutes))
    if len(distinct) == 100:
        break

fields = ["Number", "X", "Y", "Z", "Possible Routes"]
with open(path + 'nodes_with_routes.csv', 'w') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(fields)
    for node in nodesWithRoutes:
        write.writerow([node.number, node.x, node.y, node.z, node.routes])

print("Routes generated")
