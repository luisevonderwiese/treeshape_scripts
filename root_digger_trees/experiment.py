import sys
import os
import random
import math
from ete3 import Tree
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn
import copy
from treeshapy.treeshapy import TreeShape, INDICES
from collections import Counter
from tabulate import tabulate


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



INDICES = []

for i, (index_type, indices) in enumerate(index_types.items()):
    INDICES += indices

def root_trees(base_dir):
    unrooted_trees_dir = os.path.join(base_dir, "unrooted")
    rooted_trees_dir = os.path.join(base_dir, "rooted")
    for d in [rooted_trees_dir]:
        if not os.path.isdir(d):
            os.makedirs(d)

    for tree_name in os.listdir(unrooted_trees_dir):
        unrooted_tree_path = os.path.join(unrooted_trees_dir, tree_name)
        tree = Tree(unrooted_tree_path)
        tree_name_x = ".".join(tree_name.split(".")[:-1])
        rooted_trees_sub_dir = os.path.join(rooted_trees_dir, tree_name_x)
        if os.path.isdir(rooted_trees_sub_dir):
            continue
        print(tree_name_x)
        os.makedirs(rooted_trees_sub_dir)
        inner_root_id = 0
        for node in tree.iter_descendants():
            if node.is_leaf():
                root = node.name.replace("/", "").replace("_", "")
                root_type = "external"
            else:
                root_type = "internal"
                root = str(inner_root_id)
                inner_root_id += 1

            tree.set_outgroup(node)
            
            rooted_tree_path = os.path.join(rooted_trees_sub_dir, root_type + "_" + root + ".rooted.tree")
            with open(rooted_tree_path, "w+") as outfile:
                outfile.write(tree.write(format = 8))


def evaluate_indices(base_dir):
    unrooted_trees_dir = os.path.join(base_dir, "unrooted")
    rooted_trees_dir = os.path.join(base_dir, "rooted")
    results_dir = os.path.join(base_dir, "treeshapy")

    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)

    for tree_name in os.listdir(unrooted_trees_dir):
        tree_name_x = ".".join(tree_name.split(".")[:-1])
        res_path = os.path.join(results_dir, tree_name_x + "_res.tsv")

        header = ["root", "root_type"] + INDICES
        with open(res_path, "w+") as outfile:
            outfile.write("\t".join(header))
            outfile.write("\n")

        subdir = os.path.join(rooted_trees_dir, tree_name_x)
        for name in os.listdir(subdir):
            tree_path = os.path.join(subdir, name)
            rooted_tree = Tree(tree_path, format = 8)
            parts = name.split(".")[0].split("_")
            root = parts[1]
            root_type = parts[0]

            res = []
            ts = TreeShape(rooted_tree, "BINARY")
            for index_name in INDICES:
                v = ts.absolute(index_name)
                res.append(v)

            with open(res_path, "a") as outfile:
                outfile.write("\t".join([root, root_type]))
                outfile.write("\t")
                outfile.write("\t".join([str(v) for v in res]))
                outfile.write("\n")


def label_inner(new_tree, inner_root_id):
    new_id = 0
    for node in new_tree.iter_descendants():
        if not node.is_leaf():
            node.name = str(new_id)
            new_id += 1
            if new_id == inner_root_id:
                return new_tree
    return new_tree



def evaluate_indices_lwr(lwr_tree_path, res_dir):
    tree = Tree(lwr_tree_path)
    tree_name_x = ".".join(lwr_tree_path.split("/")[-1].split(".")[:-1])
    print(tree_name_x)
    inner_root_id = 0

    res_path = os.path.join(res_dir, tree_name_x + "_res.tsv")
    header = ["root", "root_type", "LWR"] + INDICES
    with open(res_path, "w+") as outfile:
        outfile.write("\t".join(header))
        outfile.write("\n")

    for node in tree.iter_descendants():
        new_tree = Tree(lwr_tree_path) #prevent reuse of treeshapy attributes
        if node.is_leaf():
            root = node.name.replace("/", "").replace("_", "")
            new_tree.set_outgroup(new_tree&node.name)
            root_type = "external"
        else:
            root_type = "internal"
            root = str(inner_root_id)
            inner_root_id += 1
            new_tree = label_inner(new_tree, inner_root_id)
            new_tree.set_outgroup(new_tree&str(inner_root_id -1))
        res = []
        ts = TreeShape(new_tree, "BINARY")
        for index_name in INDICES:
            v = ts.absolute(index_name)
            res.append(v)
        with open(res_path, "a") as outfile:
            outfile.write("\t".join([root, root_type, node.LWR]))
            outfile.write("\t")
            outfile.write("\t".join([str(v) for v in res]))
            outfile.write("\n")

def plot(base_dirs):
    plots_dir = "plots"

    if not os.path.isdir(plots_dir):
        os.makedirs(plots_dir)
    for index in INDICES:
        print(index)
        data = []
        for base_dir in base_dirs:
            row = []
            results_dir = os.path.join(base_dir, "treeshapy")
            for fn in os.listdir(results_dir):
                df = pd.read_csv(os.path.join(results_dir, fn), sep = "\t")
                row += list(df[index])
            data.append(row)
        ax = seaborn.boxplot(data = data)
        ax.set_xticklabels(base_dirs)
        plt.xticks(rotation=90)
        plt.ylabel(index)
        plt.savefig(os.path.join(plots_dir, "box_" + index + ".png"))
        plt.clf()


def get_stats_lwr(df, index):
    values = list(df[index])
    max_1 = values[0]
    max_2 = values[1]
    weighted_mean = 0
    for i, row in df.iterrows():
        if row[index] == row[index]:
            weighted_mean += row["LWR"] * row[index]
    mean = np.nanmean(values)
    return [max_1, max_2, mean, weighted_mean]

def plot_lwr(simulated_base_dir, lwr_res_path):
    plots_dir = "plots"
    if not os.path.isdir(plots_dir):
        os.makedirs(plots_dir)
    lwr_df = pd.read_csv(lwr_res_path, sep = "\t")
    lwr_df.sort_values(by = ["LWR"], inplace = True, ascending = False)
    results_dir = os.path.join(simulated_base_dir, "treeshapy")
    for index in INDICES:
        print(index)
        data = [[]]
        for fn in os.listdir(results_dir):
            df = pd.read_csv(os.path.join(results_dir, fn), sep = "\t")
            data[0] += list(df[index])
        plt.figure(figsize=(5, 10))
        ax = seaborn.boxplot(data = data)
        colors = ['green', 'blue', 'red', "gray"]
        stats = stats_lwr(lwr_df, index)
        for i, stat in enumerate(stats):
            ax.axhline(y = stat, color = colors[i], linestyle = "--")
        plt.ylabel(index)
        plt.savefig(os.path.join(plots_dir, "box_" + index + "_lwr.png"))
        plt.clf()
        plt.close()


def get_kurtosis(values):
    values = [v for v in values if v == v]
    mean = sum(values) / len(values)
    try:
        s_quad = sum([math.pow(v - mean, 4) for v in values])
        s_squared = sum([math.pow((v - mean), 2) for v in values])
    except OverflowError:
        return float("nan")
    if s_squared == 0:
        return 1
    else:
        try:
            return len(values) * (s_quad / math.pow(s_squared, 2))
        except OverflowError:
            return float("nan")

def get_iqr(values):
    Q3 = np.quantile(values, 0.9)
    Q1 = np.quantile(values, 0.1)
    return Q3 - Q1

def stats_simulated(base_dir):
    results_dir = os.path.join(base_dir, "treeshapy")
    all_data = {index : [] for index in INDICES}
    for fn in os.listdir(results_dir):
        res_path = os.path.join(results_dir, fn)
        df = pd.read_csv(res_path, sep = "\t")
        for index in INDICES:
            all_data[index] += list(df[index])
    iqrs = []
    for index in INDICES:
        iqrs.append([index, min(all_data[index]), max(all_data[index]), get_iqr(all_data[index])])
    df = pd.DataFrame(iqrs, columns = ["index", "min", "max", "iqr"])
    df.to_csv(os.path.join(base_dir, "stats.tsv"), sep = "\t")

def stats_table(res_path, stats_path):
    df = pd.read_csv(os.path.join(res_path), sep = "\t")
    stats_df = pd.read_csv(os.path.join(stats_path), sep = "\t")
    res = []
    for index in INDICES:
        stats_simulated = stats_df[stats_df["index"] == index].iloc[0]
        stats_lwr = get_stats_lwr(df, index)
        values = df[index].astype("float")
        kurtosis = get_kurtosis(values)
        iqr = get_iqr(values) / stats_simulated["iqr"]
        max_1 = (stats_lwr[0] - stats_simulated["min"]) / (stats_simulated["max"] - stats_simulated["min"])
        max_2 = (stats_lwr[1] - stats_simulated["min"]) / (stats_simulated["max"] - stats_simulated["min"])
        mean = (stats_lwr[2] - stats_simulated["min"]) / (stats_simulated["max"] - stats_simulated["min"])
        weighted_mean = (stats_lwr[3] - stats_simulated["min"]) / (stats_simulated["max"] - stats_simulated["min"])
        res.append([index, kurtosis, iqr, max_1, max_2, mean, weighted_mean])
    tab = tabulate(res, headers = ["index", "kurtosis", "iqr", "max_1", "max_2", "mean", "weighted_mean"], floatfmt = ".3f", tablefmt = "pipe")
    print(tab)

def rank(value, values):
    smaller = len([v for v in values if v < value])
    equal = len([v for v in values if v  == value])
    return round(((smaller + (equal / 2)) / len(values)) * 100)


def ranking_analysis(simulated_base_dir, emp_res_path):
    results_dir = os.path.join(simulated_base_dir, "treeshapy")
    all_data = {index : [] for index in INDICES}
    for fn in os.listdir(results_dir):
        res_path = os.path.join(results_dir, fn)
        df = pd.read_csv(res_path, sep = "\t")
        for index in INDICES:
            all_data[index] += list(df[index])
    df = pd.read_csv(os.path.join(emp_res_path), sep = "\t")
    res = []
    for index in INDICES:
        print(index)
        values_simulated = all_data[index]
        stats_lwr = get_stats_lwr(df, index)
        res.append([index] + [rank(stat, values_simulated) for stat in stats_lwr])
    tab = tabulate(res, headers = ["index", "max_1", "max_2", "mean", "weighted_mean"], tablefmt = "pipe")
    print(tab)


base_dirs = ["simulated_x_34"]#, "spiders"]
for base_dir in base_dirs:
    root_trees(base_dir)
    #evaluate_indices(base_dir)

#evaluate_indices_lwr("spiders/mitocondrial_opt_brlen.tree.lwr.tree", "spiders/treeshapy")
#plot_lwr("simulated_34", "spiders/treeshapy/mitocondrial_opt_brlen.tree.lwr_res.tsv")
#plot(base_dirs)
#stats_simulated("simulated_34")
#stats_table("spiders/treeshapy/mitocondrial_opt_brlen.tree.lwr_res.tsv", "simulated_34/stats.tsv")
#ranking_analysis("simulated_34", "spiders/treeshapy/mitocondrial_opt_brlen.tree.lwr_res.tsv")
