def find_x_nearest_neighbours(arr, amount):
    sorted_arr = sorted(arr)
    lowest_indices = [i for i, val in enumerate(arr) if val in sorted_arr[0:amount]]
    return lowest_indices


def find_nearest_neighbours_path(nodes, costsList, startingNode):
    costs = 0
    visited = [startingNode]
    route_of_costs = []
    current_node_number = startingNode
    not_visited = list(range(0, len(nodes)-1))

    while True:
        not_visited.remove(current_node_number)

        if len(not_visited) == 0:

            last_costs = costsList[current_node_number][startingNode]
            costs += last_costs
            route_of_costs.append(last_costs)
            visited.append(startingNode)

            print("Total costs: " + str(round(costs, 2)))
            print("Route:")
            print(visited)
            print("Costs:")
            print(route_of_costs)
            break

        possible_destinations = {"Number": [], "Cost": []}
        current_node_costs = costsList[current_node_number - 1]

        for node in not_visited:
            possible_destinations["Number"].append(node)
            possible_destinations["Cost"].append(current_node_costs[node - 1])

        min_costs = min(possible_destinations["Cost"])
        min_cost_index = possible_destinations["Cost"].index(min_costs)
        current_node_number = possible_destinations["Number"][min_cost_index]
        costs += min_costs
        visited.append(current_node_number)
        route_of_costs.append(min_costs)
