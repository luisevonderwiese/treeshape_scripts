import os
import time
import multiprocessing
import copy
import shutil
from ete3 import Tree
from treeshapy import TreeShape, INDICES
import treeshapy.util as treeshapy_util

import util


INDICES_UNROOTED = ["diameter",
          "area_per_pair_index",
          "wiener_index",
          "maximum_closeness",
          "minimum_farness",
          "maximum_farness",
          "total_farness",
          "minimum_bcent",
          "maximum_bcent",
          "mean_bcent",
          "bcent_variance"]

def evaluate_indices_unrooted(params):
    base_dir = params[0]
    tree_name = params[1]
    tree_name_short = tree_name.split(".")[0]

    unrooted_trees_dir = os.path.join(base_dir, "trees/unrooted")

    aresults_path = os.path.join(results_dir, tree_name_short + "_unrooted_absolute.tsv")
    rresults_tips_path = os.path.join(results_dir, tree_name_short + "_unrooted_relative_tips.tsv")

    if os.path.isfile(aresults_path) and os.path.isfile(rresults_tips_path):
        return
    for results_path in [aresults_path, rresults_tips_path]:
        header = INDICES_UNROOTED
        with open(results_path, "w+") as outfile:
            outfile.write("\t".join(header))
            outfile.write("\n")

    tree_path = os.path.join(unrooted_trees_dir, tree_name)
    tree = Tree(tree_path)

    ts = TreeShape(tree, binary = True, rooted = False)

    results_absolute = ts.evaluate("all")
    print(results_absolute)
    results_relative_tips = ts.evaluate("all", "REL_TIPS")

    with open(aresults_path, "a") as outfile:
        outfile.write("\t".join([str(results_absolute[index]) for index in INDICES_UNROOTED]))
        outfile.write("\n")

    with open(rresults_tips_path, "a") as outfile:
        outfile.write("\t".join([str(results_relative_tips[index]) for index in INDICES_UNROOTED]))
        outfile.write("\n")



def evaluate_indices(params):
    base_dir = params[0]
    tree_name = params[1]
    
    rooted_trees_dir = os.path.join(base_dir, "trees/rooted")
    results_dir = os.path.join(base_dir, "treeshapy")
    
    
    times_path = os.path.join(results_dir, tree_name + "_times.tsv")
    aresults_path = os.path.join(results_dir, tree_name + "_absolute.tsv")
    rresults_max_path = os.path.join(results_dir, tree_name + "_relative_max.tsv")
    rresults_yule_path = os.path.join(results_dir, tree_name + "_relative_yule.tsv")
    rresults_tips_path = os.path.join(results_dir, tree_name + "_relative_tips.tsv")

    if os.path.isfile(times_path) and os.path.isfile(aresults_path) and os.path.isfile(rresults_max_path) and os.path.isfile(rresults_yule_path) and os.path.isfile(rresults_tips_path):
        return
    print(tree_name)
    return
    for results_path in [times_path, aresults_path, rresults_max_path, rresults_yule_path, rresults_tips_path]:
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

        ts = TreeShape(rooted_tree, binary = True, rooted = True)
            
        times = [precomputation_time]
        for index_name in INDICES:
            start = time.time()
            ts.evaluate(index_name)
            end = time.time()
            times.append(end - start)


        results_absolute = ts.evaluate("all")
        results_relative_max = ts.evaluate("all", "REL_MAX")
        results_relative_yule = ts.evaluate("all", "REL_YULE")
        results_relative_tips = ts.evaluate("all", "REL_TIPS")
            
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
        with open(rresults_max_path, "a") as outfile:
            outfile.write("\t".join([root, root_type]))
            outfile.write("\t")
            outfile.write("\t".join([str(results_relative_max[index]) for index in INDICES]))
            outfile.write("\n")
        with open(rresults_yule_path, "a") as outfile:
            outfile.write("\t".join([root, root_type]))
            outfile.write("\t")
            outfile.write("\t".join([str(results_relative_yule[index]) for index in INDICES]))
            outfile.write("\n")
        with open(rresults_tips_path, "a") as outfile:
            outfile.write("\t".join([root, root_type]))
            outfile.write("\t")
            outfile.write("\t".join([str(results_relative_tips[index]) for index in INDICES]))
            outfile.write("\n")


def evaluate_indices_no_precomp(params):
    base_dir = params[0]
    tree_name = params[1]
    rooted_trees_dir = os.path.join(base_dir, "trees/rooted")

    times_path = os.path.join(results_dir, tree_name + "_times_no_precomp.tsv")

    if os.path.isfile(times_path):
        return
    print(tree_name)
    header = ["root", "root_type"] + INDICES
    with open(times_path, "w+") as outfile:
        outfile.write("\t".join(header))
        outfile.write("\n")

    subdir = os.path.join(rooted_trees_dir, tree_name)
    for name in os.listdir(subdir):
        tree_path = os.path.join(subdir, name)
        rooted_tree = Tree(tree_path)
        parts = ".".join(name.split(".")[:-1]).split("_")
        root = "_".join(parts[1:])
        root_type = parts[0]

        times = []
        for index_name in INDICES:
            current_tree = copy.deepcopy(rooted_tree)
            ts = TreeShape(current_tree, binary = True, rooted = True)
            start = time.time()
            ts.evaluate(index_name)
            end = time.time()
            times.append(end - start)

        with open(times_path, "a") as outfile:
            outfile.write("\t".join([root, root_type]))
            outfile.write("\t")
            outfile.write("\t".join([str(time) for time in times]))
            outfile.write("\n")

base_dirs = ["../data/grove"]
for base_dir in base_dirs:
    print(base_dir)
    results_dir = os.path.join(base_dir, "treeshapy")
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)

    tree_names = [(base_dir, tree_name) for tree_name in util.unrooted_tree_names(base_dir)]
    tree_paths = [(base_dir, tree_name) for tree_name in os.listdir(os.path.join(base_dir, "trees/unrooted"))]
    #tree_names = ['65402', '65459', '61374', '65915', '51508', '65947', '65216', '43451', '40037', '65924', '65914', '65948', '63626']
    #tree_paths = ['65402.newick', '65459.newick', '61374.newick', '65915.newick', '51508.newick', '65947.newick', '65216.newick', '43451.newick', '40037.newick', '65924.newick', '65914.newick', '65948.newick', '63626.newick']
    #tree_names = [(base_dir, n) for n in tree_names]
    #tree_paths = [(base_dir, n) for n in tree_paths]
    num_cpu = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_cpu - 4)
    #pool = multiprocessing.Pool(13)
    #pool.map(evaluate_indices_unrooted, tree_paths)
    pool.map(evaluate_indices, tree_names)
        



