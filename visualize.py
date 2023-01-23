import networkx as nx
import matplotlib.pyplot as plt
import os


def visualize_route(nodes, route, costs, save, save_title, graph_number, path):
    graph = nx.Graph()

    ax = plt.gca()
    title = "Costs: " + str(costs) + " Route: " + str(route)
    ax.set_title(title)

    for node in nodes:
        graph.add_node(node.number, pos=(node.x, node.y))

    for i in range(0, len(route)-1):
        graph.add_edge(route[i], route[i+1])

    pos = nx.get_node_attributes(graph, 'pos')
    nx.draw_networkx_labels(graph, pos=pos)
    nx.draw(graph, pos, ax=ax)
    _ = ax.axis('off')

    if save:
        path = path + "export/"
        if not os.path.isdir(path):
            os.makedirs(path)

        if graph_number == 0:
            graph_number = ""
        else:
            graph_number = "_" + str(graph_number).zfill(3)

        plt.savefig(path + "/" + save_title + graph_number + ".png", format="PNG")


def visualize_nodes(nodes):
    graph = nx.Graph()

    for node in nodes:
        graph.add_node(node.number, pos=(node.x, node.y))

    pos = nx.get_node_attributes(graph, 'pos')
    nx.draw_networkx_labels(graph, pos=pos)
    nx.draw(graph, pos)



