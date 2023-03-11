def ng_routing_lookup_elementary_k(starting_node, nodes, costs_list, lower_bound):

    def retrace_optimal_path(buffer):

        full_path_buffer = dict((k, v) for k, v in buffer.items() if k[2] == n)

        path_key = min(full_path_buffer.keys(), key=lambda x: full_path_buffer[x][0])
        curr_node = path_key[0]
        optimal_cost, prev_node, ng_set_i = buffer[path_key]

        optimal_path = [curr_node, starting_node]
        k = n

        while prev_node is not None:
            curr_node = prev_node
            k -= 1
            path_key = (curr_node, ng_set_i, k)
            _, prev_node, ng_set_i = buffer[path_key]

            optimal_path = [curr_node] + optimal_path
        return optimal_path, optimal_cost

    all_dp_routes = {}
    node_objects = {node.number: node for node in nodes}
    n = len(node_objects)
    all_nodes = frozenset(list(node_objects.keys()))
    all_nodes = frozenset(all_nodes) - frozenset([starting_node])
    ng_set_i = frozenset()
    k = 1
    state = (starting_node, ng_set_i, k)
    all_dp_routes[state] = (0, None, frozenset())
    queue = [state]

    while queue:
        current_node, ng_set_i, k = queue.pop(0)
        prev_cost, _, _ = all_dp_routes[(current_node, ng_set_i, k)]
        node_object = nodes[current_node]

        neighbours = frozenset(node_object.neighbors)
        ng_set_j = frozenset.intersection(ng_set_i, neighbours)
        ng_set_j = frozenset().union(ng_set_j, frozenset([current_node]))
        k += 1

        to_visit = all_nodes - ng_set_j
        for new_curr_node in to_visit:
            new_cost = round((prev_cost + costs_list[current_node][new_curr_node]), 3)

            if (new_curr_node, ng_set_j, k) not in all_dp_routes:
                all_dp_routes[(new_curr_node, ng_set_j, k)] = (new_cost, current_node, ng_set_i)
                queue += [(new_curr_node, ng_set_j, k)]
            elif new_cost < all_dp_routes[(new_curr_node, ng_set_j, k)][0]:
                all_dp_routes[(new_curr_node, ng_set_j, k)] = (new_cost, current_node, ng_set_i)

    full_path_buffer = dict((k, v) for k, v in all_dp_routes.items() if k[2] == n)

    for key in full_path_buffer.keys():
        cost, prev_node, ng_set_i = all_dp_routes[key]
        new_cost = cost + costs_list[key[0]][starting_node]
        all_dp_routes[key] = (new_cost, prev_node, ng_set_i)

    return retrace_optimal_path(all_dp_routes)


def ng_routing_iteration_exp(starting_node, nodeObjects, costsList):
    start = time.time()
    possibilities = 0

    all_ng_routes = {}
    node_objects = {node.number: node for node in nodeObjects}
    all_nodes = list(node_objects.keys())
    all_nodes.remove(starting_node)
    ng_set_i = frozenset()
    n = len(node_objects)
    stack = [(starting_node, ng_set_i, [], 0.0)]

    while stack:
        possibilities += 1
        node, ng_set_i, visited, costs = stack.pop()
        node_object = node_objects[node]

        neighbours = frozenset(node_object.neighbors)
        ng_set_j = frozenset.intersection(ng_set_i, neighbours)
        ng_set_j = frozenset().union(ng_set_j, frozenset([node]))

        visited.append(node)
        to_visit = [node for node in all_nodes if node not in ng_set_j]

        if len(visited) == n:
            new_cost = costs + costsList[visited[len(visited) - 1]][starting_node]
            visited.append(starting_node)
            all_ng_routes[new_cost] = visited
            continue

        for node in to_visit:
            new_cost = costs + costsList[visited[len(visited) - 1]][node]
            stack += [(node, ng_set_j, visited.copy(), new_cost)]

    else:
        cost = min(all_ng_routes.keys())
        best_route = all_ng_routes[cost]
        loops = find_loops(best_route)
        cardinality = len(all_ng_routes)

        elementary = False
        if len(loops) == 0:
            elementary = True

        end = time.time()
        return NgResult(best_route, cost, elementary, len(nodeObjects[0].neighbors), cardinality,
                        round(end - start, 3), possibilities)


def ng_routing_iteration_old(starting_node, nodeObjects, costsList):
    start = time.time()
    possibilities = 0

    all_ng_routes = {}
    node_objects = {node.number: node for node in nodeObjects}
    all_nodes = list(node_objects.keys())
    all_nodes.remove(starting_node)
    ng_set_i = set()
    n = len(node_objects)
    stack = [(starting_node, ng_set_i, [])]

    while stack:
        possibilities += 1
        node, ng_set_i, visited = stack.pop()
        node_object = node_objects[node]
        neighbours = set(node_object.neighbors)

        ng_set_j = list(set(ng_set_i) & neighbours)
        ng_set_j.append(node)
        ng_set_j = list(set(ng_set_j))

        visited.append(node)
        to_visit = [node for node in all_nodes if node not in ng_set_j]

        if len(visited) == n:
            visited.append(starting_node)
            costs = calculate_route_costs(visited, costsList)
            all_ng_routes[costs] = visited
            continue

        stack.extend((node, ng_set_j, visited.copy()) for node in to_visit)

    else:
        cost = min(all_ng_routes.keys())
        best_route = all_ng_routes[cost]
        loops = find_loops(best_route)
        elementary = False
        cardinality = len(all_ng_routes)

        if len(loops) == 0:
            elementary = True

        end = time.time()
        return NgResult(best_route, cost, elementary, len(nodeObjects[0].neighbors), cardinality,
                        round(end - start, 3), possibilities)


