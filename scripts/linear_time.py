import os
import matplotlib.pyplot as plt
import pandas as pd

from treeshapy.treeshapy import INDICES
import util

def analyze(base_dir):
    plots_dir = os.path.join(base_dir, "plots")
    if not os.path.isdir(plots_dir):
        os.makedirs(plots_dir)
    python_dir = os.path.join(base_dir, "treeshapy")
    sizes_df = pd.read_csv(os.path.join(base_dir, "tree_sizes.tsv"), sep = "\t")
    times = []
    sizes = []
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

analyze("../data/evonaps_dna")






