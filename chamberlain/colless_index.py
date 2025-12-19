import os
from ete3 import Tree
import pandas as pd

from treeshapy.treeshapy import TreeShape


tree_dir = "../data/chamberlain/plant_trees/plant_trees"

res = []
for tree_name in os.listdir(tree_dir):
    short_name = tree_name.split(".")[0].split("_")[1]
    print(os.path.join(tree_dir, tree_name))
    tree = Tree(os.path.join(tree_dir, tree_name), format = 1)
    tree.resolve_polytomy(recursive=True)
    ts = TreeShape(tree, mode = "BINARY")
    c = ts.absolute("colless_index")
    res.append([short_name, c])

df = pd.DataFrame(res, columns = ["dataset", "colless_index"])
df.to_csv("../data/chamberlain/colless_index.csv")
