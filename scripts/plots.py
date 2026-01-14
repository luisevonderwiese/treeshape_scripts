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

IMBALANCE = [
        "variance_of_leaves_depths",
        
        "maximum_depth",
        "average_leaf_depth",
        "average_vertex_depth",
        
        "colless_index",
        "sackin_index",
        "total_path_length",
        "total_internal_path_length",
        "s_shape",
        "rogers_j_index",
        "symmetry_nodes_index",
        "total_I",
        "total_I_prime",
        "total_I_w",
        "total_cophenetic_index",
        "quadratic_colless_index",

        "mean_I",
        "mean_I_prime",
        "mean_I_w",
        "I_2_index",
        "stairs1",

        "corrected_colless_index",

        #"colijn_plazotta_rank"
        ]

BALANCE = [
        "B_1_index",
        "B_2_index",
        "maximum_width",
        "modified_maxdiff_widths",
        "max_width_over_max_depth",
        "rooted_quartet_index",
        "stairs2",
        "furnas_rank"
        ]





def plot_tree_sizes(base_dirs):
    for base_dir in base_dirs:
        sizes = pd.read_csv(os.path.join(base_dir, "tree_sizes.tsv"), sep = "\t")["num_tips"] 
        plots_dir = os.path.join(base_dir, "plots")
        if not os.path.isdir(plots_dir):
            os.makedirs(plots_dir)

        hist, bins, _ = plt.hist(sizes, bins=30)
        logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
        plt.clf()
        plt.hist(sizes, bins=logbins)
        plt.xscale("log")
        plt.savefig(os.path.join(plots_dir, "tree_sizes.png"))
        plt.clf()


def plot_variances(base_dirs, selected_indices, suffix = "", colors = None, labels = None):
    plots_dir = "../data/general_plots/stats"
    if not os.path.isdir(plots_dir):
        os.makedirs(plots_dir)

    modes = ["kurtosis"]

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
    plots_dir = "../data/general_plots/correlations"
    if not os.path.isdir(plots_dir):
        os.makedirs(plots_dir)

    df = pd.read_csv(os.path.join("../data/general_output/", corr_type + "_correlations.tsv"), sep = "\t")
    heatmap = []
    for i, index1 in enumerate(index_list):
        heatmap.append([])
        for j, index2 in enumerate(index_list):
            corr = df[df["index1"] == index1].iloc[0][index2]
            heatmap[i].append(corr)

    fig, ax = plt.subplots(figsize=(15, 15))
    im = ax.imshow(heatmap)
    fig.colorbar(im)
    ax.set_xticks(range(len(index_list)), labels=index_list, rotation=45, ha="right", rotation_mode="anchor")
    ax.set_yticks(range(len(index_list)), labels=index_list)
    plt.savefig(os.path.join(plots_dir, corr_type + "_heatmap_" + list_name + ".png"))
    plt.clf()


def plot_against_size(base_dirs, selected_indices, stat, suffix = ""):
    plots_dir = "../data/general_plots/" + stat + "_size"
    if not os.path.isdir(plots_dir):
        os.makedirs(plots_dir)

    df = pd.read_csv(os.path.join("../data/general_output/" + stat + ".tsv"), sep = "\t")
    sizes = list(set(df["size"]))
    sizes.sort()
    plt.figure(figsize=(20, 10))
    for index in selected_indices:
        avg_stat = [np.mean(df[df["size"] == size][index]) for size in sizes]
        plt.scatter(sizes, avg_stat, label = index, s = 10)
        plt.plot(sizes, avg_stat)
    plt.legend(loc = "upper left")
    plt.xlabel("tree size n")
    plt.ylabel(stat)
    #plt.yscale("log")
    plt.savefig(os.path.join(plots_dir, "size_" + stat + suffix + ".png"))
    plt.clf()


def plot_size_correlations(selected_indices, mode, suffix = ""):
    plots_dir = "../data/general_plots/size_correlations"
    if not os.path.isdir(plots_dir):
        os.makedirs(plots_dir)
    df = pd.read_csv("../data/general_output/all_results_" + mode + ".tsv", sep = "\t")
    sizes = list(set(df["tree_size"]))
    sizes.sort()
    plt.figure(figsize=(20, 10))
    for index in selected_indices:
        if np.isnan(df[index]).all():
            continue
        avg_values = [np.mean(df[df["tree_size"] == size][index]) for size in sizes]
        plt.scatter(sizes, avg_values, label = index, s = 10)
        plt.plot(sizes, avg_values)
    plt.legend(loc = "upper left")
    plt.xlabel("tree size n")
    plt.ylabel("index values")
    #plt.yscale("log")
    plt.savefig(os.path.join(plots_dir, mode + suffix + ".png"))
    plt.clf()

INDICES.remove("furnas_rank")
INDICES.remove("treeness")
INDICES.remove("stemminess")

base_dirs = ["../data/evonaps_dna"]

#plot_tree_sizes(base_dirs)

##plot_correlations(base_dirs, "database", "groups_90") # grouping method deprecated, ignores index types
##plot_correlations(base_dirs, "database", "repr_90")
##plot_correlations(base_dirs, "rerooting", "groups_95") # grouping method deprecated
##plot_correlations(base_dirs, "rerooting", "repr_95")


#plot_correlations(base_dirs, "database", "types")
#plot_correlations(base_dirs, "rerooting", "types")



experiment_groups = [[
"total_I",
"total_I_w",
"total_I_prime",
    "mean_I",
"mean_I_w",
"mean_I_prime"],

["average_leaf_depth",
"average_vertex_depth",
 "total_path_length",
"total_internal_path_length",
"variance_of_leaves_depths",
"sackin_index",
  "s_shape"
 ],

["d_index",
    "colless_index",
  "corrected_colless_index",
    "total_cophenetic_index",
"quadratic_colless_index"],

["cherry_index",
"modified_cherry_index",
"IL_number",
"pitchforks",
"four_caterpillars",
"double_cherries"],

["rooted_quartet_index",
 "B_2_index",
 "B_1_index",
 "I_2_index",
 "maximum_depth",
 "stairs2",
 "j1"],

["stairs1",
    "rogers_j_index",
"symmetry_nodes_index",
"maximum_width",
 "max_width_over_max_depth"],

["maxdiff_widths",
"modified_maxdiff_widths",
    "diameter",
"average_ladder",
"ladder_length"],

["area_per_pair_index",
    "wiener_index",
 "total_farness",
"mean_bcent",
"maximum_closeness",
"minimum_farness",
"maximum_farness",
"minimum_bcent",
"maximum_bcent",
  "bcent_variance",
],

["root_imbalance",
"bcent_root",
"I_root"]
]

for k, sublist in enumerate(experiment_groups):
    print(k)
    #plot_variances(base_dirs, sublist, "_" + str(k))
    #plot_against_size(base_dirs, sublist, stat = "kurtosis", suffix = "_" + str(k)) 
    #plot_size_correlations(sublist, suffix = "_" + str(k))



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

index_types_values = {"node_indices":[
          "corrected_colless_index",
          "I_2_index",
          "stairs2",
          "j1",
          "stairs1"],
"node_indices4":[
          "rogers_j_index",
          "symmetry_nodes_index"],
"node_indices2": ["quadratic_colless_index"],
"node_indices3": ["colless_index"],
"I_based_indices":["mean_I",
          "mean_I_prime",
          "mean_I_w"],
"I_based_indices2":["total_I",
          "total_I_prime",
          "total_I_w"],
"depth_indices": ["sackin_index",
          "total_path_length",
          "total_internal_path_length"],
"depth_indices_2":[
          "s_shape",
          "variance_of_leaves_depths",
          "B_1_index"],
"depth_indices_3":[
          "average_leaf_depth",
          "average_vertex_depth",
          "maximum_depth",
          "B_2_index" ],
"width_indices" : ["maximum_width",
          "maxdiff_widths",
          "modified_maxdiff_widths",
          "max_width_over_max_depth"],
"structure_indices" : [
          "d_index",
          "ladder_length",
          "average_ladder",
          ],
"structure_indices2": ["rooted_quartet_index"],
"subgraph_indices": ["cherry_index",
          "modified_cherry_index",
          "IL_number",
          "pitchforks",
          "four_caterpillars",
          "double_cherries"],
"distance_indices" : ["total_cophenetic_index"],
"distance_indices2":["diameter",
          "area_per_pair_index"],
"network_indices": ["wiener_index",
          "total_farness"],
"network_indices2": ["maximum_bcent"],
"network_indices3":["mean_bcent",
          "bcent_root",
          "maximum_farness",
          "minimum_farness"],
"network_indices4" : ["minimum_bcent",
          "maximum_closeness"],
"network_indices5": ["bcent_variance"],
"root_indices": ["root_imbalance",
          "I_root"],
#"ranking_indices" : ["colijn_plazotta_rank",
#          "furnas_rank"]
}

index_types_max = {"node_indices":["colless_index",
          "corrected_colless_index",
          "quadratic_colless_index"],
"node_indices2":["stairs1",
          "rogers_j_index",
          "symmetry_nodes_index"],
"depth_indices": ["sackin_index",
          "total_path_length",
          "total_internal_path_length",
          "average_leaf_depth",
          "average_vertex_depth",
          "maximum_depth",
          "B_2_index" ],
"subgraph_indices": ["cherry_index",
          "modified_cherry_index"],
"distance_indices" : ["total_cophenetic_index"],
"root_indices": ["root_imbalance",
          "I_root"],
}

index_types_yule = {"node_indices":["colless_index"],
                    "node_indices2": ["corrected_colless_index"],
"depth_indices": ["sackin_index"],
"depth_indices2" : ["average_leaf_depth",
          "variance_of_leaves_depths"],
"depth_indices3" : ["B_2_index"],
"structure_indices": ["rooted_quartet_index"],
"subgraph_indices": ["cherry_index"],
"mixed_indices" : ["total_cophenetic_index",
                      "quadratic_colless_index"],
"distance_indices": ["area_per_pair_index"],
}

#for i, (index_type, indices) in enumerate(index_types_max.items()):
#    plot_size_correlations(indices, "relative_max", suffix = "_" + index_type)

for i, (index_type, indices) in enumerate(index_types_yule.items()):
    plot_size_correlations(indices, "relative_yule", suffix = "_" + index_type)

assert(False)

for i, (index_type, indices) in enumerate(index_types_values.items()):
    plot_size_correlations(indices, "absolute", suffix = "_" + index_type)
    plot_size_correlations(indices, "relative_tips", suffix = "_" + index_type)


all_indices = []
colors = []
labels = []

for i, (index_type, indices) in enumerate(index_types.items()):
    all_indices += indices
    colors += len(indices) * [i]
    labels += len(indices) * [index_type]
    plot_against_size(base_dirs, indices, stat = "kurtosis", suffix = "_" + index_type)

plot_against_size(base_dirs, ["d_index", "rooted_quartet_index", "average_ladder"], stat = "kurtosis", suffix = "_structure2_indices")

plot_variances(base_dirs, all_indices, "_all", colors, labels)
