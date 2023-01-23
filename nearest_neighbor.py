def find_x_nearest_neighbours(arr, amount):
    sorted_arr = sorted(arr)
    lowest_indices = [i for i, val in enumerate(arr) if val in sorted_arr[0:amount]]
    return lowest_indices


def find_nearest_neighbours_path(nodes, costsList, startingNode):
    visited = [startingNode]
    current_node_number = startingNode
    not_visited = list(range(0, len(nodes)))

    while True:
        not_visited.remove(current_node_number)

        if len(not_visited) == 0:
            visited.append(startingNode)
            return visited

        possible_destinations = {"Number": [], "Cost": []}
        current_node_costs = costsList[current_node_number]

        for node in not_visited:
            possible_destinations["Number"].append(node)
            possible_destinations["Cost"].append(current_node_costs[node])

        min_costs = min(possible_destinations["Cost"])
        min_cost_index = possible_destinations["Cost"].index(min_costs)
        current_node_number = possible_destinations["Number"][min_cost_index]
        visited.append(current_node_number)
