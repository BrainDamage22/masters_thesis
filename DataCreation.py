# Create a hundred random data nodes with 3 dimensions
import csv
import random
from Classes import Node
import math

amount = 100
rangeX = 1000
rangeY = 1000
rangeZ = 1000
path = '/Users/lukas/Documents/Stuff/'

fields = ["number", "X", "Y", "Z"]
nodes = []

for i in range(1, amount + 1):
    randX = random.randrange(1, rangeX)
    randY = random.randrange(1, rangeY)
    randZ = random.randrange(1, rangeZ)
    nodes.append(Node(i, randX, randY, randZ))

with open(path + 'nodes.csv', 'w') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(fields)
    for datapoint in nodes:
        write.writerow([datapoint.number, datapoint.x, datapoint.y, datapoint.z])

print("Data generation done")

# Creating cost matrix between the nodes with Manhattan distance
totalCosts_manhattan = []
totalCosts_euclidean = []

for i in range(len(nodes)):
    costs_manhattan = []

    for datapoint in nodes:
        costs_manhattan.append(abs(nodes[i].x - datapoint.x) + abs(nodes[i].y - datapoint.y) + abs(
            nodes[i].z - datapoint.z))

    totalCosts_manhattan.append(costs_manhattan)

with open(path + 'costs_manhattan.csv', 'w') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)

    head = [0]
    for i in range(len(nodes)):
        head.append(i + 1)

    write.writerow(head)

    for i in range(len(totalCosts_manhattan)):
        totalCosts_manhattan[i].insert(0, i + 1)
        write.writerow(totalCosts_manhattan[i])

print("Cost computation Manhattan done")

for i in range(len(nodes)):
    costs_euclidean = []

    for datapoint in nodes:
        costs_euclidean.append(
            round(math.sqrt((nodes[i].x - datapoint.x) ** 2 + (nodes[i].y - datapoint.y) ** 2 + (
                    nodes[i].z - datapoint.z) ** 2), 2))

    totalCosts_euclidean.append(costs_euclidean)

with open(path + 'costs_euclidean.csv', 'w') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)

    head = [0]
    for i in range(len(nodes)):
        head.append(i + 1)

    write.writerow(head)

    for i in range(len(totalCosts_euclidean)):
        totalCosts_euclidean[i].insert(0, i + 1)
        write.writerow(totalCosts_euclidean[i])

print("Cost computation Euclidean done")
