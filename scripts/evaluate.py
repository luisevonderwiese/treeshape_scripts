import os
import time
from ete3 import Tree
from treeshapy.treeshapy import TreeShape, INDICES
import treeshapy.util as treeshapy_util

import util

def evaluate_indices(base_dir):
    rooted_trees_dir = os.path.join(base_dir, "trees/rooted")
    results_dir = os.path.join(base_dir, "treeshapy")
    
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    
    for tree_name in util.unrooted_tree_names(base_dir):
        print(tree_name)
        times_path = os.path.join(results_dir, tree_name + "_times.tsv")
        aresults_path = os.path.join(results_dir, tree_name + "_absolute.tsv")
        rresults_path = os.path.join(results_dir, tree_name + "_relative.tsv")

        #if os.path.isfile(times_path) and os.path.isfile(aresults_path) and os.path.isfile(rresults_path):
        #    continue

        for results_path in [times_path, aresults_path, rresults_path]:
            header = ["root", "root_type"]
            if results_path == times_path:
                header.append("precomputation")
            header += INDICES
            with open(results_path, "w+") as outfile:
                outfile.write("\t".join(header))
                outfile.write("\n")

        subdir = os.path.join(rooted_trees_dir, tree_name)
        for name in os.listdir(subdir):
            tree_path = os.path.join(subdir, name)
            rooted_tree = Tree(tree_path)
            parts = name.split(".")[0].split("_")
            root = parts[1]
            root_type = parts[0]

            start = time.time()
            treeshapy_util.precompute_clade_sizes(rooted_tree)
            treeshapy_util.precompute_depths(rooted_tree)
            treeshapy_util.precompute_nodes_below(rooted_tree)
            treeshapy_util.precompute_farness(rooted_tree)
            treeshapy_util.precompute_bcent(rooted_tree)
            treeshapy_util.precompute_ladder_lengths(rooted_tree)
            end = time.time()
            precomputation_time = end - start

            ts = TreeShape(rooted_tree, "BINARY")
            
            times = [precomputation_time]
            for index_name in INDICES:
                start = time.time()
                ts.absolute(index_name)
                end = time.time()
                times.append(end - start)


            results_absolute = ts.all_absolute()
            results_relative = ts.all_relative()
            
            with open(times_path, "a") as outfile:
                outfile.write("\t".join([root, root_type]))
                outfile.write("\t")
                outfile.write("\t".join([str(time) for time in times]))
                outfile.write("\n")
            with open(aresults_path, "a") as outfile:
                outfile.write("\t".join([root, root_type]))
                outfile.write("\t")
                outfile.write("\t".join([str(results_absolute[index]) for index in INDICES]))
                outfile.write("\n")
            with open(rresults_path, "a") as outfile:
                outfile.write("\t".join([root, root_type]))
                outfile.write("\t")
                outfile.write("\t".join([str(results_relative[index]) for index in INDICES]))
                outfile.write("\n")

def evaluate_indices_no_precomp(base_dir):
    rooted_trees_dir = os.path.join(base_dir, "trees/rooted")
    results_dir = os.path.join(base_dir, "treeshapy")

    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)

    for tree_name in util.unrooted_tree_names(base_dir):
        print(tree_name)
        times_path = os.path.join(results_dir, tree_name + "_times_no_precomp.tsv")

        #if os.path.isfile(times_path):
        #    continue

        header = ["root", "root_type"] + INDICES
        with open(times_path, "w+") as outfile:
            outfile.write("\t".join(header))
            outfile.write("\n")

        subdir = os.path.join(rooted_trees_dir, tree_name)
        for name in os.listdir(subdir):
            tree_path = os.path.join(subdir, name)
            rooted_tree = Tree(tree_path)
            parts = name.split(".")[0].split("_")
            root = parts[1]
            root_type = parts[0]

            times = []
            for index_name in INDICES:
                ts = TreeShape(rooted_tree, "BINARY")
                start = time.time()
                ts.absolute(index_name)
                end = time.time()
                times.append(end - start)

            with open(times_path, "a") as outfile:
                outfile.write("\t".join([root, root_type]))
                outfile.write("\t")
                outfile.write("\t".join([str(time) for time in times]))
                outfile.write("\n")


evaluate_indices("../data/evonaps_dna")
evaluate_indices_no_precomp("../data/evonaps_dna")
#evaluate_indices("../data/evonaps_aa")
#evaluate_indices("../data/grove")
