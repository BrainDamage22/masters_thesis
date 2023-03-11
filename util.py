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
                    data_csv['elementary'].item(), data_csv['delta1'].item(), data_csv['time'].item(),
                    data_csv['all_ext'].item(), data_csv['followed_ext'].item(), data_csv['ub_ext'].item(),
                    data_csv['lut_ext'].item(), data_csv['lut_up_ext'].item(), data_csv['oob_ext'].item())
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
                            data_csv['time'][ind].item(),
                            data_csv['all_ext'][ind].item(), data_csv['followed_ext'][ind].item(),
                            data_csv['ub_ext'][ind].item(),
                            data_csv['lut_ext'][ind].item(), data_csv['lut_up_ext'][ind].item(),
                            data_csv['oob_ext'][ind].item())
            test_results.append(temp)
        results.append(test_results)

    return results


def read_dng_data(path):
    data_csv = pd.read_csv(path + '/results/dng_result/dng_result.csv')

    results = []
    for ind in data_csv.index:
        temp = DngResult(data_csv["best_route"].apply(literal_eval)[ind], data_csv["cost"][ind].item(),
                         data_csv["len_sub_tours"][ind].item(), data_csv["start_delta1"][ind].item(),
                         data_csv["final_delta1"][ind].item(), data_csv["delta2"][ind].item(),
                         data_csv["exceeded"][ind].item(), data_csv["elementary"][ind].item(),
                         data_csv["dng_iterations"][ind].item(), data_csv["time"][ind].item(),
                         data_csv['all_ext'][ind].item(), data_csv['followed_ext'][ind].item(),
                         data_csv['ub_ext'][ind].item(), data_csv['lut_ext'][ind].item(),
                         data_csv['lut_up_ext'][ind].item(), data_csv['oob_ext'][ind].item())
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
                             data_csv["len_sub_tours"][ind].item(), data_csv["start_delta1"][ind].item(),
                             data_csv["final_delta1"][ind].item(), data_csv["delta2"][ind].item(),
                             data_csv["exceeded"][ind].item(), data_csv["elementary"][ind].item(),
                             data_csv["dng_iterations"][ind].item(), data_csv["time"][ind].item(),
                             data_csv['all_ext'][ind].item(), data_csv['followed_ext'][ind].item(),
                             data_csv['ub_ext'][ind].item(), data_csv['lut_ext'][ind].item(),
                             data_csv['lut_up_ext'][ind].item(), data_csv['oob_ext'][ind].item())
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


def calculate_route_costs_dmp(route, costsList):
    costs = 0
    n = len(route) - 1
    k = 0
    for i in range(len(route) - 1):
        k += 1
        costs += (n - k + 1) * costsList[route[i]][route[i + 1]]
    return costs


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

        fields = ['best_route', 'cost', 'len_sub_tours', 'start_delta1', 'final_delta1', 'delta2', 'exceeded',
                  'elementary', 'dng_iterations', 'time', 'all_ext', 'followed_ext', 'ub_ext', 'lut_ext', 'lut_up_ext',
                  'oob_ext']
        write.writerow(fields)
        for result in results:
            write.writerow(
                [result.best_route, result.cost, result.len_sub_tours, result.start_delta1,
                 result.final_delta1, result.delta2, result.exceeded, result.elementary,
                 result.dng_iterations, result.time, result.all_ext, result.followed_ext, result.ub_ext, result.lut_ext,
                 result.lut_up_ext, result.oob_ext])


def save_dng_test_results(path, results, number):
    path = path + 'results/dng_test_result'
    filename = 'dng_test_result_'

    if not os.path.isdir(path):
        os.makedirs(path)

    with open(path + '/' + filename + number + '.csv', 'w') as f:
        write = csv.writer(f)

        fields = ['best_route', 'cost', 'len_sub_tours', 'start_delta1', 'final_delta1', 'delta2', 'exceeded',
                  'elementary', 'dng_iterations', 'time', 'all_ext', 'followed_ext', 'ub_ext', 'lut_ext', 'lut_up_ext',
                  'oob_ext']
        write.writerow(fields)

        for result in results:
            write.writerow(
                [result.best_route, result.cost, result.len_sub_tours, result.start_delta1,
                 result.final_delta1, result.delta2, result.exceeded, result.elementary,
                 result.dng_iterations, result.time, result.all_ext, result.followed_ext, result.ub_ext, result.lut_ext,
                 result.lut_up_ext, result.oob_ext])


def save_ng_result(path, result):
    filename = 'ng_result.csv'
    path = path + 'results/ng_result'

    if not os.path.isdir(path):
        os.makedirs(path)

    with open(path + '/' + filename + '', 'w') as f:
        write = csv.writer(f)

        fields = ['best_route', 'cost', 'elementary', 'delta1', 'time', "all_ext", "followed_ext", "ub_ext", "lut_ext",
                  "lut_up_ext", "oob_ext"]
        write.writerow(fields)
        write.writerow(
            [result.best_route, result.cost, result.elementary, result.delta1, result.time, result.all_ext,
             result.followed_ext, result.ub_ext, result.lut_ext, result.lut_up_ext, result.oob_ext])


def save_ng_test_results(path, results, number):
    path = path + 'results/ng_test_result'
    filename = 'ng_test_result_'

    if not os.path.isdir(path):
        os.makedirs(path)

    with open(path + '/' + filename + number + '.csv', 'w') as f:
        write = csv.writer(f)

        fields = ['best_route', 'cost', 'elementary', 'delta1', 'time', "all_ext", "followed_ext", "ub_ext", "lut_ext",
                  "lut_up_ext", "oob_ext"]
        write.writerow(fields)

        for result in results:
            write.writerow(
                [result.best_route, result.cost, result.elementary, result.delta1, result.time, result.all_ext,
                 result.followed_ext, result.ub_ext, result.lut_ext, result.lut_up_ext, result.oob_ext])


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
