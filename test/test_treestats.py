from ete3 import Tree
import os
import math
import unittest
import pandas as pd

from treeshape.treeshape import TreeShape

treestats_indices = [
         "average_leaf_depth",
          "variance_of_leaves_depths",
          "sackin_index",
          "total_path_length",
          "total_internal_path_length",
          "average_vertex_depth",
          "B_1_index",
          "B_2_index",
          "maximum_depth",
          "maximum_width",
          "modified_maxdiff_widths",
          "max_width_over_max_depth",
          "s_shape",
          "cherry_index",
          "total_cophenetic_index",
          "diameter",
          "area_per_pair_index",
          "root_imbalance",
          "colless_index",
          "corrected_colless_index",
          "quadratic_colless_index",
          "I_2_index",
          "stairs1",
          "stairs2",
          "rogers_j_index",
          "symmetry_nodes_index",
          "mean_I_prime",
          "rooted_quartet_index",
          "treeness",
          "ladder_length",
          "IL_number",
          "pitchforks",
          "four_caterpillars",
          "double_cherries"
          ] 

class TestMetrics(unittest.TestCase):
    ref_dir = "../refernce_results/treestats/indices/evonaps_dna" 
    tree_dir = "../data/evonaps_dna/trees/rooted"
    expected = {}
    for tree_name in os.listdir(tree_dir):
        print(tree_name)
        try:
            df = pd.read_csv(os.path.join(ref_dir, tree_name + ".csv"))
        except FileNotFoundError:
            continue
        results = {}
        for i, row in df.iterrows():
            results[row["names"]] = float(row["results"])
        expected[tree_name] = results

    def test(self):
        test_trees = {}
        for test_tree_name in os.listdir(self.tree_dir):
            print(test_tree_name)
            if not test_tree_name in self.expected:
                continue
            tree = Tree(os.path.join(self.tree_dir, test_tree_name))
            tb_b = TreeBalance(tree, "BINARY")
            tb_a = TreeBalance(tree, "ARBITRARY")
            for index_name in treestats_indices:
                if index_name == "s_shape":
                    continue #fails due to different base of logarithm
                if index_name == "variance_of_leaves_depths":
                    continue #population variance vs sample variance https://numpy.org/devdocs/reference/generated/numpy.var.html
                print(index_name)
                try:
                    self.assertAlmostEqual(tb_b.absolute(index_name), self.expected[test_tree_name][index_name])
                except ValueError as e:
                    print(e)
                    self.assertAlmostEqual(tb_a.absolute(index_name), self.expected[test_tree_name][index_name])


if __name__ == '__main__':
    unittest.main()

