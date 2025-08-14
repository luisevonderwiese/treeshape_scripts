import os
import random
from ete3 import Tree

def root_trees(base_dir):
    unrooted_trees_dir = os.path.join(base_dir, "trees/unrooted")
    rooted_trees_dir = os.path.join(base_dir, "trees/rooted")
    for d in [rooted_trees_dir]:
        if not os.path.isdir(d):
            os.makedirs(d)

    for tree_name in os.listdir(unrooted_trees_dir):
        tree_name_x = ".".join(tree_name.split(".")[:-1])
        rooted_tree_path = os.path.join(rooted_trees_dir, tree_name_x + ".rooted.tree")
        if os.path.isfile(rooted_tree_path):
            continue
        unrooted_tree_path = os.path.join(unrooted_trees_dir, tree_name)
        tree = Tree(unrooted_tree_path)
        random_root = random.choice([node for node in tree.iter_descendants()])
        tree.set_outgroup(random_root)
        with open(rooted_tree_path, "w+") as outfile:
            outfile.write(tree.write())

root_trees("../data/evonaps_dna")
