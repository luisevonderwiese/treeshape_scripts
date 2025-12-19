import os
import pandas as pd
from statistics import median
from tabulate import tabulate
import numpy as np
import matplotlib.pyplot as plt
import seaborn

import util

def select_trees(base_dirs):
    sizes = []
    for base_dir in base_dirs:
        sizes_df = pd.read_csv(os.path.join(base_dir, "tree_sizes.tsv"), sep = "\t")
        results_dir = os.path.join(base_dir, "treeshapy")
        for tree_name in util.unrooted_tree_names(base_dir):
            df_path = os.path.join(results_dir, tree_name + "_absolute.tsv")
            if not os.path.isfile(df_path):
                continue
            df = pd.read_csv(df_path, sep= "\t")
            if len(df) == 0:
                continue
            tree_size = sizes_df[sizes_df["tree_name"] == tree_name].iloc[0]["num_tips"]
            sizes.append([tree_name, tree_size])
    df = pd.DataFrame(sizes, columns = ["name", "tree_size"])



    tree_sizes = list(df["tree_size"])
    min_size = min(tree_sizes)
    max_size = max(tree_sizes)
    med_size = median(tree_sizes)

    min_tree = df[df["tree_size"] == min_size].iloc[0]["name"]
    max_tree = df[df["tree_size"] == max_size].iloc[0]["name"]
    med_tree = df[df["tree_size"] == med_size].iloc[0]["name"]

    res = [
            ["min", min_tree, min_size],
            ["max", max_tree, med_size],
            ["med", med_tree, med_size]
            ]

    print(tabulate(res, headers = ["", "tree", "n"], tablefmt = "pipe"))


def plot_size_correlations(selected_indices):
    plots_dir = "../data/plots_selected"
    if not os.path.isdir(plots_dir):
        os.makedirs(plots_dir)
    for mode in ["absolute", "relative_max", "relative_yule", "relative_tips"]:
        data = []
        df = pd.read_csv("../data/general_output/all_results_" + mode + ".tsv", sep = "\t")
        plt.figure(figsize=(20, 10))
        for index in selected_indices:
            data.append(df[index])
            plt.scatter(df["tree_size"], df[index], label = index, s = 10)
        plt.legend(loc = "upper left")
        plt.xlabel("tree size n")
        plt.ylabel("index values")
        plt.yscale("log")
        plt.savefig(os.path.join(plots_dir, "size_correlation_scatter_" + mode + ".png"))
        plt.clf()
        plt.figure(figsize=(20, 10))
        if mode in ["absolute", "relative_tips"]:
            ax = seaborn.stripplot(data = data, log_scale=True)
        else:
            ax = seaborn.stripplot(data = data)
        ax.set_xticklabels(selected_indices)
        plt.xticks(rotation=90)
        plt.xlabel("index")
        plt.ylabel("value")
        plt.savefig(os.path.join(plots_dir, "values_database_" + mode + ".png"), bbox_inches='tight')
        plt.clf()


def plot_distributions(base_dir, selected_trees, selected_indices):
    plots_dir = "../data/plots_selected"
    if not os.path.isdir(plots_dir):
        os.makedirs(plots_dir)
    modes = ["absolute", "relative_max", "relative_yule", "relative_tips"]
    results_dir = os.path.join(base_dir, "treeshapy")
    for tree_name in selected_trees:
        res = []
        for mode in modes:
            data = []
            df_path = os.path.join(results_dir, tree_name + "_" + mode + ".tsv")
            print(df_path)
            if not os.path.isfile(df_path):
                data.append([])
                continue
            df = pd.read_csv(df_path, sep= "\t")
            for index in selected_indices:
                values = list(df[index])
                mean = np.nanmean(values)
                var = np.nanvar(values)
                if mode == "absolute":
                    res.append([index, mean, var, var/mean])
                data.append(values)
            plt.figure(figsize=(20, 10))
            if mode in ["absolute", "relative_tips"]:
                ax = seaborn.stripplot(data = data, log_scale=True)
            else:
                ax = seaborn.stripplot(data = data)
            ax.set_xticklabels(selected_indices)
            plt.xticks(rotation=90)
            plt.xlabel("index")
            plt.ylabel("value")
            plt.savefig(os.path.join(plots_dir, "values_" + tree_name + "_" + mode + ".png"), bbox_inches='tight')
            plt.clf()
        print(tabulate(res, headers = ["index", "mean", "var", "cv"], tablefmt = "latex"))


#select_trees(["../data/evonaps_dna"])
#selected_trees = ["PF04533", "ENSG00000154229_PRKCA"]

selected_trees = ["ENSG00000154229_PRKCA"]
selected_indices = ["sackin_index", "colless_index", "cherry_index", "root_imbalance"]

#plot_distributions("../data/evonaps_dna", selected_trees, selected_indices)
plot_size_correlations(selected_indices)
