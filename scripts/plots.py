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


def plot_variances(base_dirs, selected_indices, suffix = ""):
    plots_dir = "../data/general_plots/rooting_variances"
    if not os.path.isdir(plots_dir):
        os.makedirs(plots_dir)

    modes = ["kurtosis"]

    for mode in modes:
        df = pd.read_csv(os.path.join("../data/general_output/" + mode + ".tsv"), sep = "\t")
        data = []
        for index in selected_indices:
            data.append(df[index])
    
        plt.figure(figsize=(20, 10))
        ax = seaborn.stripplot(data = data, log_scale=True)
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


def plot_size_correlations(base_dirs):
    plots_dir = "../data/general_plots/"
    if not os.path.isdir(plots_dir):
        os.makedirs(plots_dir)


    for mode in ["absolute", "relative_max", "relative_yule", "relative_tips"]:
        df = pd.read_csv(os.path.join("../data/general_output/", "size_correlations_" + mode + ".tsv"), sep = "\t")
        df = df.sort_values('corr')
        plt.scatter(df["index"], df["corr"], label = mode)
    plt.legend()
    plt.xticks(rotation=45, ha='right')
    plt.savefig(os.path.join(plots_dir, "size_correlation.png"))
    plt.clf()


def plot_against_size(base_dirs, selected_indices, stat, suffix = ""):
    plots_dir = "../data/general_plots/"
    if not os.path.isdir(plots_dir):
        os.makedirs(plots_dir)

    df = pd.read_csv(os.path.join("../data/general_output/" + stat + ".tsv"), sep = "\t")
    plt.figure(figsize=(20, 10))
    for index in selected_indices:
        plt.scatter(df["size"], df[index], label = index, s = 10)
    plt.legend(loc = "upper left")
    plt.xlabel("tree size n")
    plt.ylabel("kurtosis")
    plt.yscale("log")
    plt.savefig(os.path.join(plots_dir, "size_" + stat + suffix + ".png"))
    plt.clf()



def plot_size_correlations(selected_indices, suffix = ""):
    plots_dir = "../data/general_plots"
    if not os.path.isdir(plots_dir):
        os.makedirs(plots_dir)
    for mode in ["absolute", "relative_max", "relative_yule", "relative_tips"]:
        data = []
        df = pd.read_csv("../data/general_output/all_results_" + mode + ".tsv", sep = "\t")
        plt.figure(figsize=(20, 10))
        for index in selected_indices:
            data.append(df[index])
            plt.scatter(df["tree_size"], df[index], label = index, s = 10)
        plt.legend(loc = "upper left")
        plt.xlabel("tree size n")
        plt.ylabel("index values")
        plt.yscale("log")
        plt.savefig(os.path.join(plots_dir, "size_correlation_scatter_" + mode + ".png"))
        plt.clf()
        plt.figure(figsize=(20, 10))
        if mode in ["absolute", "relative_tips"]:
            ax = seaborn.stripplot(data = data, log_scale=True)
        else:
            ax = seaborn.stripplot(data = data)
        ax.set_xticklabels(selected_indices)
        plt.xticks(rotation=90)
        plt.xlabel("index")
        plt.ylabel("value")
        plt.savefig(os.path.join(plots_dir, "size_values_" + mode +  + suffix + ".png"), bbox_inches='tight')
        plt.clf()


base_dirs = ["../data/evonaps_dna"]

plot_tree_sizes(base_dirs)
#plot_correlations(base_dirs, "database", "groups_90")
#plot_correlations(base_dirs, "database", "repr_90")
##plot_correlations(base_dirs, "rerooting", "groups_95") # not sure whether of interest
##plot_correlations(base_dirs, "rerooting", "repr_95")
#plot_size_correlations(base_dirs)


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
    plot_variances(base_dirs, sublist, "_" + str(k))
    #plot_against_size(base_dirs, sublist, stat = "kurtosis", suffix = "_" + str(k)) #not looking good
    #plot_size_correlations(selected_indices, suffix = "_" + str(k))



