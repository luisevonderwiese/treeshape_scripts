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
from treeshapy import TreeShape, INDICES
from collections import Counter
from tabulate import tabulate



INDICES.remove("colijn_plazotta_rank")
INDICES.remove("furnas_rank")

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
            ts = TreeShape(rooted_tree, binary = True, rooted = True)
            for index_name in INDICES:
                v = ts.evaluate(index_name)
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
        ts = TreeShape(new_tree, binary = True)
        for index_name in INDICES:
            v = ts.evalute(index_name)
            res.append(v)
        with open(res_path, "a") as outfile:
            outfile.write("\t".join([root, root_type, node.LWR]))
            outfile.write("\t")
            outfile.write("\t".join([str(v) for v in res]))
            outfile.write("\n")


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


def rank(value, values):
    count_leq = sum(x <= value for x in values)
    count_eq = sum(x == value for x in values)
    percentile = 100 * ((count_leq  - 0.5 * count_eq)/ len(values))
    return percentile
    #smaller = len([v for v in values if v < value])
    #equal = len([v for v in values if v  == value]) - 1
    #return round(((smaller + (equal / 2)) / len(values)) * 100) 


def ranking_analysis(simulated_base_dir, emp_res_path, emp_tab_path):
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
    res_df = pd.DataFrame(res, columns = ["index", "max_1", "max_2", "mean", "weighted_mean"])
    res_df.to_csv(emp_tab_path, sep = "\t")

def ranking_table(emp_tab_path):
    df = pd.read_csv(os.path.join(emp_tab_path), sep = "\t")
    df = df.drop("Unnamed: 0", axis = 1)
    res = [list(row) for _, row in df.iterrows()]
    for row in res:
        row[0] = "\codeword{" + row[0] + "}"
        highlight  = abs(row[1] - row[2]) > 10
        for i in range(1, len(row)):
            if highlight and i <= 2:
                row[i] = "$\mathbf{" + str(round(row[i], 1)) + "}$"
            else:
                row[i] = "$" + str(round(row[i], 1)) + "$"
    tab = tabulate(res, headers = df.columns, tablefmt = "latex_raw")
    print(tab)

def print_trees(lwr_tree_path):
    tree = Tree(lwr_tree_path)
    lwr_dict = {}
    inner_node_id = 0
    num_leaves = len(list([l for l in tree.iter_leaves()]))
    i = 0
    for l in tree.iter_leaves():
        l.add_feature("Data", i/num_leaves)
        i += 1
    for node in tree.traverse():
        if not node.is_leaf():
            node.name = str(inner_node_id)
            inner_node_id += 1
        try:
            lwr_dict[node.name] = node.LWR
        except:
            print(node.name)
    lwr_dict = dict(sorted(lwr_dict.items(), key=lambda item: item[1], reverse = True))
    for name, lwr in list(lwr_dict.items())[:2]:
        print(lwr)
        tree.set_outgroup(tree&name)
        print(tree.write())

base_dirs = ["simulated_24"]
for base_dir in base_dirs:
    root_trees(base_dir)
    evaluate_indices(base_dir)

if not os.path.isdir("receptor/treeshapy"):
    os.makedirs("receptor/treeshapy")
evaluate_indices_lwr("receptor/rd.lwr.tree", "receptor/treeshapy")
ranking_analysis("simulated_24", "receptor/treeshapy/rd.lwr_res.tsv", "receptor/ranks.tsv")
ranking_table("receptor/ranks.tsv")


print_trees("receptor/rd.lwr.tree")
