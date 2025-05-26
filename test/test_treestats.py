from ete3 import Tree
import os
import math
import unittest
import pandas as pd

from treeshape.treeshape import TreeShape
import treeshape.indexlists as indexlists




class TestMetrics(unittest.TestCase):
    ref_dir = "../results/treestats/metrics/evonaps_dna" 
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
            for index_name in indexlists.treestats_indices:
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

