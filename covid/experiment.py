import sys
import os
import random
import math
from ete3 import Tree
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
from treeshapy.treeshapy import TreeShape, INDICES
from collections import Counter
from tabulate import tabulate

sys.setrecursionlimit(10**6)

#INDICES = ["colless_index", "stairs1", "maximum_width", "ladder_length", "cherry_index", "area_per_pair_index", "root_imbalance"]

def root_trees():
    unrooted_trees_dir = os.path.join("unrooted")
    rooted_trees_dir = os.path.join("rooted")
    for d in [rooted_trees_dir]:
        if not os.path.isdir(d):
            os.makedirs(d)

    for tree_name in os.listdir(unrooted_trees_dir):
        unrooted_tree_path = os.path.join(unrooted_trees_dir, tree_name)
        tree = Tree(unrooted_tree_path)
        tree_name_x = ".".join(tree_name.split(".")[:-1])
        rooted_trees_dir = os.path.join("rooted", tree_name_x)
        if os.path.isdir(rooted_trees_dir):
            continue
        print(tree_name_x)
        os.makedirs(rooted_trees_dir)
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
            
            rooted_tree_path = os.path.join(rooted_trees_dir, root_type + "_" + root + ".rooted.tree")
            with open(rooted_tree_path, "w+") as outfile:
                outfile.write(tree.write())


def evaluate_indices():
    unrooted_trees_dir = "unrooted"
    rooted_trees_dir = "rooted"
    results_dir = "treeshapy"

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
            rooted_tree = Tree(tree_path)
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


def plot():
    results_dir = "treeshapy"
    plots_dir = "plots"

    if not os.path.isdir(plots_dir):
        os.makedirs(plots_dir)

    for fn in os.listdir(results_dir):
        fn_x = "_".join(fn.split("_")[:-1])
        df = pd.read_csv(os.path.join(results_dir, fn), sep = "\t")
        for index in INDICES:
            #print(Counter(df[index]))
            try:
                plt.hist(df[index], log = True)
            except:
                continue
            plt.xlabel("index value")
            plt.ylabel("#rooted trees")
            plt.savefig(os.path.join(plots_dir, fn_x + "_" + index + ".png"))
            plt.clf()

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


def kurtosis():
    results_dir = "treeshapy"
    for fn in os.listdir(results_dir):
        fn_x = "_".join(fn.split("_")[:-1])
        df = pd.read_csv(os.path.join(results_dir, fn), sep = "\t")
        res = []
        for index in INDICES:
            res.append([index, get_kurtosis(df[index].astype("float"))])
    tab = tabulate(res, headers = ["index", "kurtosis"], tablefmt = "pipe")
    print(tab)


#root_trees()
#evaluate_indices()
#plot()
kurtosis()
