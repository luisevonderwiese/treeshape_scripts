import os
import math
import random

from ete3 import Tree


def sample_tip_count(mean, variance, min_tips=2, rng=None):
    rng = rng or random
    sd = math.sqrt(variance)

    while True:
        n_tips = round(rng.gauss(mean, sd))
        if n_tips >= min_tips:
            return n_tips


def split_integer(n, k, rng=None):
    rng = rng or random
    cuts = sorted(rng.sample(range(1, n), k - 1))

    parts = []
    previous = 0
    for cut in cuts:
        parts.append(cut - previous)
        previous = cut

    parts.append(n - previous)
    return parts


def sample_multifurcating_tree(
    n_tips,
    max_children=5,
    multifurcation_prob=0.5,
    rng=None,
):
    rng = rng or random

    leaf_names = [f"t{i + 1}" for i in range(n_tips)]
    rng.shuffle(leaf_names)

    def build_subtree(names):
        if len(names) == 1:
            leaf = Tree()
            leaf.name = names[0]
            return leaf

        max_k = min(max_children, len(names))
        if max_k > 2 and rng.random() < multifurcation_prob:
            n_children = rng.randint(3, max_k)
        else:
            n_children = 2

        subtree_sizes = split_integer(len(names), n_children, rng=rng)

        node = Tree()

        start = 0
        for size in subtree_sizes:
            child_names = names[start : start + size]
            start += size
            node.add_child(build_subtree(child_names))

        return node

    tree = build_subtree(leaf_names)
    tree.set_outgroup(tree.children[0])
    tree.name = ""
    tree.dist = 0.0
    return tree


def count_multifurcations(tree):
    return sum(
        1
        for node in tree.traverse()
        if not node.is_leaf() and len(node.children) > 2
    )

def count_inner_nodes(tree):
    return sum(1 for node in tree.traverse() if not node.is_leaf())

def multifurcating_inner_node_ratio(tree):
    inner_nodes = count_inner_nodes(tree)
    if inner_nodes == 0:
        return 0.0

    return count_multifurcations(tree) / inner_nodes


def average_multifurcating_inner_node_ratio(trees):
    trees = list(trees)
    if not trees:
        return 0.0

    return sum(multifurcating_inner_node_ratio(tree) for tree in trees) / len(trees)

def sample_multifurcating_trees(
    n_trees,
    mean,
    variance,
    min_tips=4,
    max_children=5,
    multifurcation_prob=0.5,
    seed=None,
    outdir = ""
):
    if variance < 0:
        raise ValueError("variance must be non-negative")
    if min_tips < 1:
        raise ValueError("min_tips must be at least 1")
    if max_children < 2:
        raise ValueError("max_children must be at least 2")
    if not 0 <= multifurcation_prob <= 1:
        raise ValueError("multifurcation_prob must be between 0 and 1")

    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    rng = random.Random(seed)
    trees = []

    for tree_id in range(n_trees):
        n_tips = sample_tip_count(
            mean=mean,
            variance=variance,
            min_tips=min_tips,
            rng=rng,
        )
        tree = sample_multifurcating_tree(
            n_tips=n_tips,
            max_children=max_children,
            multifurcation_prob=multifurcation_prob,
            rng=rng,
        )
        trees.append(tree)
        tree.write(outfile = os.path.join(outdir, "sample_" + str(tree_id) + ".tree"))

    return trees


sampled_trees = sample_multifurcating_trees(
        n_trees=200,
        mean=20,
        variance=20,
        max_children=5,
        multifurcation_prob=0.5,
        seed=123,
        outdir = "test_multi/trees/rooted"
    )
print(
        "average multifurcating inner node ratio:",
        average_multifurcating_inner_node_ratio(sampled_trees),
)
