# Create X random vertices with 2 dimensions
import csv
import random
from classes import Node
import math
import os


# This function generates random data for a routing problem and saves it to CSV files.
# It generates 'amount' nodes with random coordinates within the given ranges, and
# computes the Manhattan and Euclidean distances between each pair of nodes.
def create_data(amount, rangeX, rangeY, path):
    fields = ["Number", "X", "Y"]
    nodes = []

    # Create the directory for storing the data if it doesn't exist
    if not os.path.isdir(path):
        os.makedirs(path)

    # Generate random nodes
    for i in range(0, amount):
        rand_x = random.randrange(1, rangeX)
        rand_y = random.randrange(1, rangeY)
        nodes.append(Node(i, rand_x, rand_y))

    # Save the nodes to a CSV file
    with open(path + 'nodes.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        for datapoint in nodes:
            write.writerow([datapoint.number, datapoint.x, datapoint.y])

    # Calculate Manhattan distances between nodes
    total_costs_manhattan = []
    for i in range(len(nodes)):
        costs_manhattan = []
        for datapoint in nodes:
            costs_manhattan.append(abs(nodes[i].x - datapoint.x) + abs(nodes[i].y - datapoint.y))
        total_costs_manhattan.append(costs_manhattan)

    # Save the Manhattan distances to a CSV file
    with open(path + 'costs_manhattan.csv', 'w') as f:
        write = csv.writer(f)
        head = [0] + list(range(1, len(nodes) + 1))
        write.writerow(head)
        for i in range(len(total_costs_manhattan)):
            total_costs_manhattan[i].insert(0, i + 1)
            write.writerow(total_costs_manhattan[i])

    # Calculate Euclidean distances between nodes
    total_costs_euclidean = []
    for i in range(len(nodes)):
        costs_euclidean = []
        for datapoint in nodes:
            costs_euclidean.append(round(math.sqrt((nodes[i].x - datapoint.x) ** 2 + (nodes[i].y - datapoint.y) ** 2), 2))
        total_costs_euclidean.append(costs_euclidean)

    # Save the Euclidean distances to a CSV file
    with open(path + 'costs_euclidean.csv', 'w') as f:
        write = csv.writer(f)
        head = [0] + list(range(1, len(nodes) + 1))
        write.writerow(head)
        for i in range(len(total_costs_euclidean)):
            total_costs_euclidean[i].insert(0, i + 1)
            write.writerow(total_costs_euclidean[i])

    print("Data generation done")



