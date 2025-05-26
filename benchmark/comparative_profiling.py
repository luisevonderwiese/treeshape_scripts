from ete3 import Tree
import time
import os

from treeshape.treeshape import TreeShape
import treeshape.indexlists as indexlists
import treeshape.util as util


def profile(tree_dir, treename, results_dir):
    treepath = os.path.join(tree_dir, treename)
    times = []
    for index_name in indexlists.treestats_indices:
        print(index_name)
        tree =  Tree(treepath)
        tb = TreeShape(tree, "BINARY")
        start = time.time()
        tb.absolute(index_name)
        end = time.time()
        times.append(end - start)
    if not os.path.isdir(os.path.join(results_dir, "no_precompute")):
        os.makedirs(os.path.join(results_dir, "no_precompute"))
    with open(os.path.join(results_dir, "no_precompute", treename + ".csv"), "w+") as outfile:
        outfile.write(",".join(indexlists.treestats_indices) + "\n")
        outfile.write(",".join([str(time) for time in times]) + "\n")


    tree =  Tree(treepath)
    start = time.time()
    util.precompute_clade_sizes(tree)
    util.precompute_depths(tree)
    end = time.time()
    precomputation_time = end - start
    tb = TreeShape(tree, "BINARY")

    times = [precomputation_time]
    for index_name in indexlists.treestats_indices:
        print(index_name)
        start = time.time()
        tb.absolute(index_name)
        end = time.time()
        times.append(end - start)
    if not os.path.isdir(os.path.join(results_dir, "precompute")):
        os.makedirs(os.path.join(results_dir, "precompute"))
    with open(os.path.join(results_dir, "precompute", treename + ".csv"), "w+") as outfile:
        outfile.write(",".join(["precomputation"] + indexlists.treestats_indices) + "\n")
        outfile.write(",".join([str(time) for time in times]) + "\n")


tree_dir = "data/evonaps_dna/trees/rooted/"
results_dir = "results/python/benchmark/evonaps_dna"

for treename in os.listdir(tree_dir)[:10]:
    profile(tree_dir, treename, results_dir)

