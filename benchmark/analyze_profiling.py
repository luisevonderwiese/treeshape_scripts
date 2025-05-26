import os
import matplotlib.pyplot as plt
from ete3 import Tree
from tabulate import tabulate
import numpy as np


def analyze(tree_name, python_dir, R_dir):
    d = {}
    with open(os.path.join(python_dir, "no_precompute", tree_name + ".csv"), "r") as infile:
        lines = infile.readlines()
    names = lines[0][:-1].split(",")
    times = [float(s) for s in lines[1].split(",")]
    d["precomputation"] = {}
    d["precomputation"]["no_precompute"] = 0
    for i, name in enumerate(names):
        d[name] = {}
        d[name]["no_precompute"] = times[i]

    with open(os.path.join(python_dir, "precompute", tree_name + ".csv"), "r") as infile:
        lines = infile.readlines()
    names = lines[0][:-1].split(",")
    times = [float(s) for s in lines[1].split(",")]
    for i, name in enumerate(names):
        d[name]["precompute"] = times[i]

    with open(os.path.join(R_dir, tree_name + ".csv"), "r") as infile:
        lines = infile.readlines()
    d["precomputation"]["treestats"] = 0
    for line in lines[1:]:
        parts = line.split(",")
        name = parts[1].strip("\"")
        time = float(parts[2])
        d[name]["treestats"] = time
    #res = [[name] + [d[name][setup] for setup in ["no_precompute", "precompute", "treestats"]] for name in names]
    #print(tabulate(res, headers = ["metric", "no_precompute", "precompute", "treestats"], tablefmt="pipe", floatfmt=".6f"))
    return d

def boxplots(all_times, plots_dir):
    if not os.path.isdir(plots_dir):
        os.makedirs(plots_dir)
    for index, times in all_times.items():
        fig, ax = plt.subplots()
        data_matrix = [list(el) for el in times.values()]
        for i, data in enumerate(data_matrix):
            d = np.abs(data - np.median(data))
            mdev = np.median(d)
            s = d/mdev if mdev else np.zeros(len(d))
            data_matrix[i] = [el for j, el in enumerate(data) if s[j] < 2]
        ax.boxplot(data_matrix)
        ax.set_xticklabels(times.keys())
        plt.savefig(os.path.join(plots_dir, index + ".png"))

tree_dir = "../data/evonaps_dna/trees/rooted/"
python_dir = "../results/python/benchmark/evonaps_dna"
R_dir = "../results/treestats/benchmark/evonaps_dna"

all_times = {}
for tree_name in os.listdir(tree_dir):
    print(tree_name)
    n = len(Tree(os.path.join(tree_dir, tree_name)))
    times = analyze(tree_name, python_dir, R_dir)
    if len(all_times) == 0:
        for index, subtimes in times.items():
            all_times[index] = {}
            for mode, time in subtimes.items():
                all_times[index][mode] = [time / n]
    else:
        for index, subtimes in times.items():
            for mode, time in subtimes.items():
                all_times[index][mode].append(time / n)
res = []
for index, times in all_times.items():
    row = [index]
    for mode, time_arr in times.items():
        row.append(1000 * sum(time_arr) / len(time_arr))
    res.append(row)
print(tabulate(res, headers = ["metric", "no_precompute", "precompute", "treestats"], tablefmt="pipe", floatfmt=".8f"))

res = []
for index, times in all_times.items():
    row = [index]
    for mode, time_arr in times.items():
        row.append(max(time_arr))
    res.append(row)
print(tabulate(res, headers = ["metric", "no_precompute", "precompute", "treestats"], tablefmt="pipe", floatfmt=".8f"))


boxplots(all_times, "results/plots/benchmark/evonaps_dna")

        
