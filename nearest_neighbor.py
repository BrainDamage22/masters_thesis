# This function finds the indices of the 'amount' smallest values in the input array.
# It returns a list of indices corresponding to the 'amount' nearest neighbors.
def find_x_nearest_neighbours(arr, amount):
    # Sort the input array in ascending order
    sorted_arr = sorted(arr)

    # Find the indices of the 'amount' smallest values in the original array
    lowest_indices = [i for i, val in enumerate(arr) if val in sorted_arr[0:amount]]

    return lowest_indices


# This function finds a route using the nearest neighbor heuristic. It starts from a
# given node and iteratively adds the nearest unvisited node to the route until all
# nodes have been visited.
def find_nearest_neighbours_path(nodes, costsList, startingNode):
    visited = [startingNode]  # Initialize the visited nodes list with the starting node
    current_node_number = startingNode
    not_visited = list(range(0, len(nodes)))  # Create a list of unvisited nodes

    while True:
        not_visited.remove(current_node_number)  # Remove the current node from the unvisited nodes list

        # Break the loop when all nodes have been visited
        if len(not_visited) == 0:
            visited.append(startingNode)  # Add the starting node to close the loop
            return visited

        possible_destinations = {"Number": [], "Cost": []}
        current_node_costs = costsList[current_node_number]

        # Calculate costs to unvisited nodes from the current node
        for node in not_visited:
            possible_destinations["Number"].append(node)
            possible_destinations["Cost"].append(current_node_costs[node])

        # Find the minimum cost and its index
        min_costs = min(possible_destinations["Cost"])
        min_cost_index = possible_destinations["Cost"].index(min_costs)

        # Update the current node to the nearest unvisited node
        current_node_number = possible_destinations["Number"][min_cost_index]
        visited.append(current_node_number)  # Add the new current node to the visited nodes list

