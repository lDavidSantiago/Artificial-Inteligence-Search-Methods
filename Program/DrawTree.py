import matplotlib.pyplot as plt
import networkx as nx
import pydot
from networkx.drawing.nx_pydot import graphviz_layout

def draw_tree(tupla, coord_to_check, current_search_method):
    G = nx.DiGraph()
    node_costs = {}
    edges = [(parent, child) for parent, child, cost in tupla]
    G.add_edges_from(edges)

    for parent, child, cost in tupla:
        node_costs[child] = cost

    levels = nx.single_source_shortest_path_length(G, tupla[0][0])
    pos = graphviz_layout(G, prog="dot")
    plt.clf()

    node_labels = {}
    node_colors = []
    for node in G.nodes:
        if node == coord_to_check:
            node_colors.append('red')
        else:
            node_colors.append('lightblue')
        cost = node_costs.get(node, 0)
        
        # Move label assignment outside if statement
        if current_search_method == "Greedy":
            node_labels[node] = f"{node}\nNivel {levels[node]}\nHeuristica {cost}"
        else:
            node_labels[node] = f"{node}\nNivel {levels[node]}\nCosto {cost}"

    plt.title(current_search_method)
    nx.draw(G, pos, with_labels=True, labels=node_labels, node_color=node_colors, node_size=600)
    plt.show()
    plt.pause(.7)