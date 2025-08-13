import os
import numpy as np
import pandas as pd
from tabulate import tabulate
from ete3 import Tree
import matplotlib.pyplot as plt
from treeshape.treeshape import TreeShape
from treeshape.indexlists import INDICES
from collections import Counter

import seaborn

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




def evaluate_indices(base_dir):
    unrooted_trees_dir = os.path.join(base_dir, "trees/unrooted")
    results_dir = os.path.join(base_dir, "rooting_variances_relative")
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    for tree_name in os.listdir(unrooted_trees_dir):
        print(tree_name)
        unrooted_tree_path = os.path.join(unrooted_trees_dir, tree_name)
        results_path = os.path.join(results_dir, tree_name + ".tsv")
        if os.path.isfile(results_path):
            continue
        with open(results_path, "w+") as outfile:
            outfile.write("newick" + "\t" + "root_type" + "\t")
            outfile.write("\t".join(INDICES))
            outfile.write("\n")
        tree = Tree(unrooted_tree_path)
        for node in tree.iter_descendants():
            tree.set_outgroup(node)
            nwk = tree.write()
            rooted_tree = Tree(nwk)
            ts = TreeShape(rooted_tree, "BINARY")
            results = ts.all_relative()
            if node.is_leaf():
                root_type = "external"
            else:
                root_type = "internal"
            with open(results_path, "a") as outfile:
                outfile.write(nwk + "\t" + root_type + "\t")
                outfile.write("\t".join([str(results[index]) for index in INDICES]))
                outfile.write("\n")

def tree_sizes(base_dir):
    unrooted_trees_dir = os.path.join(base_dir, "trees/unrooted")
    sizes = []
    for tree_name in os.listdir(unrooted_trees_dir):
        print(tree_name)
        unrooted_tree_path = os.path.join(unrooted_trees_dir, tree_name)
        tree = Tree(unrooted_tree_path)
        sizes.append(len(tree))
    hist, bins, _ = plt.hist(sizes, bins=30)
    logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
    plt.clf()
    plt.hist(sizes, bins=logbins)
    plt.xscale("log")
    plt.savefig("tree_sizes.png")



def determine_max_min(base_dir):
    results_dir = os.path.join(base_dir, "rooting_variances")
    mins = {}
    maxs = {}
    for index in INDICES:
        mins[index] = 1000000
        maxs[index] = 0
    for results_name in os.listdir(results_dir):
        df = pd.read_csv(os.path.join(results_dir, results_name), sep= "\t")
        for index in INDICES:
            mins[index] = min(mins[index], min(df[index]))
            maxs[index] = max(maxs[index], max(df[index]))
    results = []
    for index in INDICES:
        results.append([index, mins[index], maxs[index]])
    print(tabulate(results, headers=["index", "min", "max"], tablefmt="pipe", floatfmt=".6f"))


def determine_variances(base_dir):
    results_dir = os.path.join(base_dir, "rooting_variances_relative")
    variances = {}
    variances_internal = {}
    variances_external = {}
    means = {}
    for index in INDICES:
        variances[index] = []
        variances_internal[index] = []
        variances_external[index] = []
        means[index] = []
    for results_name in os.listdir(results_dir):
        results_internal = {}
        results_external = {}
        for index in INDICES:
            results_internal[index] = []
            results_external[index] = []
        df = pd.read_csv(os.path.join(results_dir, results_name), sep= "\t")
        for index in INDICES:
            means[index].append(np.nanmean(df[index], dtype=np.float64))
        for i, row in df.iterrows():
            if row["root_type"] == "external":
                for index in INDICES:
                    results_external[index].append(row[index])
            else:
                for index in INDICES:
                    results_internal[index].append(row[index])
        for index, res_list_internal in results_internal.items():
            res_list_external = results_external[index]
            variances_internal[index].append(np.nanvar(res_list_internal))
            variances_external[index].append(np.nanvar(res_list_external))
            variances[index].append(np.nanvar(res_list_internal + res_list_external))
    table = [[index, 
              np.mean(variances[index]), 
              np.mean(variances_internal[index]), 
              np.mean(variances_external[index]),
              np.var(means[index])]
             for index in INDICES]
    headers = ["index", "var", "var_internal", "var_external", "var_means"]
    print(tabulate(table, headers = headers, tablefmt="pipe", floatfmt=".6f"))
    with open("variances.txt", "w+") as outfile:
        outfile.write(tabulate(table, headers = headers, tablefmt="pipe", floatfmt=".6f"))

    with open("variances.tsv", "w+") as outfile:
        outfile.write(tabulate(table, headers = headers, tablefmt="tsv", floatfmt=".6f"))

    
def determine_database_variances(base_dir):
    results_dir = os.path.join(base_dir, "rooting_variances_relative")
    all_values = {}
    for index in INDICES:
        all_values[index] = []
    for results_name in os.listdir(results_dir):
        df = pd.read_csv(os.path.join(results_dir, results_name), sep= "\t")
        for index in INDICES:
            all_values[index] += list(df[index])
    table = [[index, np.var(all_values[index])] for index in INDICES]
    headers = ["index", "database_var"]
    print(tabulate(table, headers = headers, tablefmt="pipe", floatfmt=".6f"))
    with open("variances_database.txt", "w+") as outfile:
        outfile.write(tabulate(table, headers = headers, tablefmt="pipe", floatfmt=".6f"))

    with open("variances_database.tsv", "w+") as outfile:
        outfile.write(tabulate(table, headers = headers, tablefmt="tsv", floatfmt=".6f"))

def determine_alternative_database_variances(base_dir):
    results_dir = os.path.join(base_dir, "rooting_variances_relative")
    all_values = {}
    for index in INDICES:
        all_values[index] = []
    for results_name in os.listdir(results_dir):
        df = pd.read_csv(os.path.join(results_dir, results_name), sep= "\t")
        for index in INDICES:
            all_values[index].append(np.mean(df[index]))

    table = [[index, np.nanvar(all_values[index])] for index in INDICES]
    headers = ["index", "database_var"]
    print(tabulate(table, headers = headers, tablefmt="pipe", floatfmt=".6f"))
    with open("variances_database_alternative.txt", "w+") as outfile:
        outfile.write(tabulate(table, headers = headers, tablefmt="pipe", floatfmt=".6f"))

    with open("variances_database_alternative.tsv", "w+") as outfile:
        outfile.write(tabulate(table, headers = headers, tablefmt="tsv", floatfmt=".6f"))


def tidy_up():
    with open("variances_database_alternative.tsv", "r") as infile:
        lines = infile.readlines()
    data = []
    for line in lines:
        line = line.replace("\n", "")
        line = line.replace(" ", "")
        line =  line.split("\t")
        data.append(line)
    df = pd.DataFrame(data[1:], columns = data[0])
    print(df)
    df.to_csv("variances_database_alternative_new.tsv", sep = "\t")

def determine_relative_variances():
    rerooting_df = pd.read_csv("variances_new.tsv", sep = "\t")
    database_df = pd.read_csv("variances_database_alternative_new.tsv", sep = "\t")
    print(database_df)
    print(rerooting_df)
    results = []
    for index in INDICES:
        database_var = database_df[database_df["index"] == index]["database_var"].iloc[0]
        if database_var != database_var:
            continue
        rerooting_var = rerooting_df[rerooting_df["index"] == index]["var"].iloc[0]
        rerooting_var_internal = rerooting_df[rerooting_df["index"] == index]["var_internal"].iloc[0]
        rerooting_var_external = rerooting_df[rerooting_df["index"] == index]["var_external"].iloc[0]
        results.append([index,
                        rerooting_var / database_var,
                        rerooting_var_internal / database_var,
                        rerooting_var_external / database_var])
    headers = ["index", "relative var", "relative var int", "relative var ext"]
    print(tabulate(results, headers = headers, tablefmt="pipe", floatfmt=".6f"))


def plot_relative_variances(base_dir):
    results_dir = os.path.join(base_dir, "rooting_variances_relative")
    rerooting_df = pd.read_csv("variances_new.tsv", sep = "\t")
    database_df = pd.read_csv("variances_database_alternative_new.tsv", sep = "\t")
    selected_indices = ["sackin_index", "maximum_depth", "cherry_index", "rogers_j_index", "root_imbalance", "B_2_index"]
    database_vars = {}
    for index in selected_indices:
        database_var = database_df[database_df["index"] == index]["database_var"].iloc[0]
        if database_var == database_var:
            database_vars[index] = database_var

    results = {}
    modes = ["mean", "rooting_var", "rooting_var_internal", "rooting_var_external", "rel_var", "rel_var_external", "rel_var_internal"]
    for mode in modes:
        results[mode] = {}
        for index in selected_indices:
            if index not in database_vars:
                continue
            results[mode][index] = []
    for results_name in os.listdir(results_dir):
        df = pd.read_csv(os.path.join(results_dir, results_name), sep= "\t")
        for index in selected_indices:
            if not index in database_vars:
                continue
            v = np.var(df[index])
            results["mean"][index].append(np.mean(df[index]))
            results["rooting_var"][index].append(v)
            relative_var = v / database_vars[index]
            results["rel_var"][index].append(relative_var)
            v = np.var(df[df["root_type"] == "external"][index])
            results["rooting_var_external"][index].append(v)
            relative_var = v / database_vars[index]
            results["rel_var_external"][index].append(relative_var)
            v = np.var(df[df["root_type"] == "internal"][index])
            results["rooting_var_internal"][index].append(v)
            relative_var = v / database_vars[index]
            results["rel_var_internal"][index].append(relative_var)

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
        elif mode.startswith("rooting_var"):
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
 
        plt.savefig(mode + ".png", bbox_inches='tight')


def determine_correlations(base_dir):
    index_list = GROUPS_ROOTING
    list_name = "groups_rooting"
    results_dir = os.path.join(base_dir, "rooting_variances")
    correlations = {}
    for index1 in index_list:
        correlations[index1] = {}
        for index2 in index_list:
            correlations[index1][index2] = []
    for results_name in os.listdir(results_dir):
        df = pd.read_csv(os.path.join(results_dir, results_name), sep= "\t")
        for index1 in index_list:
            for index2 in index_list:
                c = abs(df[index1].corr(df[index2]))
                correlations[index1][index2].append(c)
    heatmap = []
    for i, index1 in enumerate(index_list):
        heatmap.append([])
        for j, index2 in enumerate(index_list):
            mean_c = np.nanmean(correlations[index1][index2])
            if mean_c >= 0.95:
                print(index1, index2, str(mean_c))
            heatmap[i].append(np.nanmean(correlations[index1][index2]))

    fig, ax = plt.subplots(figsize=(15, 15))
    im = ax.imshow(heatmap)
    fig.colorbar(im)
    ax.set_xticks(range(len(index_list)), labels=index_list, rotation=45, ha="right", rotation_mode="anchor")
    ax.set_yticks(range(len(index_list)), labels=index_list)
    plt.savefig("heatmap_" + list_name + ".png")

def determine_mean_correlations(base_dir):
    index_list = GROUPS_STRICT
    list_name = "groups_strict"
    results_dir = os.path.join(base_dir, "rooting_variances")
    means = {}
    for index in index_list:
        means[index] = []
    for results_name in os.listdir(results_dir):
        df = pd.read_csv(os.path.join(results_dir, results_name), sep= "\t")
        for index in index_list:
            means[index] += [el for el in df[index]]
    means_df = pd.DataFrame()
    for index in index_list:
        print(index)
        means_df[index] = means[index]
    heatmap = []
    for i, index1 in enumerate(index_list):
        heatmap.append([])
        for j, index2 in enumerate(index_list):
            corr = abs(means_df[index1].corr(means_df[index2]))
            heatmap[i].append(corr)

    fig, ax = plt.subplots(figsize=(15, 15))
    im = ax.imshow(heatmap)
    fig.colorbar(im)
    ax.set_xticks(range(len(index_list)), labels=index_list, rotation=45, ha="right", rotation_mode="anchor")
    ax.set_yticks(range(len(index_list)), labels=index_list)
    plt.savefig("heatmap_means_" + list_name + ".png")


#tree_sizes("../data/evonaps_dna")
#evaluate_indices("../data/evonaps_dna")
#determine_variances("../data/evonaps_dna")
#determine_database_variances("../data/evonaps_dna")
#determine_alternative_database_variances("../data/evonaps_dna")
#tidy_up()
#determine_relative_variances()
#determine_max_min("../data/evonaps_dna")

plot_relative_variances("../data/evonaps_dna")
#determine_correlations("../data/evonaps_dna")
#determine_mean_correlations("../data/evonaps_dna")

