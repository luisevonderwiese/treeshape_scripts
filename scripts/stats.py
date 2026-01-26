import os
import math
import pandas as pd
import numpy as np
from tabulate import tabulate
from ete3 import Tree

from treeshapy.treeshapy import INDICES

import util

def determine_tree_sizes(base_dirs):
    for base_dir in base_dirs:
        tree_dir = os.path.join(base_dir, "trees/unrooted/")
        data = []

        for tree_name in os.listdir(tree_dir):
            n = len(Tree(os.path.join(tree_dir, tree_name)))
            tree_name_x = tree_name.split(".")[0]
            data.append([tree_name_x, n])

        df = pd.DataFrame(data, columns = ["tree_name", "num_tips"])
        out_path = os.path.join(base_dir, "tree_sizes.tsv")
        df.to_csv(out_path, sep = "\t")

def determine_max_min(base_dirs):
    mins = {index : 1000000 for index in INDICES}
    maxs = {index : 0 for index in INDICES}
    
    for base_dir in base_dirs:
        results_dir = os.path.join(base_dir, "treeshapy")
        for tree_name in util.unrooted_tree_names(base_dir):
            df_path = os.path.join(results_dir, tree_name + "_absolute.tsv")
            if not os.path.isfile(df_path):
                continue
            df = pd.read_csv(df_path, sep= "\t")
            if len(df) == 0:
                continue
            for index in INDICES:
                mins[index] = min(mins[index], min(df[index]))
                maxs[index] = max(maxs[index], max(df[index]))

    results = []
    for index in INDICES:
        results.append([index, mins[index], maxs[index]])

    print(tabulate(results, headers=["index", "min", "max"], tablefmt="pipe", floatfmt=".6f"))
    df = pd.DataFrame(results, columns=["index", "min", "max"])
    df.to_csv("../data/general_output/min_max.tsv", sep = "\t")


def determine_database_variances(base_dirs):
    all_values = {index : [] for index in INDICES}

    for base_dir in base_dirs:
        results_dir = os.path.join(base_dir, "treeshapy")
        for tree_name in util.unrooted_tree_names(base_dir):
            df_path = os.path.join(results_dir, tree_name + "_absolute.tsv")
            if not os.path.isfile(df_path):
                continue
            df = pd.read_csv(df_path, sep= "\t")
            if len(df) == 0:
                continue
            for index in INDICES:
                all_values[index].append(np.mean(df[index]))
    table = []
    for index in INDICES:
        var = np.nanvar(all_values[index])
        mean = np.nanmean(all_values[index])
        table.append([index, var, var / mean])
    
    headers = ["index", "database_var", "database_vc"]
    print(tabulate(table, headers = headers, tablefmt="pipe", floatfmt=".6f"))
    
    df = pd.DataFrame(table, columns=headers)
    df.to_csv(os.path.join(out_dir, "database_variances.tsv"), sep = "\t")

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


def determine_stats(base_dirs):
    db_df = pd.read_csv("../data/general_output/database_variances.tsv", sep = "\t")
    for base_dir in base_dirs:
        results_dir = os.path.join(base_dir, "treeshapy")
        variance_dir = os.path.join(base_dir, "rooting_variances")
        if not os.path.isdir(variance_dir):
            os.makedirs(variance_dir)
        for tree_name in util.unrooted_tree_names(base_dir):
            df_path = os.path.join(results_dir, tree_name + "_absolute.tsv")
            if not os.path.isfile(df_path):
                continue
            df = pd.read_csv(df_path, sep= "\t")
            if len(df) == 0:
                continue
            df_external = df[df["root_type"] == "external"]
            df_internal = df[df["root_type"] == "internal"]
            table = []
            for index in INDICES:
                #db_var = db_df[db_df["index"] == index].iloc[0]["database_var"]
                #db_vc = db_df[db_df["index"] == index].iloc[0]["database_vc"]
                mean = np.nanmean(df[index], dtype=np.float64)
                #var = np.nanvar(df[index], dtype=np.float64)
                #var_ext = np.nanvar(df_external[index], dtype=np.float64)
                #var_int = np.nanvar(df_internal[index], dtype=np.float64)
                kurtosis = get_kurtosis(df[index])
                kurtosis_int = get_kurtosis(df_internal[index])
                kurtosis_ext = get_kurtosis(df_external[index])
                table.append([index, mean, kurtosis, kurtosis_int, kurtosis_ext]) 
            headers = ["index", "mean", "kurtosis", "kurtosis_int", "kurtosis_ext"]
            print(tabulate(table, headers = headers, tablefmt="pipe", floatfmt=".6f"))
            df = pd.DataFrame(table, columns=headers)
            df.to_csv(os.path.join(variance_dir, tree_name + ".tsv"), sep = "\t")

def determine_variance_means(base_dirs):
    dfs = []
    for base_dir in base_dirs:
        variances_dir = os.path.join(base_dir, "rooting_variances")
        for tree_name in util.unrooted_tree_names(base_dir):
            df_path = os.path.join(variances_dir, tree_name + ".tsv")
            if not os.path.isfile(df_path):
                continue
            dfs.append(pd.read_csv(df_path, sep= "\t"))
    
    props = ["mean", "var", "var_int", "var_ext", "rel_var", "rel_var_int", "rel_var_ext", "vc", "vc_int", "vc_ext", "rel_vc", "rel_vc_int", "rel_vc_ext"]
    table = []
    for index in INDICES:
        sub_dfs = [df[df["index"] == index].iloc[0] for df in dfs]
        table.append([index] + [np.nanmean([sub_df[prop] for sub_df in sub_dfs]) for prop in props])

    headers = ["index"] + props
    print(tabulate(table, headers = headers, tablefmt="pipe", floatfmt=".6f"))
    df = pd.DataFrame(table, columns=headers)
    df.to_csv("../data/general_output/mean_variances.tsv", sep = "\t")


def determine_rerooting_correlations(base_dirs):
    correlations = {}
    for index1 in INDICES:
        correlations[index1] = {}
        for index2 in INDICES:
            correlations[index1][index2] = []
    
    for base_dir in base_dirs:
        results_dir = os.path.join(base_dir, "treeshapy")
        for tree_name in util.unrooted_tree_names(base_dir):
            df_path = os.path.join(results_dir, tree_name + "_absolute.tsv")
            if not os.path.isfile(df_path):
                continue
            df = pd.read_csv(df_path, sep= "\t")
            if len(df) == 0:
                continue
            for index1 in INDICES:
                for index2 in INDICES:
                    c = abs(df[index1].corr(df[index2]))
                    correlations[index1][index2].append(c)

    table = [[index1] + [np.nanmean(correlations[index1][index2]) for index2 in INDICES] for index1 in INDICES]
    
    headers = ["index1"] + INDICES
    print(tabulate(table, headers = headers, tablefmt="pipe", floatfmt=".6f"))
    df = pd.DataFrame(table, columns=headers)
    df.to_csv("../data/general_output/rerooting_correlations.tsv", sep = "\t")

def determine_database_correlations(base_dirs):
    all_values = {index : [] for index in INDICES}
    for base_dir in base_dirs:
        results_dir = os.path.join(base_dir, "treeshapy")
        for tree_name in util.unrooted_tree_names(base_dir):
            df_path = os.path.join(results_dir, tree_name + "_absolute.tsv")
            if not os.path.isfile(df_path):
                continue
            df = pd.read_csv(df_path, sep= "\t")
            if len(df) == 0:
                continue
            for index in INDICES:
                all_values[index] += [el for el in df[index]]
    df = pd.DataFrame()
    for index in INDICES:
        df[index] = all_values[index]

    table = [[index1] + [abs(df[index1].corr(df[index2])) for index2 in INDICES] for index1 in INDICES]
    
    headers = ["index1"] + INDICES
    print(tabulate(table, headers = headers, tablefmt="pipe", floatfmt=".6f"))
    df = pd.DataFrame(table, columns=headers)
    df.to_csv("../data/general_output/database_correlations.tsv", sep = "\t")


def get_correlation(df, corr_mode):
    if corr_mode == "linear":
        sizes = df["size"]
    elif corr_mode == "log":
        sizes = [math.log(s) for s in df["size"]]
    elif corr_mode == "nlogn":
        sizes = [s * math.log(s) for s in df["size"]]
    elif corr_mode == "quadratic":
        sizes = [s * s for s in df["size"]]
    elif corr_mode == "exp":
        sizes = []
        for s in df["size"]:
            try:
                sizes.append(math.pow(2, s))
            except Exception as e:
                sizes.append(float("inf"))
    else:
        raise ValueError(corr_mode, "is not a correlation mode")
    return [df[index].corr(pd.Series(sizes)) for index in INDICES]


def determine_size_correlations(base_dirs, mode):
    all_values = {index : [] for index in INDICES}
    sizes = []
    corr_df = pd.DataFrame({"index" : INDICES})
    for base_dir in base_dirs:
        sizes_df = pd.read_csv(os.path.join(base_dir, "tree_sizes.tsv"), sep = "\t")
        results_dir = os.path.join(base_dir, "treeshapy")
        for tree_name in util.unrooted_tree_names(base_dir):
            df_path = os.path.join(results_dir, tree_name + "_" + mode + ".tsv")
            if not os.path.isfile(df_path):
                continue
            df = pd.read_csv(df_path, sep= "\t")
            if len(df) == 0:
                continue
            tree_size = sizes_df[sizes_df["tree_name"] == tree_name].iloc[0]["num_tips"]
            sizes += len(df) * [tree_size]
            for index in INDICES:
                all_values[index] += [el for el in df[index]]
    df = pd.DataFrame()
    df["size"] = sizes 
    for index in INDICES:
        df[index] = all_values[index]
    for corr_mode in ["linear", "log", "nlogn", "quadratic", "exp"]:
        print(corr_mode)
        corr_df["corr_" + corr_mode] = get_correlation(df, corr_mode)
    corr_df.to_csv("../data/general_output/size_correlations_" + mode + ".tsv", sep = "\t")


def gather_results(base_dirs, mode):
    all_results = []
    for base_dir in base_dirs:
        sizes_df = pd.read_csv(os.path.join(base_dir, "tree_sizes.tsv"), sep = "\t")
        results_dir = os.path.join(base_dir, "treeshapy")
        for tree_name in util.unrooted_tree_names(base_dir):
            tree_size = sizes_df[sizes_df["tree_name"] == tree_name].iloc[0]["num_tips"]
            df_path = os.path.join(results_dir, tree_name + "_" + mode + ".tsv")
            if not os.path.isfile(df_path):
                continue
            df = pd.read_csv(df_path, sep= "\t")
            if len(df) == 0:
                continue
            for i, row in df.iterrows():
                res_row = [tree_name + "_" + str(row["root"]), tree_size]
                for index in INDICES:
                    res_row.append(row[index])
                all_results.append(res_row)

    all_df = pd.DataFrame(all_results, columns = ["rooted_tree_name", "tree_size"] + INDICES)
    all_df.to_csv("../data/general_output/all_results_"+ mode + ".tsv", sep = "\t")


def gather_stats(base_dirs):
    stats = ["mean", "kurtosis", "kurtosis_int", "kurtosis_ext"]
    all_values = {}
    for stat in stats:
        all_values[stat] = {index : [] for index in INDICES}
    sizes = []
    for base_dir in base_dirs:
        sizes_df = pd.read_csv(os.path.join(base_dir, "tree_sizes.tsv"), sep = "\t")
        variance_dir = os.path.join(base_dir, "rooting_variances")
        for tree_name in util.unrooted_tree_names(base_dir):
            df_path = os.path.join(variance_dir, tree_name + ".tsv")
            if not os.path.isfile(df_path):
                continue
            df = pd.read_csv(df_path, sep= "\t")
            if len(df) == 0:
                continue
            tree_size = sizes_df[sizes_df["tree_name"] == tree_name].iloc[0]["num_tips"]
            sizes.append(tree_size)
            for index in INDICES:
                for stat in stats:
                    all_values[stat][index].append(df[df["index"] == index].iloc[0][stat])
    for stat in stats:
        df = pd.DataFrame()
        df["size"] = sizes
        for index in INDICES:
            df[index] = all_values[stat][index]
        df.to_csv("../data/general_output/" + stat + ".tsv", sep = "\t")


INDICES.remove("furnas_rank")
INDICES.remove("treeness")
INDICES.remove("stemminess")



#base_dirs = ["../data/evonaps_dna", "../data/evonaps_aa", "../data/grove"]
base_dirs = ["../data/evonaps_dna"]
out_dir = os.path.join("../data/general_output")
if not os.path.isdir(out_dir):
    os.makedirs(out_dir)

#determine_tree_sizes(base_dirs)
#determine_max_min(base_dirs)

#determine_database_variances(base_dirs) #deprecated
#determine_stats(base_dirs)
#gather_stats(base_dirs)
#determine_variance_means(base_dirs) #deprecated

#determine_rerooting_correlations(base_dirs) # not sure if of interest
#determine_database_correlations(base_dirs)

modes = ["absolute"] #"relative_max", "relative_tips", "relative_yule"]
for mode in modes:
    #gather_results(base_dirs, mode)
    determine_size_correlations(base_dirs, mode)
