import os
import shutil
import random
from ete3 import Tree

def root_trees(base_dir):
    unrooted_trees_dir = os.path.join(base_dir, "trees/unrooted")
    rooted_trees_dir = os.path.join(base_dir, "trees/rooted")
    for d in [rooted_trees_dir]:
        if not os.path.isdir(d):
            os.makedirs(d)
    for tree_name in os.listdir(unrooted_trees_dir):
        unrooted_tree_path = os.path.join(unrooted_trees_dir, tree_name)
        print(unrooted_tree_path)
        tree = Tree(unrooted_tree_path)
        tree_name_x = ".".join(tree_name.split(".")[:-1])
        rooted_trees_dir = os.path.join(base_dir, "trees/rooted", tree_name_x)
        if os.path.isdir(rooted_trees_dir):
            continue
        print(tree_name_x)
        os.makedirs(rooted_trees_dir)
        inner_root_id = 0
        for node in tree.iter_descendants():
            if node.is_leaf():
                root = node.name.replace("/", "").replace("_", "").replace(".", "")
                root_type = "external"
            else:
                root_type = "internal"
                root = str(inner_root_id)
                inner_root_id += 1

            tree.set_outgroup(node)
            
            rooted_tree_path = os.path.join(rooted_trees_dir, root_type + "_" + root + ".rooted.tree")
            with open(rooted_tree_path, "w+") as outfile:
                outfile.write(tree.write())


root_trees("../data/evonaps_dna")
root_trees("../data/evonaps_aa")
root_trees("../data/grove")
