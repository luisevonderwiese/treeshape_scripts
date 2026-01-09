import os
from ete3 import Tree
import pandas as pd

from treeshapy.treeshapy import TreeShape

def colless(continent):
    tree_dir = os.path.join("../data/vos/trees/", continent)

    res = []
    for tree_name in os.listdir(tree_dir):
        short_name = tree_name.split(".")[0]
        print(os.path.join(tree_dir, tree_name))
        tree = Tree(os.path.join(tree_dir, tree_name), format = 1)
        if len([l for l in tree.iter_leaves()]) < 2:
            print(tree_name)
            continue
        tree.resolve_polytomy(recursive=True)
        ts = TreeShape(tree, mode = "BINARY")
        c = ts.relative_max("colless_index")
        res.append([short_name, c])

    df = pd.DataFrame(res, columns = ["dataset", "colless_index"])
    df.to_csv(os.path.join("../data/vos/" , continent + ".csv"))


colless("africa")
colless("southamerica")
