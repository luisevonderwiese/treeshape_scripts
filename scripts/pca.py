import os
import pandas as pd
from treeshapy.treeshapy import INDICES

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.decomposition import PCA

import util


import itertools
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence



def subset_score(subset, weights):
    return sum([weights[i][j] for i, j in itertools.combinations(subset, 2)])

# careful, not sure if an how this is working
def greedy_randomized_subset(weights, n, starts = 2000, seed = 1):
    rng = random.Random(seed)
    size = len(weights)
    best_subset: tuple[int, ...] | None = None
    best_score = math.inf

    start_nodes = list(range(size))
    for start_number in range(max(starts, size)):
        if start_number < size:
            subset = [start_nodes[start_number]]
        else:
            subset = [rng.randrange(size)]

        remaining = set(range(size))
        remaining.remove(subset[0])

        while len(subset) < n:
            candidates = []
            for candidate in remaining:
                proposed = subset + [candidate]
                candidates.append((subset_score(proposed, weights), candidate))
            candidates.sort(key=lambda item: item[0])

            # Take the best candidate most of the time, but sample among the top
            # few candidates on later starts to escape obvious local optima.
            if start_number < size:
                chosen = candidates[0][1]
            else:
                top_k = min(5, len(candidates))
                chosen = rng.choice(candidates[:top_k])[1]

            subset.append(chosen)
            remaining.remove(chosen)

        score = subset_score(subset, weights)
        if score < best_score:
            best_score = score
            best_subset = tuple(sorted(subset))

    assert best_subset is not None
    return best_subset, best_score


def find_low_correlation_subset(correlations, n):
    names = list(correlations["index1"])
    correlations.drop("index1", axis = 1, inplace = True)
    matrix = correlations.to_numpy().tolist()
    size = len(matrix)

    weights = [[abs(matrix[i][j]) for j in range(size)] for i in range(size)]

    best_subset: tuple[int, ...] | None = None
    best_score = math.inf
    for subset in itertools.combinations(range(size), n):
        score = subset_score(subset, weights)
        if score < best_score:
            best_score = score
            best_subset = subset
        assert best_subset is not None
    return [names[i] for i in best_subset]


def pca(mode):
    correlation_df = pd.read_csv("../data/general_output/database_correlations_spearman.tsv", sep = "\t", index_col = 0)
    correlation_df.drop('colijn_plazotta_rank', axis=1, inplace=True)
    correlation_df = correlation_df[correlation_df["index1"] != "colijn_plazotta_rank"]
    selected_indices = find_low_correlation_subset(correlation_df, 10)
    print(selected_indices)
    assert(False)
    #print(selected_indices)
    #selected_indices = ['variance_of_leaves_depths', 'B_2_index', 'maxdiff_widths', 'modified_maxdiff_widths', 'four_caterpillars', 'ladder_length', 'average_ladder', 'I_root', 'stairs1', 'I_2_index']
    #selected_indices = ['variance_of_leaves_depths', 'B_2_index', 'maxdiff_widths', 'max_width_over_max_depth', 'four_caterpillars', 'double_cherries', 'ladder_length', 'average_ladder', 'I_root', 'stairs1']
    selected_indices = ['B_1_index', 'B_2_index', 'maxdiff_widths', 'modified_maxdiff_widths', 'cherry_index', 'average_ladder', 'I_root', 'stairs1', 'mean_I_prime', 'mean_I_w']
    X = pd.read_csv("../data/general_output/all_results_" + mode + ".tsv", sep = "\t")
    print(X)
    to_drop = [x for x in X.columns if x not in selected_indices]
    for x in to_drop:
        X.drop(x, axis=1, inplace=True)
    X.replace([np.inf, -np.inf], np.nan, inplace=True)
    X.dropna(axis=0, inplace=True)
    scaler = RobustScaler()#StandardScaler()
    print(X)
    X_scaled = scaler.fit_transform(X)
    #X_log = np.log1p(X)   # only if values are >= 0
    #X_scaled = StandardScaler().fit_transform(X_log)
    #scaler = RobustScaler()
    #coords = PCA(n_components=5).fit_transform(X_scaled)
    #plt.scatter(coords[:, 1], coords[:, 2])  # PC2 vs PC3

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    print(pca.explained_variance_)
    print(pca.explained_variance_ratio_)
    pca_df = pd.DataFrame(X_pca, columns = ["pc1", "pc2"])
    pca_df.to_csv("../data/general_output/pca_" + mode + ".tsv", sep = "\t")

def plot_pca(mode, color_prop):
    X_pca = pd.read_csv("../data/general_output/pca_" + mode + ".tsv", sep = "\t")
    other_df = pd.read_csv("../data/general_output/all_results_" + mode + ".tsv", sep = "\t").filter([color_prop], axis=1)
    X_pca = X_pca.join(other_df)
    plt.figure(figsize=(20,20))
    plt.scatter(X_pca["pc1"], X_pca["pc2"], s=10, c=X_pca[color_prop], norm=matplotlib.colors.LogNorm())
    plt.colorbar()
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.savefig("../data/general_plots/pca_" + mode + "_" + color_prop + ".png")


def correlate_with_pca(mode, method="pearson", output_path=None):
    if method not in {"pearson", "spearman"}:
        raise ValueError('method must be "pearson" or "spearman"')
    all_results_path = "../data/general_output/all_results_" + mode + ".tsv"
    pca_path = "../data/general_output/pca_" + mode + ".tsv"

    all_results = pd.read_csv(all_results_path, sep="\t")
    pca_coords = pd.read_csv(pca_path, sep="\t")

    unnamed_columns = [c for c in pca_coords.columns if c.startswith("Unnamed:")]
    if unnamed_columns:
        pca_coords.drop(columns=unnamed_columns, inplace=True)

    
    row_count = min(len(all_results), len(pca_coords))
    if len(all_results) != len(pca_coords):
        print(
            "Warning: all-results and PCA files have different row counts; "
            f"using the first {row_count} rows by position."
        )

    all_results = all_results.iloc[:row_count].reset_index(drop=True)
    pca_coords = pca_coords.iloc[:row_count].reset_index(drop=True)

    numeric_results = all_results.select_dtypes(include=[np.number])
    rows = []
    for column in numeric_results.columns:
        values = numeric_results[column]
        pc1_corr = values.corr(pca_coords["pc1"], method=method)
        pc2_corr = values.corr(pca_coords["pc2"], method=method)
        abs_correlations = [abs(c) for c in [pc1_corr, pc2_corr] if not pd.isna(c)]
        rows.append(
            {
                "column": column,
                "pc1_correlation": pc1_corr,
                "pc2_correlation": pc2_corr,
                "max_abs_correlation": max(abs_correlations, default=np.nan),
            }
        )

    correlations = pd.DataFrame(rows)
    correlations.sort_values(
        "max_abs_correlation",
        ascending=False,
        inplace=True,
        na_position="last",
    )
    correlations.reset_index(drop=True, inplace=True)

    if output_path is not None:
        correlations.to_csv(output_path, sep="\t", index=False)
    else:
        print(correlations.to_string(index=False))

    return correlations


modes = ["absolute"]

#color_props = ["tree_size", "sackin_index"]
color_props = ["I_root", "B_1_index"]
for mode in modes:
    pca(mode)
    #correlate_with_pca(mode)
    for color_prop in color_props:
        plot_pca(mode, color_prop)


