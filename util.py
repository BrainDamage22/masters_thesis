import pandas as pd
from classes import Node, NodeWithNeighbours
from nearest_neighbor import find_x_nearest_neighbours


def read_data(path):
    nodes_csv = pd.read_csv(path + 'nodes.csv', sep=',')
    costs_csv = pd.read_csv(path + 'costs_euclidean.csv', sep=',')
    costs_csv = costs_csv.iloc[:, 1:]

    costs_list = []
    for ind in costs_csv.index:
        costs_list.append(costs_csv.iloc[ind].to_numpy())

    nodes = []
    for ind in nodes_csv.index:
        temp = Node(nodes_csv['Number'][ind], nodes_csv['X'][ind], nodes_csv['Y'][ind])
        nodes.append(temp)

    return costs_list, nodes


def calculate_n_sets(costsList, nodes, delta1):
    node_objects = []
    for node in nodes:
        node_objects.append(
            NodeWithNeighbours(node.number, node.x, node.y, find_x_nearest_neighbours(costsList[node.number - 1], delta1)))
    return node_objects


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


def calculate_route_costs(route, costsList):
    costs = 0
    for i in range(len(route) - 1):
        costs += costsList[route[i]][route[i + 1]]
    return round(costs, 2)


def print_exceeded(best_route, min_value):
    print("")
    print("Delta 2 exceeded")
    print("Best Route:")
    print(best_route)
    print("Costs :", str(min_value))
