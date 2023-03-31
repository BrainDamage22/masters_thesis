import csv
import os
import glob
import pandas as pd
from classes import Node, NodeWithNeighbors, NgResult, DngResult, SortOption
from nearest_neighbor import find_x_nearest_neighbours
from ast import literal_eval


# This function reads node data and Euclidean costs data from CSV files in the given path,
# and returns a list of Node objects and a list of costs between each pair of nodes.
def read_data(path):
    # Read the node data from the CSV file
    nodes_csv = pd.read_csv(path + 'nodes.csv', sep=',')

    # Read the Euclidean costs data from the CSV file
    costs_csv = pd.read_csv(path + 'costs_euclidean.csv', sep=',')
    costs_csv = costs_csv.iloc[:, 1:]  # Remove the first column (node numbers)

    # Convert the costs data to a list of numpy arrays
    costs_list = []
    for ind in costs_csv.index:
        costs_list.append(costs_csv.iloc[ind].to_numpy())

    # Create a list of Node objects from the node data
    nodes = []
    for ind in nodes_csv.index:
        temp = Node(nodes_csv['Number'][ind], nodes_csv['X'][ind], nodes_csv['Y'][ind])
        nodes.append(temp)

    return costs_list, nodes


# This function reads the results of the ng-routing algorithm from a CSV file in the given path,
# and returns an NgResult object containing the results.
def read_ng_data(path):
    # Read the ng_result data from the CSV file
    data_csv = pd.read_csv(path + '/results/ng_result/ng_result.csv')

    # Create an NgResult object from the data
    temp = NgResult(
        data_csv['best_route'].apply(literal_eval).item(),
        data_csv['cost'].item(),
        data_csv['elementary'].item(),
        data_csv['delta1'].item(),
        data_csv['time'].item(),
        data_csv['all_ext'].item(),
        data_csv['followed_ext'].item(),
        data_csv['ub_ext'].item(),
        data_csv['lut_ext'].item(),
        data_csv['lut_up_ext'].item(),
        data_csv['oob_ext'].item(),
        data_csv['feasible_solutions'].item()
    )
    return temp


# This function reads the test results of the ng-routing algorithm from multiple CSV files in the given path,
# and returns a list of lists containing NgResult objects.
def read_ng_test_data(path):
    path = path + "results/ng_test_result/"

    # Find all CSV files in the specified directory
    csv_files = glob.glob(os.path.join(path, "*.csv"))

    results = []
    for file in csv_files:
        data_csv = pd.read_csv(file)
        test_results = []

        # Iterate through each row in the CSV file and create an NgResult object
        for ind in data_csv.index:
            temp = NgResult(
                data_csv['best_route'].apply(literal_eval)[ind],
                data_csv['cost'][ind].item(),
                data_csv['elementary'][ind].item(),
                data_csv['delta1'][ind].item(),
                data_csv['time'][ind].item(),
                data_csv['all_ext'][ind].item(),
                data_csv['followed_ext'][ind].item(),
                data_csv['ub_ext'][ind].item(),
                data_csv['lut_ext'][ind].item(),
                data_csv['lut_up_ext'][ind].item(),
                data_csv['oob_ext'][ind].item(),
                data_csv['feasible_solutions'][ind].item()
            )
            test_results.append(temp)

        results.append(test_results)

    return results


# This function reads the results of the dynamic ng-routing algorithm from a CSV file in the given path,
# and returns a list of DngResult objects containing the results.
def read_dng_data(path):
    # Read the dng_result data from the CSV file
    data_csv = pd.read_csv(path + '/results/dng_result/dng_result.csv')

    results = []
    # Iterate through each row in the CSV file and create a DngResult object
    for ind in data_csv.index:
        temp = DngResult(
            data_csv["best_route"].apply(literal_eval)[ind],
            data_csv["cost"][ind].item(),
            data_csv["len_sub_tours"][ind].item(),
            data_csv["start_delta1"][ind].item(),
            data_csv["final_delta1"][ind].item(),
            data_csv["delta2"][ind].item(),
            data_csv["exceeded"][ind].item(),
            data_csv["elementary"][ind].item(),
            data_csv["dng_iterations"][ind].item(),
            data_csv["time"][ind].item(),
            data_csv['all_ext'][ind].item(),
            data_csv['followed_ext'][ind].item(),
            data_csv['ub_ext'][ind].item(),
            data_csv['lut_ext'][ind].item(),
            data_csv['lut_up_ext'][ind].item(),
            data_csv['oob_ext'][ind].item(),
            data_csv['feasible_solutions'][ind].item()
        )
        results.append(temp)

    return results


# This function reads the test results of the dynamic ng-routing algorithm from multiple CSV files in the given path,
# and returns a list of lists containing DngResult objects.
def read_dng_test_data(path):
    path = path + "results/dng_test_result/"

    # Find all CSV files in the specified directory
    csv_files = glob.glob(os.path.join(path, "*.csv"))

    results = []
    for file in csv_files:
        data_csv = pd.read_csv(file)
        test_results = []

        # Iterate through each row in the CSV file and create a DngResult object
        for ind in data_csv.index:
            temp = DngResult(
                data_csv["best_route"].apply(literal_eval)[ind],
                data_csv["cost"][ind].item(),
                data_csv["len_sub_tours"][ind].item(),
                data_csv["start_delta1"][ind].item(),
                data_csv["final_delta1"][ind].item(),
                data_csv["delta2"][ind].item(),
                data_csv["exceeded"][ind].item(),
                data_csv["elementary"][ind].item(),
                data_csv["dng_iterations"][ind].item(),
                data_csv["time"][ind].item(),
                data_csv['all_ext'][ind].item(),
                data_csv['followed_ext'][ind].item(),
                data_csv['ub_ext'][ind].item(),
                data_csv['lut_ext'][ind].item(),
                data_csv['lut_up_ext'][ind].item(),
                data_csv['aob_ext'][ind].item(),
                data_csv['feasible_solutions'][ind].item()
            )
            test_results.append(temp)

        results.append(test_results)

    return results


# This function calculates the n-sets (nearest neighbors) for each node in the given list of nodes,
# and returns a list of NodeWithNeighbors objects containing the nodes and their neighbors.
def calculate_n_sets(costsList, nodes, delta1):
    node_objects = []

    # Iterate through each node in the nodes list
    for node in nodes:
        # Create a NodeWithNeighbors object with the node's information and its delta1 nearest neighbors
        node_objects.append(
            NodeWithNeighbors(
                node.number, node.x, node.y,
                find_x_nearest_neighbours(costsList[node.number], delta1)
            )
        )

    return node_objects


# This function finds loops (sub-tours) in the given array and returns a list of loops.
# Each loop is a subsequence of the array that starts and ends with the same element.
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

            # Only add the loop if it is not the same as the entire array
            if len(loop) != len(arr):
                loops.append(loop)

        # Otherwise, store the current index in the dictionary.
        indices[elem] = i

    # Return the list of loops.
    return loops


# This function calculates the total costs of a given route using the provided costsList.
def calculate_route_costs(route, costsList):
    costs = 0

    # Iterate through the route, summing the costs between each consecutive pair of nodes.
    for i in range(len(route) - 1):
        costs += costsList[route[i]][route[i + 1]]

    # Return the total costs rounded to two decimal places.
    return round(costs, 2)


# This function calculates the total costs of a given route using the provided costsList,
# with a decreasing multiplier penalty (DMP) for each leg of the route.
def calculate_route_costs_dmp(route, costsList):
    costs = 0
    n = len(route) - 1
    k = 0

    # Iterate through the route, summing the costs between each consecutive pair of nodes,
    # while applying a decreasing multiplier penalty.
    for i in range(len(route) - 1):
        k += 1
        costs += (n - k + 1) * costsList[route[i]][route[i + 1]]

    # Return the total costs with the DMP applied.
    return costs


# This function prints the exceeded Delta 2 information along with the best route and its cost.
def print_exceeded(best_route, cost):
    print('')
    print('Delta 2 exceeded')
    print('best_route:')
    print(best_route)
    print('Costs :', str(cost))


# This function saves the results of a DNG algorithm to a CSV file.
def save_dng_results(path, results):
    # Define the filename for the output CSV file.
    filename = 'dng_result.csv'
    # Update the path to include the 'results' subdirectory.
    path = path + 'results/dng_result'

    # Check if the directory exists; if not, create it.
    if not os.path.isdir(path):
        os.makedirs(path)

    # Open the CSV file in write mode and create a CSV writer object.
    with open(path + '/' + filename + '', 'w') as f:
        write = csv.writer(f)

        # Define the header row for the CSV file.
        fields = ['best_route', 'cost', 'len_sub_tours', 'start_delta1', 'final_delta1', 'delta2', 'exceeded',
                  'elementary', 'dng_iterations', 'time', 'all_ext', 'followed_ext', 'ub_ext', 'lut_ext', 'lut_up_ext',
                  'oob_ext', 'feasible_solutions']
        # Write the header row to the CSV file.
        write.writerow(fields)

        # Iterate through the results and write each result as a row in the CSV file.
        for result in results:
            write.writerow(
                [result.best_route, result.cost, result.len_sub_tours, result.start_delta1,
                 result.final_delta1, result.delta2, result.exceeded, result.elementary,
                 result.dng_iterations, result.time, result.all_ext, result.followed_ext, result.ub_ext, result.lut_ext,
                 result.lut_up_ext, result.oob_ext, result.feasible_solutions])


# This function saves the test results of a DNG algorithm to a CSV file with a unique number identifier.
def save_dng_test_results(path, results, number):
    # Update the path to include the 'results' subdirectory.
    path = path + 'results/dng_test_result'
    # Define the base filename for the output CSV file.
    filename = 'dng_test_result_'

    # Check if the directory exists; if not, create it.
    if not os.path.isdir(path):
        os.makedirs(path)

    # Open the CSV file with the unique number identifier in write mode and create a CSV writer object.
    with open(path + '/' + filename + number + '.csv', 'w') as f:
        write = csv.writer(f)

        # Define the header row for the CSV file.
        fields = ['best_route', 'cost', 'len_sub_tours', 'start_delta1', 'final_delta1', 'delta2', 'exceeded',
                  'elementary', 'dng_iterations', 'time', 'all_ext', 'followed_ext', 'ub_ext', 'lut_ext', 'lut_up_ext',
                  'oob_ext', 'feasible_solutions']
        # Write the header row to the CSV file.
        write.writerow(fields)

        # Iterate through the results and write each result as a row in the CSV file.
        for result in results:
            write.writerow(
                [result.best_route, result.cost, result.len_sub_tours, result.start_delta1,
                 result.final_delta1, result.delta2, result.exceeded, result.elementary,
                 result.dng_iterations, result.time, result.all_ext, result.followed_ext, result.ub_ext, result.lut_ext,
                 result.lut_up_ext, result.oob_ext, result.feasible_solutions])


# This function saves the results of an NG algorithm to a CSV file.
def save_ng_result(path, result):
    # Set output CSV file name and update the path.
    filename = 'ng_result.csv'
    path = path + 'results/ng_result'

    # Create the directory if it doesn't exist.
    if not os.path.isdir(path):
        os.makedirs(path)

    # Open the CSV file in write mode.
    with open(path + '/' + filename + '', 'w') as f:
        write = csv.writer(f)

        # Define the header row and write it to the file.
        fields = ['best_route', 'cost', 'elementary', 'delta1', 'time', "all_ext", "followed_ext", "ub_ext", "lut_ext",
                  "lut_up_ext", "oob_ext", 'feasible_solutions']
        write.writerow(fields)

        # Write the result as a row in the CSV file.
        write.writerow(
            [result.best_route, result.cost, result.elementary, result.delta1, result.time, result.all_ext,
             result.followed_ext, result.ub_ext, result.lut_ext, result.lut_up_ext, result.oob_ext,
             result.feasible_solutions])


# This function saves the test results of an NG algorithm to a CSV file with a unique number identifier.
def save_ng_test_results(path, results, number):
    # Update the path and set output CSV file name.
    path = path + 'results/ng_test_result'
    filename = 'ng_test_result_'

    # Create the directory if it doesn't exist.
    if not os.path.isdir(path):
        os.makedirs(path)

    # Open the CSV file with the unique number identifier in write mode.
    with open(path + '/' + filename + number + '.csv', 'w') as f:
        write = csv.writer(f)

        # Define the header row and write it to the file.
        fields = ['best_route', 'cost', 'elementary', 'delta1', 'time', "all_ext", "followed_ext", "ub_ext", "lut_ext",
                  "lut_up_ext", 'aob_ext', 'feasible_solutions']
        write.writerow(fields)

        # Iterate through the results and write each result as a row in the CSV file.
        for result in results:
            write.writerow(
                [result.best_route, result.cost, result.elementary, result.delta1, result.time, result.all_ext,
                 result.followed_ext, result.ub_ext, result.lut_ext, result.lut_up_ext, result.oob_ext,
                 result.feasible_solutions])


# This function groups data from a list of DNG algorithm results according to a specified sort option.
def group_data_by(to_group, sort_option):
    # Check the sort option and group the data accordingly.
    if sort_option == SortOption.delta2:
        max_delta2 = max(item.delta2 for item in to_group)
        return_list = []
        for k in range(0, max_delta2):
            return_list.append([])
            for item in to_group:
                if k + 1 == item.delta2:
                    return_list[k].append(item)
        return return_list

    elif sort_option == SortOption.start_delta1:
        max_start_delta1 = max(item.start_delta1 for item in to_group)
        return_list = []
        for k in range(0, max_start_delta1):
            return_list.append([])
            for item in to_group:
                if k + 1 == item.start_delta1:
                    return_list[k].append(item)
        return return_list

    elif sort_option == SortOption.final_delta1:
        max_final_delta1 = max(item.final_delta1 for item in to_group)
        return_list = []
        for k in range(0, max_final_delta1):
            return_list.append([])
            for item in to_group:
                if k + 1 == item.final_delta1:
                    return_list[k].append(item)
        return return_list

    elif sort_option == SortOption.elementary:
        elem = []
        not_elem = []
        for item in to_group:
            if item.elementary:
                elem.append(item)
            else:
                not_elem.append(item)
        return elem, not_elem

    elif sort_option == SortOption.exceeded:
        elem = []
        not_elem = []
        for item in to_group:
            if item.exceeded:
                elem.append(item)
            else:
                not_elem.append(item)
        return elem, not_elem
