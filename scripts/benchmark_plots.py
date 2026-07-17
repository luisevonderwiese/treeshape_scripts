import os
import matplotlib.pyplot as plt
import pandas as pd

from treeshapy.treeshapy import INDICES
import util

def linear_time(base_dirs):
    plots_dir = "../data/plots"
    if not os.path.isdir(plots_dir):
        os.makedirs(plots_dir)
    
    times_dict = {}

    for base_dir in base_dirs:
        sizes_df = pd.read_csv(os.path.join(base_dir, "tree_sizes.tsv"), sep = "\t")
        sizes_df = sizes_df.astype({"tree_name": str})
        python_dir = os.path.join(base_dir, "treeshapy")
        for tree_name in util.unrooted_tree_names(base_dir):
            df_path = os.path.join(python_dir, tree_name + "_times.tsv")
            if not os.path.isfile(df_path):
                continue
            times_python = pd.read_csv(df_path, sep = "\t")
            if len(times_python) == 0:
                continue
            tree_size = sizes_df[sizes_df["tree_name"] == tree_name].iloc[0]["num_tips"]
            tree_size = tree_size // 10 + 5
            if not tree_size in times_dict:
                times_dict[tree_size] = []
            times_dict[tree_size] += [(sum([row[index] for index in INDICES])) for _, row in times_python.iterrows()]

    for size, size_times in times_dict.items():
        if len(size_times) > 0: 
            v = sum(size_times) / len(size_times)
        else: 
            v = float("nan")
        if size == 100:
            print(v)
        times_dict[size] = v
    times_dict = dict(sorted(times_dict.items()))


    plt.figure(figsize=(20,20))
    plt.scatter(times_dict.keys(), times_dict.values(), s=10)
    plt.xlabel("tree size")
    plt.ylabel("run_time")
    plt.savefig(os.path.join(plots_dir, "linear_time.png"))
    plt.clf()


def comparison_plots(base_dirs, reference, suffix):
    plots_dir = "../data/plots"
    if not os.path.isdir(plots_dir):
        os.makedirs(plots_dir)
    
    times_python = {}
    times_R = {}
    for base_dir in base_dirs:
        sizes_df = pd.read_csv(os.path.join(base_dir, "tree_sizes.tsv"), sep = "\t")
        sizes_df = sizes_df.astype({"tree_name": str})
        python_dir = os.path.join(base_dir, "treeshapy_clean")
        R_dir = os.path.join(base_dir, reference)
        for tree_name in util.unrooted_tree_names(base_dir):
            tree_size = sizes_df[sizes_df["tree_name"] == tree_name].iloc[0]["num_tips"]
            tree_size = tree_size // 10 + 5
            if not tree_size in times_R:
                times_R[tree_size] = [] 
                times_python[tree_size] = []

            try:
                times_python_df = pd.read_csv(os.path.join(python_dir, tree_name + "_times" + suffix + ".tsv"), sep = "\t")
                times_R_df = pd.read_csv(os.path.join(R_dir, tree_name + "_times.tsv"), sep = "\t")
            except Exception as e:
                print(e)
                continue
            relevant_indices = list(times_R_df.columns[3:])
            times_R[tree_size] += [sum([row[index] for index in relevant_indices]) for  _, row in times_R_df.iterrows()]
            times_python[tree_size] += [sum([row[index] for index in relevant_indices]) for  _, row in times_python_df.iterrows()]

    
    for times_dict in [times_R, times_python]:
        for size, size_times in times_dict.items():
            if len(size_times) > 0:
                v = sum(size_times) / len(size_times)
            else:
                v = float("nan") 
            times_dict[size] = v
    times_R = dict(sorted(times_R.items()))
    times_python = dict(sorted(times_python.items()))

    plt.figure(figsize=(20,20))
    plt.plot(times_python.keys(), times_python.values(), marker = "s", label = "treeshapy")
    plt.plot(times_R.keys(), times_R.values(), marker = "s", label = reference)
    plt.xlabel("tree size")
    plt.ylabel("run_time (sec)")
    util.add_fancy_legend()
    plt.savefig(os.path.join(plots_dir, "comparing_benchmark_" + reference + suffix + ".png"))
    plt.clf()

base_dirs = ["../data/evonaps_dna", "../data/evonaps_aa", "../data/grove", "../data/grove_modificated"]

#linear_time(base_dirs)
comparison_plots(base_dirs, "treestats", "")
#comparison_plots(base_dirs, "treebalance", "")
#comparison_plots(base_dirs, "treestats", "_no_precomp")
#comparison_plots(base_dirs, "treebalance", "_no_precomp")





