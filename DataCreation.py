# Create X random vertices with 2 dimensions
import csv
import random
from Classes import Node
import math

amount = 15
rangeX = 100
rangeY = 100
path = '/Users/lukas/Documents/Master Thesis/'

fields = ["Number", "X", "Y"]
nodes = []

for i in range(1, amount + 1):
    randX = random.randrange(1, rangeX)
    randY = random.randrange(1, rangeY)
    nodes.append(Node(i, randX, randY))


random.shuffle(nodes)

with open(path + 'nodes.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(fields)
    for datapoint in nodes:
        write.writerow([datapoint.number, datapoint.x, datapoint.y])

print("Data generation done")

totalCosts_manhattan = []
totalCosts_euclidean = []

for i in range(len(nodes)):
    costs_manhattan = []

    for datapoint in nodes:
        costs_manhattan.append(abs(nodes[i].x - datapoint.x) + abs(nodes[i].y - datapoint.y))

    totalCosts_manhattan.append(costs_manhattan)

with open(path + 'costs_manhattan.csv', 'w') as f:
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
            round(math.sqrt((nodes[i].x - datapoint.x) ** 2 + (nodes[i].y - datapoint.y) ** 2), 2))

    totalCosts_euclidean.append(costs_euclidean)

with open(path + 'costs_euclidean.csv', 'w') as f:
    write = csv.writer(f)

    head = [0]
    for i in range(len(nodes)):
        head.append(i + 1)

    write.writerow(head)

    for i in range(len(totalCosts_euclidean)):
        totalCosts_euclidean[i].insert(0, i + 1)
        write.writerow(totalCosts_euclidean[i])

print("Cost computation Euclidean done")
