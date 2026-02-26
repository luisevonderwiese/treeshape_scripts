import os
import numpy as np
import pandas as pd
from tabulate import tabulate
from ete3 import Tree
import matplotlib.pyplot as plt
from collections import Counter
import seaborn

import util

def plot_tree_sizes(base_dirs, plots_dir):
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


def plot_kurtosis(selected_indices, plots_dir, suffix = "", colors = None, labels = None):
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
        data = [[el for el in l if not (el is float("nan") or el is float("inf") or el is float("-inf") or el == 0)] for l in data]
        if colors is not None:
            ax = seaborn.violinplot(data = data, palette = colors, log_scale = True)
        else:
            ax = seaborn.violinplot(data = data, log_scale=True)
        ax.set_ylim(0.8, 1100)
        ax.axhline(y=1, color='gray', linestyle='--')

        ax.set_xticklabels(selected_indices)
        plt.xticks(rotation=90)
        plt.xlabel("index")
        plt.ylabel(mode)

        plt.savefig(os.path.join(plots_dir, mode + suffix + ".png"), bbox_inches='tight')
        plt.clf()


def plot_iqr(selected_indices, plots_dir, suffix = "", colors = None, labels = None):
    modes = ["iqr", "iqr_int", "iqr_ext"]

    if colors is not None:
        palette = seaborn.color_palette("husl", max(colors) + 1)
        colors = [palette[color] for color in colors]
    database_df = pd.read_csv("../data/general_output/database_iqrs.tsv", sep = "\t")
    for mode in modes:
        df = pd.read_csv(os.path.join("../data/general_output/" + mode + ".tsv"), sep = "\t")
        data = []
        for index in selected_indices:
            db_iqr = database_df[database_df["index"] == index]["iqr"].iloc[0]
            data.append([v / db_iqr for v in df[index]])
    
        plt.figure(figsize=(2 * len(selected_indices), 10))
        data = [[el for el in l if not (el is float("nan") or el is float("inf") or el is float("-inf") or el == 0)] for l in data]
        if colors is not None:
            ax = seaborn.boxplot(data = data, palette = colors, log_scale = True)
        else:
            ax = seaborn.violinplot(data = data, log_scale = True)
        ax.set_ylim(0.000001, 1000)
        ax.axhline(y=1, color='gray', linestyle='--')
        
        ax.set_xticklabels(selected_indices)
        plt.xticks(rotation=90)
        plt.xlabel("index")
        plt.ylabel(mode)
 
        plt.savefig(os.path.join(plots_dir, mode + suffix + ".png"), bbox_inches='tight')
        plt.clf()


def plot_correlations(corr_type, index_list, plots_dir):
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
    plt.savefig(os.path.join(plots_dir, corr_type + "_heatmap.png"))
    plt.clf()


def colored_cell(v):
    if v != v:
        return "\cellcolor{gray!25} "
    if abs(v) < 0.1:
        return "\cellcolor{green!25}$" + str(round(v, 2)) + "$"
    if abs(v) <= 0.3:
        return "\cellcolor{yellow!25}$" + str(round(v, 2)) + "$"
    if abs(v) > 0.6:
        return "\cellcolor{red!25}$" + str(round(v, 2)) + "$"
    return "\cellcolor{orange!25}$" + str(round(v, 2)) + "$"

def size_correlation_table(indices, plots_dir):
    modes = ["absolute", "relative_tips", "relative_max", "relative_yule"]
    dfs = {}
    for mode in modes:
        df = pd.read_csv("../data/general_output/size_correlations_" + mode + ".tsv", sep = "\t")
        df = df.drop("Unnamed: 0", axis = 1)
        dfs[mode] = df

    for corr_type in ["pearson", "spearman"]:
        res = []
        res_latex = []

        for index in indices:
            res_row = [index]
            res_row_latex = ["\codeword{" + index + "}"]
            for mode in modes:
                df = dfs[mode]
                sub_df = df[df["index"] == index]
                if len(sub_df) == 0:
                    v = float("nan")
                else:
                    v = sub_df.iloc[0]["corr_" + corr_type]
                res_row.append(v)
                res_row_latex.append(colored_cell(v))
            res.append(res_row)
            res_latex.append(res_row_latex)
        tab = tabulate(res, headers = ["index"] + modes, tablefmt = "csv")
        with open(os.path.join(plots_dir, "size_correlations_" + corr_type + ".csv"), "w+") as outfile:
            outfile.write(tab)
        tab = tabulate(res_latex, headers = ["index"] + modes, tablefmt = "latex_raw")
        print(tab)
        with open(os.path.join(plots_dir, "size_correlations_" + corr_type + ".tex"), "w+") as outfile:
            outfile.write(tab)




plots_dir = "../data/plots"
if not os.path.isdir(plots_dir):
    os.makedirs(plots_dir)


base_dirs = ["../data/evonaps_dna"]
plot_tree_sizes(base_dirs, plots_dir)



index_types = {"node_indices":[
          "colless_index",
          "corrected_colless_index",
          "quadratic_colless_index",
          "I_2_index",
          "stairs2",
          "stairs1",
          "j1",
          "rogers_j_index",
          "symmetry_nodes_index"],
"I_based_indices":["mean_I",
          "mean_I_prime",
          "mean_I_w",
          "total_I",
          "total_I_prime",
          "total_I_w"],
"depth_indices": ["sackin_index",
          "total_path_length",
          "total_internal_path_length",
          "average_vertex_depth",
          "average_leaf_depth",
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
          "average_ladder",
          "ladder_length",
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
all_indices_gaps = []
colors = []
labels = []

for i, (index_type, indices) in enumerate(index_types.items()):
    all_indices += indices
    all_indices_gaps += indices
    all_indices_gaps.append("")
    colors += len(indices) * [i]
    labels += len(indices) * [index_type]

#size_correlation_table(all_indices, plots_dir)
#plot_kurtosis(all_indices, plots_dir, "_all", colors, labels)
plot_iqr(all_indices, plots_dir, "_all", colors, labels)

#plot_correlations("database", all_indices_gaps, plots_dir)
#plot_correlations("rerooting", all_indices_gaps, plots_dir)

