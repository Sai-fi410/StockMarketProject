import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load Correlation Matrix

corr = pd.read_csv("data/correlation_matrix.csv", index_col=0)

# Create Graph

G = nx.Graph()

# Add nodes
for stock in corr.columns:
    G.add_node(stock)

import numpy as np

# Convert correlation to distance
distance_matrix = np.sqrt(2 * (1 - corr))

# Create weighted graph from distance matrix
G_full = nx.Graph()

for i in range(len(distance_matrix.columns)):
    for j in range(i + 1, len(distance_matrix.columns)):
        stock1 = distance_matrix.columns[i]
        stock2 = distance_matrix.columns[j]
        weight = distance_matrix.iloc[i, j]
        G_full.add_edge(stock1, stock2, weight=weight)

# Build Minimum Spanning Tree
G = nx.minimum_spanning_tree(G_full, weight='weight')

from networkx.algorithms import community

# Detect Communities
communities = community.greedy_modularity_communities(G, weight='weight')

print("\nDetected Communities:")
for i, comm in enumerate(communities):
    print(f"Community {i+1}: {list(comm)}")

# Assign community index to each node
community_map = {}
for i, comm in enumerate(communities):
    for node in comm:
        community_map[node] = i

# Generate colors
import matplotlib.cm as cm
cmap = cm.get_cmap('tab20', len(communities))

node_colors = [cmap(community_map[node]) for node in G.nodes()]

# Centralities
degree_centrality = nx.degree_centrality(G)
eigen_centrality = nx.eigenvector_centrality(G, max_iter=1000)

print("\nDegree Centrality:")
for stock, value in sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True):
    print(stock, round(value, 3))

print("\nEigenvector Centrality:")
for stock, value in sorted(eigen_centrality.items(), key=lambda x: x[1], reverse=True):
    print(stock, round(value, 3))

# Select top 10 influential stocks
top_nodes = sorted(eigen_centrality, key=eigen_centrality.get, reverse=True)[:10]

labels = {}
for node in G.nodes():
    if node in top_nodes:
        labels[node] = node
    else:
        labels[node] = ""

# Draw Graph

plt.figure(figsize=(14, 12))

pos = nx.spring_layout(G, k=0.3, iterations=100, seed=42)

edges = G.edges()
weights = [abs(G[u][v]['weight']) * 3 for u, v in edges]

edge_colors = []
for u, v in edges:
    if G[u][v]['weight'] > 0:
        edge_colors.append("green")
    else:
        edge_colors.append("red")

node_sizes = [eigen_centrality[node] * 8000 for node in G.nodes()]

plt.figure(figsize=(14, 12))

# Community colors
community_map = {}
for i, comm in enumerate(communities):
    for node in comm:
        community_map[node] = i

import matplotlib.cm as cm
cmap = cm.get_cmap("tab20", len(communities))
node_colors = [cmap(community_map[node]) for node in G.nodes()]

# Node sizes from eigenvector centrality
node_sizes = [eigen_centrality[node] * 9000 for node in G.nodes()]

# Draw components separately for full control
nx.draw_networkx_edges(
    G,
    pos,
    width=[abs(w)*2 for w in weights],
    edge_color=edge_colors,
    alpha=0.6
)

nx.draw_networkx_nodes(
    G,
    pos,
    node_size=node_sizes,
    node_color=node_colors,
    edgecolors="black",
    linewidths=0.5
)

nx.draw_networkx_labels(
    G,
    pos,
    font_size=8
)

plt.title("Stock Correlation Network\nNode Size = Eigenvector Centrality", fontsize=14)
plt.axis("off")
plt.savefig("data/stock_network_final.png", dpi=300)
plt.show()

from networkx.algorithms import community