import networkx as nx
import matplotlib.pyplot as plt

# with open("input_test.txt") as f:
with open("input.txt") as f:
    edges = [tuple(line.strip().split("-")) for line in f.readlines()]

nodes = set()
for a, b in edges:
    nodes.add(a)
    nodes.add(b)

graph = nx.Graph()
graph.add_nodes_from(nodes)
graph.add_edges_from(edges)


triangles = [triangle for triangle in nx.enumerate_all_cliques(graph) if len(triangle) == 3]
count = 0
for triangle in triangles:
    contains_t = False
    for pc in triangle:
        if pc[0] == 't':
            contains_t = True
    if contains_t: count += 1
print("There are", count, "sets of three inter-connected computers that contain a computer that name starts with 't'.")

largest_party = sorted(max(nx.enumerate_all_cliques(graph), key=len))
password = ",".join(largest_party)
print(f"Password to largest party is: {password}")

# options = {
#     'node_color': 'black',
#     'node_size': 3,
#     'width': 0.2,
# }
# nx.draw(graph, **options)
# plt.show()