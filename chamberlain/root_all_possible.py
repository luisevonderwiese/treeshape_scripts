import os
import random
from ete3 import Tree

def root_trees():
    unrooted_trees_dir = os.path.join("../data/chamberlain/plant_trees/plant_trees")
    rooted_trees_base_dir = os.path.join("../data/chamberlain/plant_trees_rooted")
    if not os.path.isdir(rooted_trees_base_dir):
        os.makedirs(rooted_trees_base_dir)

    for tree_name in os.listdir(unrooted_trees_dir):
        unrooted_tree_path = os.path.join(unrooted_trees_dir, tree_name)
        tree = Tree(unrooted_tree_path, format = 1)
        tree.resolve_polytomy(recursive = True)
        tree_name_x = tree_name.split(".")[0].split("_")[1]
        print(tree_name_x)
        rooted_trees_dir = os.path.join(rooted_trees_base_dir, tree_name_x)
        if not os.path.isdir(rooted_trees_dir):
            os.makedirs(rooted_trees_dir)

        inner_root_id = 0
        for node in tree.iter_descendants():
            if node.is_leaf():
                root = node.name.replace("/", "").replace("_", "")
                root_type = "external"
            else:
                root_type = "internal"
                root = str(inner_root_id)
                inner_root_id += 1

            tree.set_outgroup(node)
            
            rooted_tree_path = os.path.join(rooted_trees_dir, root_type + "_" + root + ".rooted.tree")
            with open(rooted_tree_path, "w+") as outfile:
                outfile.write(tree.write())


root_trees()
