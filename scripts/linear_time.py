import os
import matplotlib.pyplot as plt
from ete3 import Tree
from tabulate import tabulate
import numpy as np


def analyze(tree_name, results_dir):
    d = {}
    with open(os.path.join(results_dir, tree_name + ".csv"), "r") as infile:
        lines = infile.readlines()
    names = lines[0][:-1].split(",")
    times = [float(s) for s in lines[1].split(",")]
    for i, name in enumerate(names):
        d[name] = times[i]
    return d

tree_dir = "../data/evonaps_dna/trees/rooted/"
results_dir = "../data/evonaps_dna/benchmark"
plots_dir = "../plots"

all_times = []
tree_sizes = []
for tree_name in os.listdir(tree_dir):
    print(tree_name)
    n = len(Tree(os.path.join(tree_dir, tree_name)))
    tree_sizes.append(n)
    times = analyze(tree_name, results_dir)
    full_time = sum([time for index, time in times.items()])
    all_times.append(full_time)

plt.figure(figsize=(20,20))
plt.scatter(tree_sizes, all_times, s=10)
if not os.path.isdir(plots_dir):
    os.makedirs(plots_dir)
plt.savefig(os.path.join(plots_dir, "runtimes_full.png"))
        
