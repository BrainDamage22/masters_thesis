import csv
import os
import glob
import pandas as pd
from classes import Node, NodeWithNeighbors, NgResult, DngResult
from nearest_neighbor import find_x_nearest_neighbours
from ast import literal_eval


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


def read_ng_data(path):
    data_csv = pd.read_csv(path + '/results/ng_result/ng_result.csv')
    temp = NgResult(data_csv['best_route'].apply(literal_eval).item(), data_csv['min_cost'].item(),
                    data_csv['elementary'].item(), data_csv['delta1'].item(), data_csv['cardinality'].item(),
                    data_csv['time'].item())
    return temp


def read_ng_test_data(path):
    path = path + "results/ng_test_result/"
    csv_files = glob.glob(os.path.join(path, "*.csv"))

    results = []
    for file in csv_files:
        data_csv = pd.read_csv(file)
        test_results = []
        for ind in data_csv.index:
            temp = NgResult(data_csv['best_route'].apply(literal_eval)[ind], data_csv['min_cost'][ind].item(),
                            data_csv['elementary'][ind].item(), data_csv['delta1'][ind].item(),
                            data_csv['cardinality'][ind].item(),
                            data_csv['time'][ind].item())
            test_results.append(temp)
        results.append(test_results)

    return results


def read_dng_data(path):
    data_csv = pd.read_csv(path + '/results/dng_result/dng_result.csv')

    results = []
    for ind in data_csv.index:
        temp = DngResult(data_csv["best_route"].apply(literal_eval)[ind], data_csv["min_cost"][ind].item(), data_csv["sub_tours"].apply(literal_eval)[ind],
                         data_csv["cardinality"][ind].item(), data_csv["start_delta1"][ind].item(),
                         data_csv["final_delta1"][ind].item(), data_csv["delta2"][ind].item(), data_csv["exceeded"][ind].item(),
                         data_csv["elementary"][ind].item(), data_csv["iterations"][ind].item(), data_csv["time"][ind].item())
        results.append(temp)

    return results


def read_dng_test_data(path):
    path = path + "results/dng_test_result/"
    csv_files = glob.glob(os.path.join(path, "*.csv"))

    results = []
    for file in csv_files:
        data_csv = pd.read_csv(file)
        test_results = []
        for ind in data_csv.index:
            temp = DngResult(data_csv["best_route"].apply(literal_eval)[ind], data_csv["min_cost"][ind].item(),
                             data_csv["sub_tours"].apply(literal_eval)[ind],
                             data_csv["cardinality"][ind].item(), data_csv["start_delta1"][ind].item(),
                             data_csv["final_delta1"][ind].item(), data_csv["delta2"][ind].item(),
                             data_csv["exceeded"][ind].item(),
                             data_csv["elementary"][ind].item(), data_csv["iterations"][ind].item(),
                             data_csv["time"][ind].item())
            test_results.append(temp)
        results.append(test_results)

    return results


def calculate_n_sets(costsList, nodes, delta1):
    node_objects = []
    for node in nodes:
        node_objects.append(
            NodeWithNeighbors(node.number, node.x, node.y,
                              find_x_nearest_neighbours(costsList[node.number - 1], delta1)))
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
            loop = arr[start_index:i + 1]
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
    print('')
    print('Delta 2 exceeded')
    print('best_route:')
    print(best_route)
    print('Costs :', str(min_value))


def save_dng_results(path, results):
    filename = 'dng_result.csv'
    path = path + 'results/dng_result'

    if not os.path.isdir(path):
        os.makedirs(path)

    with open(path + '/' + filename + '', 'w') as f:
        write = csv.writer(f)

        fields = ['elementary', 'best_route', 'min_cost', 'sub_tours', 'iterations', 'cardinality', 'delta2',
                  'start_delta1', 'final_delta1', 'exceeded', 'time']
        write.writerow(fields)
        for result in results:
            write.writerow(
                [result.elementary, result.best_route, result.min_cost, result.sub_tours, result.iterations,
                 result.cardinality, result.delta2, result.start_delta1, result.final_delta1,
                 result.exceeded, result.time])


def save_dng_test_results(path, results, number):
    path = path + 'results/dng_test_result'
    filename = 'dng_test_result_'

    if not os.path.isdir(path):
        os.makedirs(path)

    with open(path + '/' + filename + number + '.csv', 'w') as f:
        write = csv.writer(f)

        fields = ['elementary', 'best_route', 'min_cost', 'sub_tours', 'iterations', 'cardinality', 'delta2',
                  'start_delta1', 'final_delta1', 'exceeded', 'time']
        write.writerow(fields)

        for result in results:
            write.writerow(
                [result.elementary, result.best_route, result.min_cost, result.sub_tours, result.iterations,
                 result.cardinality, result.delta2, result.start_delta1, result.final_delta1,
                 result.exceeded, result.time])


def save_ng_result(path, result):
    filename = 'ng_result.csv'
    path = path + 'results/ng_result'

    if not os.path.isdir(path):
        os.makedirs(path)

    with open(path + '/' + filename + '', 'w') as f:
        write = csv.writer(f)

        fields = ['best_route', 'min_cost', 'elementary', 'delta1', 'cardinality', 'time']
        write.writerow(fields)
        write.writerow(
            [result.best_route, result.min_value, result.elementary, result.delta1, result.cardinality, result.time])


def save_ng_test_results(path, results, number):
    path = path + 'results/ng_test_result'
    filename = 'ng_test_result_'

    if not os.path.isdir(path):
        os.makedirs(path)

    with open(path + '/' + filename + number + '.csv', 'w') as f:
        write = csv.writer(f)

        fields = ['best_route', 'min_cost', 'elementary', 'delta1', 'cardinality', 'time']
        write.writerow(fields)

        for result in results:
            write.writerow(
                [result.best_route, result.min_value, result.elementary, result.delta1, result.cardinality,
                 result.time])
