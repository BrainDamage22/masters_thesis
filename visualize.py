import networkx as nx
import matplotlib.pyplot as plt
import os


# This function visualizes a route and saves a PNG image of the visualization to a specified file path.
def visualize_route(nodes, route, costs, save, save_title, graph_number, path):
    # Create an empty networkx graph and set the plot title.
    graph = nx.Graph()
    ax = plt.gca()
    title = "Costs: " + str(costs)
    ax.set_title(title)

    # Add the nodes to the graph.
    for node in nodes:
        graph.add_node(node.number, pos=(node.x, node.y))

    # Add the edges to the graph.
    for i in range(0, len(route)-1):
        graph.add_edge(route[i], route[i+1])

    # Get the node positions and draw the graph.
    pos = nx.get_node_attributes(graph, 'pos')
    nx.draw_networkx_labels(graph, pos=pos)
    nx.draw(graph, pos, ax=ax)
    _ = ax.axis('off')

    # If save is True, save the plot as a PNG image to the specified file path.
    if save:
        path = path + "export/"
        if not os.path.isdir(path):
            os.makedirs(path)

        if graph_number == 0:
            graph_number = ""
        else:
            graph_number = "_" + str(graph_number).zfill(3)

        plt.savefig(path + "/" + save_title + graph_number + ".png", format="PNG")


# This function visualizes the nodes of a graph.
def visualize_nodes(nodes):
    # Create a networkx graph and add the nodes to it.
    graph = nx.Graph()
    for node in nodes:
        graph.add_node(node.number, pos=(node.x, node.y))

    # Get the node positions and draw the graph.
    pos = nx.get_node_attributes(graph, 'pos')
    nx.draw_networkx_labels(graph, pos=pos)
    nx.draw(graph, pos)
