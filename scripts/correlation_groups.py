import os
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

from treeshapy.treeshapy import INDICES

INDICES.remove("furnas_rank")
INDICES.remove("treeness")
INDICES.remove("stemminess")
INDICES.remove("colijn_plazotta_rank")


base_dir = "../data/general_output"
threshold = 0.9
#corr_type = "database"
#corr_type = "rerooting"
corr_type = "vc"

groups_dir = os.path.join(base_dir, "groups")
if not os.path.isdir(groups_dir):
    os.makedirs(groups_dir)
repr_path = os.path.join(groups_dir, corr_type + "_repr_" + str(int(threshold * 100)) + ".txt")
groups_path = os.path.join(groups_dir, corr_type + "_groups_" + str(int(threshold * 100)) + ".txt")

for p in repr_path, groups_path:
    with open(p, "w+") as f:
        f.write("")

G = nx.Graph()
G.add_nodes_from(INDICES)

heatmap = {}

df = pd.read_csv(os.path.join("../data/general_output/", corr_type + "_correlations.tsv"), sep = "\t")
for i, index1 in enumerate(INDICES):
    heatmap[index1] = {}
    for j, index2 in enumerate(INDICES):
        corr = df[df["index1"] == index1].iloc[0][index2]
        heatmap[index1][index2] = corr
        if j > i and corr >= threshold:
            G.add_edge(index1, index2)


fig = plt.figure()
#nx.draw(G, ax=fig.add_subplot(), node_size = 10)
#fig.savefig(os.path.join(plots_dir, corr_type + "_correlations_" + str(int(threshold * 100)) + ".png"))
components = nx.connected_components(G)

for C in components:

    # select index with largest total correlation as representative
    total_corrs = {}
    for index1 in C:
        total_corrs[index1] = 0
        for index2 in INDICES:
            total_corrs[index1] += heatmap[index1][index2]
    selected_index = max(total_corrs, key=total_corrs.get)

    # determine average inner correlation
    inner_corr = 0
    missing = 0
    for i, index1 in enumerate(C):
        for j, index2 in enumerate(C):
            if j <= i:
                continue
            corr = heatmap[index1][index2]
            if corr < threshold:
                missing += 1
            inner_corr += heatmap[index1][index2]
    if len(C) > 1:
        inner_corr /= (len(C) * (len(C) - 1)) / 2
    for p in repr_path, groups_path:
        with open(p, "a") as f:
            f.write(selected_index + "\n")
    for index in C:
        if index == selected_index:
            continue
        with open(groups_path, "a") as f:
            f.write(index + "\n")



    #print(C)
    #print("Representative:", selected_index)
    #print("Average inner Correlation:", str(inner_corr))
    #print("Pairwise correlations below threshold:", str(missing))


