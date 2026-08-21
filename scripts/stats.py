import os
import math
import statistics
import pandas as pd
import numpy as np
from scipy import stats
from tabulate import tabulate
from ete3 import Tree

from treeshapy import INDICES

import util

large_value_indices = ["furnas_rank", "colijn_plazotta_rank"]


INDICES_UNROOTED = ["diameter",
          "area_per_pair_index",
          "wiener_index",
          "maximum_closeness",
          "minimum_farness",
          "maximum_farness",
          "total_farness",
          "minimum_bcent",
          "maximum_bcent",
          "mean_bcent",
          "bcent_variance"]

def not_nan(v):
    return [val for val in v if val == val and not isinstance(val, str)]

def safemean(v, index):
    if index in large_value_indices:
        v_nn = not_nan(v)
        if len(v_nn) == 0:
            return float("nan")
        return statistics.mean(v_nn)
    else:
        return np.nanmean(v)

def safevar(v, index):
    if index in large_value_indices:
        v_nn = not_nan(v)
        if len(v_nn) == 0:
            return float("nan")
        return statistics.pvariance(v_nn)
    else:
        return np.nanvar(v)

def safepearson(v1, v2, index1, index2):
    if index1 in large_value_indices or index2 in large_value_indices:
        try:
            return statistics.correlation(v1, v2)
        except:
            return float("nan")
    else:
        return np.corrcoef([v1, v2])[0][1]

def safespearman(v1, v2, index1, index2):
    if index1 in large_value_indices or index2 in large_value_indices:
        try:
            return statistics.correlation(v1, v2, method = "ranked")
        except:
            return float("nan")
    else:
        return stats.spearmanr(v1, v2, nan_policy="omit").statistic

def safequantile(v, index):
    if index in large_value_indices:
        v_nn = not_nan(v)
        if len(v_nn) == 0:
            return float("nan")
        q = statistics.quantiles(v_nn, n=10, method = "inclusive")
        return q[8] - q[0]
    else:
        return np.nanquantile(v, 0.9) - np.nanquantile(v, 0.1)

def determine_tree_sizes(base_dirs):
    print("determining tree sizes")
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
    print("determining min max")
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
                try:
                    mins[index] = min(mins[index], min(df[index]))
                    maxs[index] = max(maxs[index], max(df[index]))
                except:
                    continue

    results = []
    for index in INDICES:
        results.append([index, mins[index], maxs[index]])

    #print(tabulate(results, headers=["index", "min", "max"], tablefmt="pipe", floatfmt=".6f"))
    df = pd.DataFrame(results, columns=["index", "min", "max"])
    df.to_csv("../data/general_output/min_max.tsv", sep = "\t")


def determine_database_variances(base_dirs):
    print("determining database variance")
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
                all_values[index].append(safemean(df[index]))
    table = []
    for index in INDICES:
        var = safevar(all_values[index], index)
        mean = safemean(all_values[index], index)
        table.append([index, var, var / mean])
    
    headers = ["index", "database_var", "database_vc"]
    
    df = pd.DataFrame(table, columns=headers)
    df.to_csv(os.path.join(out_dir, "database_variances.tsv"), sep = "\t")

def get_kurtosis(values, index):
    values = [v for v in values if v == v]
    mean = safemean(values, index)
    if mean != mean:
        return float("nan")
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

def get_iqr(values, index):
    return safequantile(values, index)


def determine_unrooted_stats(base_dirs):
    print("determining unrooted stats")
    for base_dir in base_dirs:
        results_dir = os.path.join(base_dir, "treeshapy")
        unrooted_stats_dir = os.path.join(base_dir, "unrooted_stats")
        if not os.path.isdir(unrooted_stats_dir):
            os.makedirs(unrooted_stats_dir)
        for tree_name in util.unrooted_tree_names(base_dir):
            df_path = os.path.join(results_dir, tree_name + "_absolute.tsv")
            if not os.path.isfile(df_path):
                continue
            df = pd.read_csv(df_path, sep= "\t")
            unrooted_df_path = os.path.join(results_dir, tree_name + "_unrooted_absolute.tsv")
            if not os.path.isfile(unrooted_df_path):
                continue
            unrooted_df = pd.read_csv(unrooted_df_path, sep= "\t")
            if len(unrooted_df) == 0:
                continue
            table = []
            for index in INDICES_UNROOTED:
                rooted_values = df[index]
                unrooted_value = unrooted_df[index].iloc[0]
                count_leq = sum(value <= unrooted_value for value in rooted_values)
                count_eq = sum(value == unrooted_value for value in rooted_values)
                unrooted_percentile = 100 * ((count_leq - 0.5 * count_eq) / len(rooted_values))
                table.append([index, unrooted_percentile])
            headers = ["index", "unrooted_percentile"]
            df = pd.DataFrame(table, columns=headers)
            df.to_csv(os.path.join(unrooted_stats_dir, tree_name + ".tsv"), sep = "\t")


def determine_stats(base_dirs):
    print("determining stats")
    for base_dir in base_dirs:
        results_dir = os.path.join(base_dir, "treeshapy")
        stats_dir = os.path.join(base_dir, "stats")
        if not os.path.isdir(stats_dir):
            os.makedirs(stats_dir)
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
                mean = safemean(df[index], index)
                kurtosis = get_kurtosis(df[index], index)
                kurtosis_int = get_kurtosis(df_internal[index], index)
                kurtosis_ext = get_kurtosis(df_external[index], index)
                iqr = get_iqr(df[index], index)
                iqr_int = get_iqr(df_internal[index], index)
                iqr_ext = get_iqr(df_external[index], index)
                table.append([index, mean, kurtosis, kurtosis_int, kurtosis_ext, iqr, iqr_int, iqr_ext]) 
            headers = ["index", "mean", "kurtosis", "kurtosis_int", "kurtosis_ext", "iqr", "iqr_int", "iqr_ext"]
            df = pd.DataFrame(table, columns=headers)
            df.to_csv(os.path.join(stats_dir, tree_name + ".tsv"), sep = "\t")

def determine_database_correlations(base_dirs):
    print("determine database correlations")
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
    table = []
    for index in INDICES:
        df[index] = all_values[index]
        iqr = get_iqr(df[index], index)
        table.append([index, iqr])
    headers = ["index", "iqr"]
    iqr_df = pd.DataFrame(table, columns=headers)
    iqr_df.to_csv("../data/general_output/database_iqrs.tsv", sep = "\t")


    table = [[index1] + [abs(safepearson(df[index1], df[index2], index1, index2)) for index2 in INDICES] for index1 in INDICES]
    headers = ["index1"] + INDICES
    #print(tabulate(table, headers = headers, tablefmt="pipe", floatfmt=".6f"))
    corr_df = pd.DataFrame(table, columns=headers)
    corr_df.to_csv("../data/general_output/database_correlations_pearson.tsv", sep = "\t")

    table = [[index1] + [abs(safespearman(df[index1], df[index2], index1, index2)) for index2 in INDICES] for index1 in INDICES]
    headers = ["index1"] + INDICES
    #print(tabulate(table, headers = headers, tablefmt="pipe", floatfmt=".6f"))
    corr_df = pd.DataFrame(table, columns=headers)
    corr_df.to_csv("../data/general_output/database_correlations_spearman.tsv", sep = "\t")


def get_correlation(df, corr_mode, index):
    if corr_mode == "pearson":
        return [safepearson(df[index], df["size"], index, index) for index in INDICES]
    elif corr_mode == "spearman":
        return [safespearman(df[index], df["size"], index, index) for index in INDICES]
    else:
        raise ValueError(corr_mode, "is not a correlation mode")

def determine_size_correlations(base_dirs, mode):
    print("determine size correlations")
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
            try:
                tree_size = sizes_df[sizes_df["tree_name"] == tree_name].iloc[0]["num_tips"]
            except IndexError:
                continue
            sizes += len(df) * [tree_size]
            for index in INDICES:
                all_values[index] += [el for el in df[index]]
    df = pd.DataFrame()
    df["size"] = sizes 
    for index in INDICES:
        df[index] = all_values[index]
    for corr_mode in ["pearson", "spearman"]:
        corr_df["corr_" + corr_mode] = get_correlation(df, corr_mode, "")
    corr_df.to_csv("../data/general_output/size_correlations_" + mode + ".tsv", sep = "\t")


def gather_results(base_dirs, mode):
    print("gather results")
    all_results = []
    for base_dir in base_dirs:
        sizes_df = pd.read_csv(os.path.join(base_dir, "tree_sizes.tsv"), sep = "\t")
        sizes_df = sizes_df.astype({"tree_name": str})
        results_dir = os.path.join(base_dir, "treeshapy")
        for tree_name in util.unrooted_tree_names(base_dir):
            try:
                tree_size = sizes_df[sizes_df["tree_name"] == tree_name].iloc[0]["num_tips"]
            except IndexError:
                continue
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
    print("gather stats")
    stats = ["mean", "kurtosis", "kurtosis_int", "kurtosis_ext", "iqr", "iqr_int", "iqr_ext"]
    all_values = {}
    for stat in stats:
        all_values[stat] = {index : [] for index in INDICES}
    sizes = []
    for base_dir in base_dirs:
        sizes_df = pd.read_csv(os.path.join(base_dir, "tree_sizes.tsv"), sep = "\t")
        sizes_df = sizes_df.astype({"tree_name": str})
        stats_dir = os.path.join(base_dir, "stats")
        for tree_name in util.unrooted_tree_names(base_dir):
            df_path = os.path.join(stats_dir, tree_name + ".tsv")
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


def gather_unrooted_stats(base_dirs):
    print("gather stats")
    stats = ["unrooted_percentile"]
    all_values = {}
    for stat in stats:
        all_values[stat] = {index : [] for index in INDICES}
    sizes = []
    for base_dir in base_dirs:
        unrooted_stats_dir = os.path.join(base_dir, "unrooted_stats")
        for tree_name in util.unrooted_tree_names(base_dir):
            df_path = os.path.join(unrooted_stats_dir, tree_name + ".tsv")
            if not os.path.isfile(df_path):
                continue
            df = pd.read_csv(df_path, sep= "\t")
            if len(df) == 0:
                continue
            for index in INDICES_UNROOTED:
                for stat in stats:
                    all_values[stat][index].append(df[df["index"] == index].iloc[0][stat])
    for stat in stats:
        df = pd.DataFrame()
        for index in INDICES_UNROOTED:
            df[index] = all_values[stat][index]
        df.to_csv("../data/general_output/" + stat + ".tsv", sep = "\t")




base_dirs = ["../data/evonaps_dna", "../data/evonaps_aa", "../data/grove", "../data/grove_modificated"]
out_dir = os.path.join("../data/general_output")
if not os.path.isdir(out_dir):
    os.makedirs(out_dir)

determine_tree_sizes(base_dirs)
determine_max_min(base_dirs)

determine_stats(base_dirs)
gather_stats(base_dirs)

determine_database_correlations(base_dirs)

determine_unrooted_stats(base_dirs)
gather_unrooted_stats(base_dirs)

modes = ["absolute", "relative_max", "relative_tips", "relative_yule"]
for mode in modes:
    gather_results(base_dirs, mode)
    determine_size_correlations(base_dirs, mode)
