from ete3 import Tree
import time
import os

from treeshape.treeshape import TreeShape
from treeshape.indexlists import INDICES

import treeshape.util as util


def profile(tree_dir, treename, results_dir):
    treepath = os.path.join(tree_dir, treename)
    tree =  Tree(treepath)
    times = {}
    for node in tree.iter_descendants():
        tree.set_outgroup(node)
        nwk = tree.write()
        rooted_tree = Tree(nwk)
        
        start = time.time()
        util.precompute_clade_sizes(rooted_tree)
        util.precompute_depths(rooted_tree)
        util.prcompute_nodes_below(rooted_tree)
        util.precompute_farness(rooted_tree)
        util.precompute_bcent(rooted_tree)
        end = time.time()
        precomputation_time = end - start

        ts = TreeShape(rooted_tree, "BINARY")

        times[node] = [precomputation_time]
        for index_name in INDICES:
            start = time.time()
            ts.absolute(index_name)
            end = time.time()
            times[node].append(end - start)
    
    if not os.path.isdir(results_dir):
            os.makedirs(results_dir)
    
    with open(os.path.join(results_dir, treename + ".csv"), "w+") as outfile:
        outfile.write(",".join(["precomputation"] + INDICES) + "\n")
        for node, node_times in times.items():
            outfile.write(",".join([str(node_time) for node_time in node_times]) + "\n")


tree_dir = "../data/evonaps_dna/trees/unrooted/"
results_dir = "../data/evonaps_dna/benchmark_new"

util.read_we()
for treename in os.listdir(tree_dir):
    print(treename)
    profile(tree_dir, treename, results_dir)

