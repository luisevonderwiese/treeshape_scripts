from ete3 import Tree
import os
import math
import unittest
import pandas as pd

from treeshape.treeshape import TreeShape

treebalance_indices = [
        "area_per_pair_index",
        "average_leaf_depth",
        "average_vertex_depth",
        "B_1_index",
        "B_2_index",
        "cherry_index",
        "colless_index",
        "corrected_colless_index",
        "quadratic_colless_index",
        # "colijn_plazotta_rank",
        "I_2_index",
        # "furnas_rank",
        "mean_I",
        "total_I",
        "mean_I_prime",
        "total_I_prime",
        "mean_I_w",
        "total_I_w",
        "maxdiff_widths",
        "modified_maxdiff_widths",
        "maximum_depth",
        "maximum_width",
        "modified_cherry_index",
        "max_width_over_max_depth",
        "rogers_j_index",
        "rooted_quartet_index",
        "sackin_index",
        "s_shape",
        "stairs1",
        "stairs2",
        "symmetry_nodes_index",
        "total_cophenetic_index",
        "total_internal_path_length",
        "total_path_length",
        "variance_of_leaves_depths",
        "d_index"]

class TestMetrics(unittest.TestCase):
    ref_dir = "../reference_results/treebalance/indices/evonaps_dna"
    tree_dir = "../data/evonaps_dna/trees/rooted"
    expected = {}
    for tree_name in os.listdir(tree_dir):
        print(tree_name)
        try:
            df = pd.read_csv(os.path.join(ref_dir, tree_name + ".csv"))
        except FileNotFoundError:
            print("no results found")
            continue
        results = {}
        for i, row in df.iterrows():
            results[row["names"]] = float(row["results"])
        expected[tree_name] = results

    def test(self):
        test_trees = {}
        for test_tree_name in os.listdir(self.tree_dir):
            if not test_tree_name in self.expected:
                continue
            tree = Tree(os.path.join(self.tree_dir, test_tree_name))
            tb_b = TreeShape(tree, "BINARY")
            tb_a = TreeShape(tree, "ARBITRARY")
            for index_name in treebalance_indices:
                print(index_name)
                try:
                    self.assertAlmostEqual(tb_b.absolute(index_name), self.expected[test_tree_name][index_name])
                except ValueError as e:
                    print(e)
                    self.assertAlmostEqual(tb_a.absolute(index_name), self.expected[test_tree_name][index_name])


if __name__ == '__main__':
    unittest.main()
