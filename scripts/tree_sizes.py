import os
from ete3 import Tree
import pandas as pd


def determine_tree_sizes(base_dir):
    tree_dir = os.path.join(base_dir, "trees/unrooted/")
    data = []

    for tree_name in os.listdir(tree_dir):
        print(tree_name)
        n = len(Tree(os.path.join(tree_dir, tree_name)))
        tree_name_x = tree_name.split(".")
        data.append([tree_name_x, n])

    df = pd.DataFrame(data, colums = ["tree_name", "num_tips"])
    out_path = os.path.join(base_dir, "tree_size.tsv")
    df.to_csv(out_path, sep = "\t")


determine_tree_sizes("../data/evonaps_dna")

