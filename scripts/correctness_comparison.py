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
    for tree_name in util.unrooted_tree_names(base_dir):
        results_python = pd.read_csv(os.path.join(python_dir, tree_name + "_absolute.tsv"), sep = "\t")
        results_R = pd.read_csv(os.path.join(R_dir, tree_name + "_absolute.tsv"), sep = "\t")
        relevant_indices = results_R.columns[3:]
        all_results = results_python.merge(results_R, on = "root", suffixes = ["_python", "_R"])
        for _, row in all_results.iterrows():
            for index in relevant_indices:
                if reference == "treestats" and index == "s_shape":
                    continue # different logarithms
                if reference == "treebalance" and index == "colijn_plazotta_rank":
                    continue # problems with big ints
                r_value = row[index + "_R"]
                p_value = row[index + "_python"]
                if isinstance(r_value, str):
                    try: 
                        r_value = int(r_value)
                        p_value = int(p_value)
                    except:
                        #print("Skipping large", index)
                        continue
                diff = abs(p_value - r_value)
                if diff > epsilon:
                    if not index in fail_counts:
                        fail_counts[index] = 0
                    fail_counts[index] += 1
                    if index == "j1":
                        #t = Tree(os.path.join(base_dir, "trees/rooted", tree_name, row["root_type_python"] + "_" + row["root"] + ".rooted.tree"))
                        #print(t.write())
                        #print(t)
                        #print(index)
                        print(row[index + "_python"])
                        print(row[index + "_R"])
                        #print(tree_name)
                        #print(row["root_type_python"])
                        #print(row["root"])
                        print("")

    print(fail_counts)


check("../data/evonaps_dna", "treestats")
check("../data/evonaps_dna", "treebalance")

