import os
import numpy as np
import pandas as pd
from tabulate import tabulate
from ete3 import Tree
import matplotlib.pyplot as plt
from collections import Counter
import seaborn

from treeshapy.treeshapy import TreeShape, INDICES
import util

def plot_tree_sizes(base_dirs):
    plots_dir = os.path.join("../data/plots")
    if not os.path.isdir(plots_dir):
        os.makedirs(plots_dir)
    for base_dir in base_dirs:
        sizes = pd.read_csv(os.path.join(base_dir, "tree_sizes.tsv"), sep = "\t")["num_tips"] 
        hist, bins, _ = plt.hist(sizes, bins=30)
        logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
        plt.clf()
        plt.hist(sizes, bins=logbins)
        plt.xscale("log")
        base_dir_name = base_dir.split(os.sep)[-1]
        plt.savefig(os.path.join(plots_dir, "tree_sizes_" + base_dir_name + ".png"))
        plt.clf()


def plot_stats(base_dirs, selected_indices, suffix = "", colors = None, labels = None):
    plots_dir = "../data/plots"
    if not os.path.isdir(plots_dir):
        os.makedirs(plots_dir)

    modes = ["kurtosis", "kurtosis_int", "kurtosis_ext"]

    if colors is not None:
        palette = seaborn.color_palette("husl", max(colors) + 1)
        colors = [palette[color] for color in colors]

    for mode in modes:
        df = pd.read_csv(os.path.join("../data/general_output/" + mode + ".tsv"), sep = "\t")
        data = []
        for index in selected_indices:
            data.append(df[index])
    
        plt.figure(figsize=(2 * len(selected_indices), 10))
        data = [[el for el in l if not (el is float("nan") or el is float("inf") or el is float("-inf"))] for l in data]
        ax = seaborn.violinplot(data = data, log_scale=True)
        if colors is not None:
            ax = seaborn.violinplot(data = data, palette = colors, log_scale=True)
        ax.set_ylim(0.8, 1100)
        ax.axhline(y=1, color='gray', linestyle='--')
        
        ax.set_xticklabels(selected_indices)
        plt.xticks(rotation=90)
        plt.xlabel("index")
        plt.ylabel(mode)
 
        plt.savefig(os.path.join(plots_dir, mode + suffix + ".png"), bbox_inches='tight')
        plt.clf()


def plot_correlations(base_dirs, corr_type, list_name):
    with open(os.path.join("../data/general_output/groups", corr_type + "_" + list_name + ".txt"), "r") as listfile:
        index_list = listfile.read().split("\n")[:-1]
    plots_dir = "../data/plots"
    if not os.path.isdir(plots_dir):
        os.makedirs(plots_dir)

    df = pd.read_csv(os.path.join("../data/general_output/", corr_type + "_correlations.tsv"), sep = "\t")
    heatmap = []
    for i, index1 in enumerate(index_list):
        heatmap.append([])
        for j, index2 in enumerate(index_list):
            if index1 == "" or index2 == "":
                corr = float("nan")
            else:
                corr = df[df["index1"] == index1].iloc[0][index2]
            heatmap[i].append(corr)

    fig, ax = plt.subplots(figsize=(15, 15))
    im = ax.imshow(heatmap)
    fig.colorbar(im)
    ax.set_xticks(range(len(index_list)), labels=index_list, rotation=45, ha="right", rotation_mode="anchor")
    ax.set_yticks(range(len(index_list)), labels=index_list)
    plt.savefig(os.path.join(plots_dir, corr_type + "_heatmap_" + list_name + ".png"))
    plt.clf()


INDICES.remove("furnas_rank")
INDICES.remove("treeness")
INDICES.remove("stemminess")

base_dirs = ["../data/evonaps_dna"]

plot_tree_sizes(base_dirs)
plot_correlations(base_dirs, "database", "types")
plot_correlations(base_dirs, "rerooting", "types")



index_types = {"node_indices":[
          "colless_index",
          "corrected_colless_index",
          "quadratic_colless_index",
          "I_2_index",
          "stairs2",
          "j1",
          "stairs1",
          "rogers_j_index",
          "symmetry_nodes_index"],
"I_based_indices":["mean_I",
          "total_I",
          "mean_I_prime",
          "total_I_prime",
          "mean_I_w",
          "total_I_w"],
"depth_indices": ["average_leaf_depth",
          "sackin_index",
          "total_path_length",
          "total_internal_path_length",
          "average_vertex_depth",
          "s_shape",
          "maximum_depth",
          "variance_of_leaves_depths",
          "B_1_index",
          "B_2_index" ],
"width_indices" : ["maximum_width",
          "maxdiff_widths",
          "modified_maxdiff_widths",
          "max_width_over_max_depth"],
"structure_indices" : [
          "d_index",
          "rooted_quartet_index",
          "ladder_length",
          "average_ladder",
          ],
"subgraph_indices": ["cherry_index",
          "modified_cherry_index",
          "IL_number",
          "pitchforks",
          "four_caterpillars",
          "double_cherries"],
"distance_indices" : ["total_cophenetic_index",
          "diameter",
          "area_per_pair_index"],
"network_indices": [          "wiener_index",
          "total_farness",
          "mean_bcent",
          "bcent_root",
          "maximum_farness",
          "minimum_bcent",
          "maximum_bcent",
          "bcent_variance",
          "maximum_closeness",
          "minimum_farness"],
"root_indices": ["root_imbalance",
          "I_root"],
#"ranking_indices" : ["colijn_plazotta_rank",
#          "furnas_rank"]
}



all_indices = []
colors = []
labels = []

for i, (index_type, indices) in enumerate(index_types.items()):
    all_indices += indices
    colors += len(indices) * [i]
    labels += len(indices) * [index_type]

plot_stats(base_dirs, all_indices, "_all", colors, labels)
