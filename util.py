import csv
import os
import glob
import pandas as pd
from classes import Node, NodeWithNeighbors, NgResult, DngResult, SortOption
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
    temp = NgResult(data_csv['best_route'].apply(literal_eval).item(), data_csv['cost'].item(),
                    data_csv['elementary'].item(), data_csv['delta1'].item(), data_csv['cardinality'].item(),
                    data_csv['time'].item(), data_csv['ng_iterations'].item())
    return temp


def read_ng_test_data(path):
    path = path + "results/ng_test_result/"
    csv_files = glob.glob(os.path.join(path, "*.csv"))

    results = []
    for file in csv_files:
        data_csv = pd.read_csv(file)
        test_results = []
        for ind in data_csv.index:
            temp = NgResult(data_csv['best_route'].apply(literal_eval)[ind], data_csv['cost'][ind].item(),
                            data_csv['elementary'][ind].item(), data_csv['delta1'][ind].item(),
                            data_csv['cardinality'][ind].item(),
                            data_csv['time'][ind].item(), data_csv['ng_iterations'][ind].item())
            test_results.append(temp)
        results.append(test_results)

    return results


def read_dng_data(path):
    data_csv = pd.read_csv(path + '/results/dng_result/dng_result.csv')

    results = []
    for ind in data_csv.index:
        temp = DngResult(data_csv["best_route"].apply(literal_eval)[ind], data_csv["cost"][ind].item(),
                         data_csv["sub_tours"].apply(literal_eval)[ind],
                         data_csv["cardinality"][ind].item(), data_csv["start_delta1"][ind].item(),
                         data_csv["final_delta1"][ind].item(), data_csv["delta2"][ind].item(),
                         data_csv["exceeded"][ind].item(),
                         data_csv["elementary"][ind].item(), data_csv["iterations"][ind].item(),
                         data_csv["time"][ind].item(), data_csv['ng_iterations'][ind].item())
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
            temp = DngResult(data_csv["best_route"].apply(literal_eval)[ind], data_csv["cost"][ind].item(),
                             data_csv["sub_tours"].apply(literal_eval)[ind],
                             data_csv["cardinality"][ind].item(), data_csv["start_delta1"][ind].item(),
                             data_csv["final_delta1"][ind].item(), data_csv["delta2"][ind].item(),
                             data_csv["exceeded"][ind].item(),
                             data_csv["elementary"][ind].item(), data_csv["iterations"][ind].item(),
                             data_csv["time"][ind].item(), data_csv['ng_iterations'][ind].item())
            test_results.append(temp)
        results.append(test_results)

    return results


def calculate_n_sets(costsList, nodes, delta1):
    node_objects = []
    for node in nodes:
        node_objects.append(
            NodeWithNeighbors(node.number, node.x, node.y,
                              find_x_nearest_neighbours(costsList[node.number], delta1)))
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


def print_exceeded(best_route, cost):
    print('')
    print('Delta 2 exceeded')
    print('best_route:')
    print(best_route)
    print('Costs :', str(cost))


def save_dng_results(path, results):
    filename = 'dng_result.csv'
    path = path + 'results/dng_result'

    if not os.path.isdir(path):
        os.makedirs(path)

    with open(path + '/' + filename + '', 'w') as f:
        write = csv.writer(f)

        fields = ['elementary', 'best_route', 'cost', 'sub_tours', 'iterations', 'cardinality', 'delta2',
                  'start_delta1', 'final_delta1', 'exceeded', 'time', "ng_iterations"]
        write.writerow(fields)
        for result in results:
            write.writerow(
                [result.elementary, result.best_route, result.cost, result.sub_tours, result.iterations,
                 result.cardinality, result.delta2, result.start_delta1, result.final_delta1,
                 result.exceeded, result.time, result.ng_iterations])


def save_dng_test_results(path, results, number):
    path = path + 'results/dng_test_result'
    filename = 'dng_test_result_'

    if not os.path.isdir(path):
        os.makedirs(path)

    with open(path + '/' + filename + number + '.csv', 'w') as f:
        write = csv.writer(f)

        fields = ['elementary', 'best_route', 'cost', 'sub_tours', 'iterations', 'cardinality', 'delta2',
                  'start_delta1', 'final_delta1', 'exceeded', 'time', "ng_iterations"]
        write.writerow(fields)

        for result in results:
            write.writerow(
                [result.elementary, result.best_route, result.cost, result.sub_tours, result.iterations,
                 result.cardinality, result.delta2, result.start_delta1, result.final_delta1,
                 result.exceeded, result.time, result.ng_iterations])


def save_ng_result(path, result):
    filename = 'ng_result.csv'
    path = path + 'results/ng_result'

    if not os.path.isdir(path):
        os.makedirs(path)

    with open(path + '/' + filename + '', 'w') as f:
        write = csv.writer(f)

        fields = ['best_route', 'cost', 'elementary', 'delta1', 'cardinality', 'time', "ng_iterations"]
        write.writerow(fields)
        write.writerow(
            [result.best_route, result.cost, result.elementary, result.delta1, result.cardinality, result.time,
             result.ng_iterations])


def save_ng_test_results(path, results, number):
    path = path + 'results/ng_test_result'
    filename = 'ng_test_result_'

    if not os.path.isdir(path):
        os.makedirs(path)

    with open(path + '/' + filename + number + '.csv', 'w') as f:
        write = csv.writer(f)

        fields = ['best_route', 'cost', 'elementary', 'delta1', 'cardinality', 'time', "ng_iterations"]
        write.writerow(fields)

        for result in results:
            write.writerow(
                [result.best_route, result.cost, result.elementary, result.delta1, result.cardinality,
                 result.time, result.ng_iterations])


def group_data_by(to_group, sort_option):
    if sort_option == SortOption.delta2:
        max_delta2 = max(item.delta2 for item in to_group)
        return_list = []
        for k in range(0, max_delta2):
            return_list.append([])
            for item in to_group:
                if k + 1 == item.delta2:
                    return_list[k].append(item)
        return return_list

    if sort_option == SortOption.start_delta1:
        max_start_delta1 = max(item.start_delta1 for item in to_group)
        return_list = []
        for k in range(0, max_start_delta1):
            return_list.append([])
            for item in to_group:
                if k + 1 == item.start_delta1:
                    return_list[k].append(item)
        return return_list

    if sort_option == SortOption.final_delta1:
        max_final_delta1 = max(item.final_delta1 for item in to_group)
        return_list = []
        for k in range(0, max_final_delta1):
            return_list.append([])
            for item in to_group:
                if k + 1 == item.final_delta1:
                    return_list[k].append(item)
        return return_list

    if sort_option == SortOption.elementary:
        elem = []
        not_elem = []
        for item in to_group:
            if item.elementary:
                elem.append(item)
            else:
                not_elem.append(item)
        return elem, not_elem

    if sort_option == SortOption.exceeded:
        elem = []
        not_elem = []
        for item in to_group:
            if item.exceeded:
                elem.append(item)
            else:
                not_elem.append(item)
        return elem, not_elem

    if sort_option == SortOption.iterations:
        max_iterations = max(item.iterations for item in to_group)
        return_list = []
        for k in range(1, max_iterations + 1):
            return_list.append([])
            for item in to_group:
                if k == item.iterations:
                    return_list[k - 1].append(item)
        return return_list
