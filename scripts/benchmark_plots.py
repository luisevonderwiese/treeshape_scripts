import os
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from treeshapy import INDICES
import util


def gather_times(base_dirs):
    times_python = {}
    times_R = {}
    for base_dir in base_dirs:
        sizes_df = pd.read_csv(os.path.join(base_dir, "tree_sizes.tsv"), sep = "\t")
        sizes_df = sizes_df.astype({"tree_name": str})
        python_dir = os.path.join(base_dir, "treeshapy")
        R_dir = os.path.join(base_dir, "treestats")
        for tree_name in util.unrooted_tree_names(base_dir):
            tree_size = sizes_df[sizes_df["tree_name"] == tree_name].iloc[0]["num_tips"]
            tree_size = tree_size // 10 + 5
            if not tree_size in times_R:
                times_R[tree_size] = [] 
                times_python[tree_size] = []

            try:
                times_python_df = pd.read_csv(os.path.join(python_dir, tree_name + "_times.tsv"), sep = "\t")
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

    R_df = pd.DataFrame(times_R.items(), columns = ["size", "time"])
    R_df.to_csv("../data/general_output/times_treestats.tsv", sep = "\t")

    python_df = pd.DataFrame(times_python.items(), columns = ["size", "time"])
    python_df.to_csv("../data/general_output/times_treeshapy.tsv", sep = "\t")


def plot_times():
    plots_dir = "../data/plots"
    if not os.path.isdir(plots_dir):
        os.makedirs(plots_dir)

    matplotlib.rcParams.update({'font.size': 8})
    times_R = pd.read_csv("../data/general_output/times_treestats.tsv", sep = "\t")
    times_python = pd.read_csv("../data/general_output/times_treeshapy.tsv", sep = "\t")
    plt.figure(figsize=(5.2 , 3))
    plt.plot(times_python["size"], times_python["time"], marker = "s", label = "treeshapy", lw  = 0.5, markersize = 2)
    plt.plot(times_R["size"], times_R["time"], marker = "s", label = "treestats", lw = 0.5, markersize = 2)
    plt.xlabel("tree size")
    plt.ylabel("run_time (sec)")
    util.add_fancy_legend()
    plt.savefig(os.path.join(plots_dir, "comparing_benchmark.eps"), dpi = 300, bbox_inches = "tight")
    plt.clf()

base_dirs = ["../data/evonaps_dna", "../data/evonaps_aa", "../data/grove"]

gather_times(base_dirs)
plot_times()





