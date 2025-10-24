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

GROUPS = [
        "sackin_index",
        "total_cophenetic_index",
        "wiener_index",
        "s_shape",
        "double_cherries",
        "average_leaf_depth",
        "maximum_depth",
        "diameter",
        "area_per_pair_index",
        "maximum_width",
        "maxdiff_widths",
        "modified_maxdiff_widths",
        "max_width_over_max_depth",
        "rooted_quartet_index",
        "stairs1",
        "stairs2",
        "mean_I",
        "I_2_index",
        "variance_of_leaves_depths",
        "ladder_length",
        "corrected_colless_index",
        "B_2_index",
        "root_imbalance"
        ]

GROUPS_STRICT = [
        "sackin_index",
        "double_cherries",
        "area_per_pair_index",
        "maximum_width",
        "rooted_quartet_index",
        "I_2_index",
        "variance_of_leaves_depths",
        "ladder_length",
        "corrected_colless_index",
        "B_2_index",
        "root_imbalance"
        ]

GROUPS_ROOTING = [
        "sackin_index",
        "mean_I",
        "maximum_depth",
        "max_width_over_max_depth",
        "rooted_quartet_index",
        "variance_of_leaves_depths",
        "B_2_index",
        "furnas_rank",
        "colijn_plazotta_rank",
        "maximum_width",
        "B_1_index",
        "cherry_index",
        "rogers_j_index",
        "root_imbalance",
        "maxdiff_widths",
        "modified_maxdiff_widths",
        "ladder_length",
        "pitchforks",
        "four_caterpillars",
        "double_cherries",
        "diameter",

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



def plot_variances(base_dirs):
    plots_dir = "../data/general_plots/rooting_variances"
    if not os.path.isdir(plots_dir):
        os.makedirs(plots_dir)

    selected_indices = ["sackin_index", "maximum_depth", "cherry_index", "rogers_j_index", "root_imbalance", "B_2_index"]

    results = {}
    modes = ["mean", "var", "var_int", "var_ext", "rel_var", "rel_var_int", "rel_var_ext"] 
    for mode in modes:
        results[mode] = {}
        for index in selected_indices:
            results[mode][index] = []
    
    for base_dir in base_dirs:
        variances_dir = os.path.join(base_dir, "rooting_variances")
        for tree_name in util.unrooted_tree_names(base_dir):
            df = pd.read_csv(os.path.join(variances_dir, tree_name + ".tsv"), sep= "\t")
            for index in selected_indices:
                sub_df = df[df["index"] == index].iloc[0]
                for mode in modes:
                    results[mode][index].append(sub_df[mode])
    
    for mode in modes:
        data = []
        labels = []
        for i, (index, rel_vars) in enumerate(results[mode].items()):
            data.append(rel_vars)
            labels.append(index)
    
        plt.figure(figsize=(20, 10))
        if mode == "mean":
            plt.ylim((-0.1, 1.1))
            ax = seaborn.stripplot(data = data, log_scale=False)
        elif mode in ["var", "var_int", "var_ext"]:
            plt.ylim((-0.01, 0.26))
            ax = seaborn.stripplot(data = data, log_scale=False)
        else:
            plt.ylim((0.00001, 100))
            ax = seaborn.stripplot(data = data, log_scale=True)
            ax.axhline(y=1, color='gray', linestyle='--')
        
        ax.set_xticklabels(labels)
        plt.xticks(rotation=90)
        plt.xlabel("index")
        plt.ylabel(mode)
 
        plt.savefig(os.path.join(plots_dir, mode + ".png"), bbox_inches='tight')
        plt.clf()


def plot_correlations(base_dirs, corr_type, index_list, list_name):
    index_list = GROUPS
    list_name = "groups"

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
    plt.savefig(os.path.join(plots_dir, corr_type + "_heatmap.png"))
    plt.clf()


base_dirs = ["../data/evonaps_dna"]
plot_tree_sizes(base_dirs)
plot_variances(base_dirs)
plot_correlations(base_dirs, "database", GROUPS, "groups")
plot_correlations(base_dirs, "rerooting", GROUPS_ROOTING, "groups_rooting")

