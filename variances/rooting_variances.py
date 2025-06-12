import os
import numpy as np
import pandas as pd
from tabulate import tabulate
from ete3 import Tree
import matplotlib.pyplot as plt
from treeshape.treeshape import TreeShape
from treeshape.indexlists import INDICES

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
            variances_internal[index].append(np.var(res_list_internal))
            variances_external[index].append(np.var(res_list_external))
            variances[index].append(np.var(res_list_internal + res_list_external))
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

    
def determine_correlations(base_dir):
    results_dir = os.path.join(base_dir, "rooting_variances")
    correlations = {}
    for index1 in INDICES:
        correlations[index1] = {}
        for index2 in INDICES:
            correlations[index1][index2] = []
    for results_name in os.listdir(results_dir):
        df = pd.read_csv(os.path.join(results_dir, results_name), sep= "\t")
        for index1 in INDICES:
            for index2 in INDICES:
                c = abs(df[index1].corr(df[index2]))
                correlations[index1][index2].append(c)
    heatmap = []
    for i, index1 in enumerate(INDICES):
        heatmap.append([])
        for j, index2 in enumerate(INDICES):
            heatmap[i].append(np.nanmean(correlations[index1][index2]))

    fig, ax = plt.subplots(figsize=(15, 15))
    im = ax.imshow(heatmap)
    fig.colorbar(im)
    ax.set_xticks(range(len(INDICES)), labels=INDICES, rotation=45, ha="right", rotation_mode="anchor")
    ax.set_yticks(range(len(INDICES)), labels=INDICES)
    plt.savefig("heatmap.png")

def determine_mean_correlations(base_dir):
    results_dir = os.path.join(base_dir, "rooting_variances")
    means = {}
    for index in INDICES:
        means[index] = []
    for results_name in os.listdir(results_dir):
        df = pd.read_csv(os.path.join(results_dir, results_name), sep= "\t")
        for index in INDICES:
            means[index].append(np.nanmean(df[index], dtype=np.float64))
    means_df = pd.DataFrame()
    for index in INDICES:
        means_df[index] = means[index]
    heatmap = []
    for i, index1 in enumerate(INDICES):
        heatmap.append([])
        for j, index2 in enumerate(INDICES):
            corr = abs(means_df[index1].corr(means_df[index2]))
            if corr != corr:
                print(index1)
                print(means_df[index1])
                print(index2)
                print(means_df[index2])
            heatmap[i].append(corr)

    fig, ax = plt.subplots(figsize=(15, 15))
    im = ax.imshow(heatmap)
    fig.colorbar(im)
    ax.set_xticks(range(len(INDICES)), labels=INDICES, rotation=45, ha="right", rotation_mode="anchor")
    ax.set_yticks(range(len(INDICES)), labels=INDICES)
    plt.savefig("heatmap_means.png")



evaluate_indices("../data/evonaps_dna")
determine_variances("../data/evonaps_dna")
determine_correlations("../data/evonaps_dna")
determine_mean_correlations("../data/evonaps_dna")

