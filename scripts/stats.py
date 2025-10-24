import os
import pandas as pd
import numpy as np
from tabulate import tabulate
from ete3 import Tree

from treeshapy.treeshapy import INDICES

import util

def determine_tree_sizes(base_dir):
    tree_dir = os.path.join(base_dir, "trees/unrooted/")
    data = []

    for tree_name in os.listdir(tree_dir):
        n = len(Tree(os.path.join(tree_dir, tree_name)))
        tree_name_x = tree_name.split(".")[0]
        data.append([tree_name_x, n])

    df = pd.DataFrame(data, columns = ["tree_name", "num_tips"])
    out_path = os.path.join(base_dir, "tree_sizes.tsv")
    df.to_csv(out_path, sep = "\t")

def determine_max_min(base_dir):
    results_dir = os.path.join(base_dir, "treeshapy")

    mins = {}
    maxs = {}
    for index in INDICES:
        mins[index] = 1000000
        maxs[index] = 0

    for tree_name in util.unrooted_tree_names(base_dir):
        df = pd.read_csv(os.path.join(results_dir, tree_name + "_absolute.tsv"), sep= "\t")
        for index in INDICES:
            mins[index] = min(mins[index], min(df[index]))
            maxs[index] = max(maxs[index], max(df[index]))

    results = []
    for index in INDICES:
        results.append([index, mins[index], maxs[index]])

    print(tabulate(results, headers=["index", "min", "max"], tablefmt="pipe", floatfmt=".6f"))
    df = pd.DataFrame(results, columns=["index", "min", "max"])
    df.to_csv(os.path.join(base_dir, "min_max.tsv"), sep = "\t")


def determine_database_variances(base_dir):
    results_dir = os.path.join(base_dir, "treeshapy")
    all_values = {}
    for index in INDICES:
        all_values[index] = []
    for tree_name in util.unrooted_tree_names(base_dir):
        df = pd.read_csv(os.path.join(results_dir, tree_name + "_relative.tsv"), sep= "\t")
        for index in INDICES:
            if index == "maximum_depth":
                print(df[index])
            all_values[index].append(np.mean(df[index]))
    table = [[index, np.nanvar(all_values[index])] for index in INDICES]
    headers = ["index", "database_var"]
    print(tabulate(table, headers = headers, tablefmt="pipe", floatfmt=".6f"))
    df = pd.DataFrame(table, columns=headers)
    df.to_csv(os.path.join(base_dir, "database_variances.tsv"), sep = "\t")

def determine_variances(base_dir):
    results_dir = os.path.join(base_dir, "treeshapy")
    variance_dir = os.path.join(base_dir, "rooting_variances")
    if not os.path.isdir(variance_dir):
        os.makedirs(variance_dir)

    db_df = pd.read_csv(os.path.join(base_dir, "database_variances.tsv"), sep = "\t")

    for tree_name in util.unrooted_tree_names(base_dir):
        df = pd.read_csv(os.path.join(results_dir, tree_name + "_relative.tsv"), sep= "\t")
        df_external = df[df["root_type"] == "external"]
        df_internal = df[df["root_type"] == "internal"]
        table = []
        for index in INDICES:
            db_var = db_df[db_df["index"] == index].iloc[0]["database_var"]
            mean = np.nanmean(df[index], dtype=np.float64)
            var = np.nanvar(df[index], dtype=np.float64)
            var_ext = np.nanvar(df_external[index], dtype=np.float64)
            var_int = np.nanvar(df_internal[index], dtype=np.float64)
            table.append([index, mean, var, var_int, var_ext,
                    var / db_var, var_int / db_var, var_ext / db_var])

        headers = ["index", "mean", "var", "var_int", "var_ext", "rel_var", "rel_var_int", "rel_var_ext"]
        print(tabulate(table, headers = headers, tablefmt="pipe", floatfmt=".6f"))
        df = pd.DataFrame(table, columns=headers)
        df.to_csv(os.path.join(variance_dir, tree_name + ".tsv"), sep = "\t")

def determine_mean_variances(base_dir):
    variances_dir = os.path.join(base_dir, "rooting_variances")
    dfs = [pd.read_csv(os.path.join(variances_dir, tree_name + ".tsv"), sep= "\t") for tree_name in util.unrooted_tree_names(base_dir)]
    props = ["mean", "var", "var_int", "var_ext", "rel_var", "rel_var_int", "rel_var_ext"]
    table = []
    for index in INDICES:
        sub_dfs = [df[df["index"] == index].iloc[0] for df in dfs]
        table.append([index] + [np.nanmean([sub_df[prop] for sub_df in sub_dfs]) for prop in props])

    headers = ["index"] + props
    print(tabulate(table, headers = headers, tablefmt="pipe", floatfmt=".6f"))
    df = pd.DataFrame(table, columns=headers)
    df.to_csv(os.path.join(base_dir, "mean_variances.tsv"), sep = "\t")


def determine_rerooting_correlations(base_dir):
    results_dir = os.path.join(base_dir, "treeshapy")

    correlations = {}
    for index1 in INDICES:
        correlations[index1] = {}
        for index2 in INDICES:
            correlations[index1][index2] = []
    for tree_name in util.unrooted_tree_names(base_dir):
        df = pd.read_csv(os.path.join(results_dir, tree_name + "_absolute.tsv"), sep= "\t")
        for index1 in INDICES:
            for index2 in INDICES:
                c = abs(df[index1].corr(df[index2]))
                correlations[index1][index2].append(c)

    table = [[index1] + [np.nanmean(correlations[index1][index2]) for index2 in INDICES] for index1 in INDICES]
    
    headers = ["index1"] + INDICES
    print(tabulate(table, headers = headers, tablefmt="pipe", floatfmt=".6f"))
    df = pd.DataFrame(table, columns=headers)
    df.to_csv(os.path.join(base_dir, "rerooting_correlations.tsv"), sep = "\t")

def determine_database_correlations(base_dir):
    results_dir = os.path.join(base_dir, "treeshapy")
    
    all_values = {index : [] for index in INDICES}
    for tree_name in util.unrooted_tree_names(base_dir):
        df = pd.read_csv(os.path.join(results_dir, tree_name + "_absolute.tsv"), sep= "\t")
        for index in INDICES:
            all_values[index] += [el for el in df[index]]
    df = pd.DataFrame()
    for index in INDICES:
        df[index] = all_values[index]

    table = [[index1] + [abs(df[index1].corr(df[index2])) for index2 in INDICES] for index1 in INDICES]
    
    headers = ["index1"] + INDICES
    print(tabulate(table, headers = headers, tablefmt="pipe", floatfmt=".6f"))
    df = pd.DataFrame(table, columns=headers)
    df.to_csv(os.path.join(base_dir, "database_correlations.tsv"), sep = "\t")


def all_stats(base_dir):
    determine_tree_sizes(base_dir)
    determine_max_min(base_dir)
    determine_database_variances(base_dir)
    determine_variances(base_dir)
    determine_mean_variances(base_dir)
    determine_rerooting_correlations(base_dir)
    determine_database_correlations(base_dir)


all_stats("../data/evonaps_dna")
