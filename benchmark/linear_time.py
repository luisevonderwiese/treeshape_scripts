import os
import matplotlib.pyplot as plt
from ete3 import Tree
from tabulate import tabulate
import numpy as np


def analyze(tree_name, python_dir):
    d = {}
    with open(os.path.join(python_dir, "precompute", tree_name + ".csv"), "r") as infile:
        lines = infile.readlines()
    names = lines[0][:-1].split(",")
    times = [float(s) for s in lines[1].split(",")]
    for i, name in enumerate(names):
        d[name] = times[i]
    return d

tree_dir = "../data/evonaps_dna/trees/rooted/"
python_dir = "../results/python/benchmark/evonaps_dna"

all_times = []
tree_sizes = []
for tree_name in os.listdir(tree_dir):
    print(tree_name)
    n = len(Tree(os.path.join(tree_dir, tree_name)))
    tree_sizes.append(n)
    times = analyze(tree_name, python_dir)
    full_time = sum([time for index, time in times.items()])
    all_times.append(full_time)

plt.figure(figsize=(20,20))
plt.scatter(tree_sizes, all_times, s=10)
plt.savefig("runtimes_full.png")
plt.clf()
plt.loglog(tree_sizes, all_times)
plt.savefig("runtimes_loglog.png")
        
