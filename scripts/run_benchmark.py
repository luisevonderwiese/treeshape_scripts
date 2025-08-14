from ete3 import Tree
import time
import os

from treeshape.treeshape import TreeShape
from treeshape.indexlists import INDICES

import treeshape.util as util


def profile(tree_dir, treename, results_dir):
    treepath = os.path.join(tree_dir, treename)
    tree =  Tree(treepath)
    start = time.time()
    util.precompute_clade_sizes(tree)
    util.precompute_depths(tree)
    end = time.time()
    precomputation_time = end - start
    tb = TreeShape(tree, "BINARY")

    times = [precomputation_time]
    for index_name in INDICES:
        print(index_name)
        start = time.time()
        tb.absolute(index_name)
        end = time.time()
        times.append(end - start)
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    with open(os.path.join(results_dir, treename + ".csv"), "w+") as outfile:
        outfile.write(",".join(["precomputation"] + INDICES) + "\n")
        outfile.write(",".join([str(time) for time in times]) + "\n")


tree_dir = "../data/evonaps_dna/trees/rooted/"
results_dir = "../data/evonaps_dna/benchmark"

for treename in os.listdir(tree_dir):
    profile(tree_dir, treename, results_dir)

