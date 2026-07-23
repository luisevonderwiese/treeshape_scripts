import os
import shutil
import time
from ete3 import Tree
from treeshapy import TreeShape, INDICES, INDICES_UNROOTED
import treeshapy.util as treeshapy_util

import util

def evaluate_indices(d):

    rooted_trees_dir = os.path.join(d, "trees/rooted")
    results_dir = os.path.join(d, "treeshapy")
   
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    for tree_fn in os.listdir(rooted_trees_dir):
        print(tree_fn)
        tree_name = tree_fn.split(".")[0]
        results_path = os.path.join(results_dir, tree_name + ".tsv")

        #if os.path.isfile(results_path):
        #    continue

        with open(results_path, "w+") as outfile:
            outfile.write("\t".join(INDICES))
            outfile.write("\n")

        tree_path = os.path.join(rooted_trees_dir, tree_fn)
        rooted_tree = Tree(tree_path)

        ts = TreeShape(rooted_tree, "ARBITRARY")
            
        results_absolute = ts.all_absolute()

        
        with open(results_path, "a") as outfile:
            outfile.write("\t".join([str(results_absolute[index]) for index in INDICES]))
            outfile.write("\n")



evaluate_indices("../data/test_multi")
