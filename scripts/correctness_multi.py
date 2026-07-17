import os
import sys
import pandas as pd
from ete3 import Tree

import util

epsilon = 0.001

sys.set_int_max_str_digits(110000)

def check(base_dir, reference):
    python_dir = os.path.join(base_dir, "treeshapy")
    R_dir = os.path.join(base_dir, reference)
    fail_counts = {}
    for tree_fn in os.listdir(os.path.join(base_dir, "trees/rooted")):
        tree_name = tree_fn.split(".")[0]
        results_python = pd.read_csv(os.path.join(python_dir, tree_name + ".tsv"), sep = "\t")
        results_R = pd.read_csv(os.path.join(R_dir, tree_name + "_absolute.tsv"), sep = "\t")
        relevant_indices = results_R.columns[3:]
        for index in relevant_indices:
            R_value = results_R[index].iloc[0]
            python_value = results_python[index].iloc[0]
            diff = abs(python_value - R_value)
            if diff > epsilon:
                if index == "four_caterpillars":
                    tree_path = os.path.join(base_dir, "trees/rooted", tree_fn)
                    print(tree_path)
                    t = Tree(tree_path)
                    print(t)
                    print(R_value)
                    print(python_value)
                    print("..............................")
                if not index in fail_counts:
                    fail_counts[index] = 0
                fail_counts[index] += 1
    print(fail_counts)

check("../test/test_multi", "treestats")

