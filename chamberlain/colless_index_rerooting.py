import os
from ete3 import Tree
import pandas as pd

from treeshapy.treeshapy import TreeShape


tree_dir = "../data/chamberlain/plant_trees_rooted"

res = []
for unrooted_tree_name in os.listdir(tree_dir):
    rooted_tree_dir = os.path.join(tree_dir, unrooted_tree_name)
    for tree_name in os.listdir(rooted_tree_dir):
        parts = tree_name.split(".")[0].split("_")
        root = parts[1]
        root_type = parts[0]

        short_name = tree_name.split(".")[0].split("_")[1]
        tree = Tree(os.path.join(rooted_tree_dir, tree_name), format = 1)
        ts = TreeShape(tree, mode = "BINARY")
        c = ts.absolute("colless_index")
        res.append([unrooted_tree_name, root, root_type, c])

df = pd.DataFrame(res, columns = ["dataset", "root", "root_type", "colless_index"])
df.to_csv("../data/chamberlain/colless_index_rooted.csv")
