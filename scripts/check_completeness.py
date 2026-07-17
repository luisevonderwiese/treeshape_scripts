import os
import time
from ete3 import Tree
from treeshapy.treeshapy import TreeShape, INDICES
import treeshapy.util as treeshapy_util
import pandas as pd
import util

def check(base_dir):
    rooted_trees_dir = os.path.join(base_dir, "trees/rooted")
    results_dir = os.path.join(base_dir, "treeshapy")
    
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    
    for tree_name in util.unrooted_tree_names(base_dir):
        times_path = os.path.join(results_dir, tree_name + "_times.tsv")
        no_precomp_times_path = os.path.join(results_dir, tree_name + "_times_no_precomp.tsv")
        aresults_path = os.path.join(results_dir, tree_name + "_absolute.tsv")
        rresults_max_path = os.path.join(results_dir, tree_name + "_relative_max.tsv")
        rresults_yule_path = os.path.join(results_dir, tree_name + "_relative_yule.tsv")
        rresults_tips_path = os.path.join(results_dir, tree_name + "_relative_tips.tsv")

        subdir = os.path.join(rooted_trees_dir, tree_name)
        if not os.path.isdir(subdir):
            print(subdir + " missing")
            continue
        num_rooted_trees = len([name for name in os.listdir(subdir)])

        for results_path in [times_path, aresults_path, rresults_max_path, rresults_yule_path, rresults_tips_path]:
            if not os.path.isfile(results_path):
                print(results_path + " missing")
                print(num_rooted_trees)
                continue
            df = pd.read_csv(results_path, sep = "\t")
            if len(df) != num_rooted_trees:
                diff = str(num_rooted_trees - len(df))
                print(diff + " rows missing in " + results_path)
                print(num_rooted_trees)
                os.remove(results_path)



#check("../data/evonaps_dna")
#check("../data/evonaps_aa")
#check("../data/evonaps_dna_big")
check("../data/grove_modificated")
check("../data/grove")
