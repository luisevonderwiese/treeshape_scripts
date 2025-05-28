import os
import numpy as np
import pandas as pd
from tabulate import tabulate
from ete3 import Tree
from treeshape.treeshape import TreeShape
from treeshape.indexlists import INDICES

def evaluate_indices(base_dir):
    unrooted_trees_dir = os.path.join(base_dir, "trees/unrooted")
    results_dir = os.path.join(base_dir, "rooting_variances")
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    for tree_name in os.listdir(unrooted_trees_dir):
        print(tree_name)
        unrooted_tree_path = os.path.join(unrooted_trees_dir, tree_name)
        results_path = os.path.join(results_dir, tree_name + ".tsv")
        with open(results_path, "w+") as outfile:
            outfile.write("newick" + "\t" + "root_type" + "\t")
            outfile.write("\t".join(INDICES))
            outfile.write("\n")
        tree = Tree(unrooted_tree_path)
        for node in tree.iter_descendants():
            tree.set_outgroup(node)
            nwk = tree.write()
            rooted_tree = Tree(nwk)
            ts = TreeShape(rooted_tree, "BINARY")
            results = ts.all_absolute()
            if node.is_leaf():
                root_type = "external"
            else:
                root_type = "internal"
            with open(results_path, "a") as outfile:
                outfile.write(nwk + "\t" + root_type + "\t")
                outfile.write("\t".join([str(results[index]) for index in INDICES]))
                outfile.write("\n")

def determine_variances(base_dir):
    results_dir = os.path.join(base_dir, "rooting_variances")
    variances = {}
    variances_internal = {}
    variances_external = {}
    for index in INDICES:
        variances[index] = []
        variances_internal[index] = []
        variances_external[index] = []
    for results_name in os.listdir(results_dir):
        results_internal = {}
        results_external = {}
        for index in INDICES:
            results_internal[index] = []
            results_external[index] = []
        df = pd.read_csv(os.path.join(results_dir, results_name), sep= "\t")
        for i, row in df.iterrows():
            if row["root_type"] == "external":
                for index in INDICES:
                    results_external[index].append(row[index])
            else:
                for index in INDICES:
                    results_internal[index].append(row[index])
        for index, res_list_internal in results_internal.items():
            res_list_external = results_external[index]
            variances_internal[index].append(np.var(res_list_internal))
            variances_external[index].append(np.var(res_list_external))
            variances[index].append(np.var(res_list_internal + res_list_external))
    table = [[index, 
              np.mean(variances[index]), 
              np.mean(variances_internal[index]), 
              np.mean(variances_external[index])]
             for index in INDICES]
    print(tabulate(table, headers = ["index", "var", "var_internal", "var_external"], tablefmt="pipe", floatfmt=".6f"))

    

evaluate_indices("../data/evonaps_dna")
determine_variances("../data/evonaps_dna")
