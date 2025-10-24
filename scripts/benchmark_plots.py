import os
import matplotlib.pyplot as plt
import pandas as pd

from treeshapy.treeshapy import INDICES
import util

def linear_time(base_dirs):
    plots_dir = "../data/general_plots"
    if not os.path.isdir(plots_dir):
        os.makedirs(plots_dir)
    
    times = []
    sizes = []

    for base_dir in base_dirs:
        sizes_df = pd.read_csv(os.path.join(base_dir, "tree_sizes.tsv"), sep = "\t")
        python_dir = os.path.join(base_dir, "treeshapy")
        for tree_name in util.unrooted_tree_names(base_dir):
            tree_size = sizes_df[sizes_df["tree_name"] == tree_name].iloc[0]["num_tips"]
            times_python = pd.read_csv(os.path.join(python_dir, tree_name + "_times.tsv"), sep = "\t")
            for i, row in times_python.iterrows():
                sizes.append(tree_size)
                times.append(sum([row[index] for index in INDICES]))

    plt.figure(figsize=(20,20))
    plt.scatter(sizes, times, s=10)
    plt.xlabel("tree size")
    plt.ylabel("run_time")
    plt.savefig(os.path.join(plots_dir, "linear_time.png"))
    plt.clf()


def comparison_plots(base_dirs, reference, suffix):
    plots_dir = os.path.join("../data/general_plots", "comparing_benchmark_" + reference + suffix)
    if not os.path.isdir(plots_dir):
        os.makedirs(plots_dir)
    
    times_python = {}
    times_R = {}
    for base_dir in base_dirs:
        sizes_df = pd.read_csv(os.path.join(base_dir, "tree_sizes.tsv"), sep = "\t")
        python_dir = os.path.join(base_dir, "treeshapy")
        R_dir = os.path.join(base_dir, reference)
        for tree_name in util.unrooted_tree_names(base_dir):
            tree_size = sizes_df[sizes_df["tree_name"] == tree_name].iloc[0]["num_tips"]
            times_python_df = pd.read_csv(os.path.join(python_dir, tree_name + "_times" + suffix + ".tsv"), sep = "\t")
            times_R_df = pd.read_csv(os.path.join(R_dir, tree_name + "_times.tsv"), sep = "\t")
            for index in times_R_df.columns[3:]:
                if not index in times_R:
                    times_R[index] = {}
                    times_python[index] = {}
                if not tree_size in times_R[index]:
                    times_R[index][tree_size] = []
                    times_python[index][tree_size] = []
                times_R[index][tree_size] += list(times_R_df[index])
                times_python[index][tree_size] += list(times_python_df[index])
    
    for times_dict in [times_R, times_python]:
        for index, index_times in times_dict.items():
            for size, size_times in index_times.items():
                index_times[size] = sum(size_times) / len(size_times)
            times_dict[index] = dict(sorted(index_times.items()))

    for index, index_times_R in times_R.items():
        print(index)
        plt.figure(figsize=(20,20))
        plt.plot(index_times_R.keys(), index_times_R.values(), marker = "s", label = reference)
        index_times_python = times_python[index]
        plt.plot(index_times_python.keys(), index_times_python.values(), marker = "s", label = "treeshapy")
        plt.xlabel("tree size")
        plt.ylabel("run_time")
        util.add_fancy_legend()
        plt.savefig(os.path.join(plots_dir, index + ".png"))
        plt.clf()
        plt.close()
    print("")

base_dirs = ["../data/evonaps_dna"]

linear_time(base_dirs)
comparison_plots(base_dirs, "treestats", "")
comparison_plots(base_dirs, "treebalance", "")
comparison_plots(base_dirs, "treestats", "_no_precomp")
comparison_plots(base_dirs, "treebalance", "_no_precomp")





