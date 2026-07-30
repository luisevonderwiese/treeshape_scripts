import os
import pandas as pd
from treeshapy import INDICES

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression



import util
import subsets


def pca():
    correlation_df = pd.read_csv("../data/general_output/database_correlations_spearman.tsv", sep = "\t", index_col = 0)
    correlation_df.drop('colijn_plazotta_rank', axis=1, inplace=True)
    correlation_df = correlation_df[correlation_df["index1"] != "colijn_plazotta_rank"]
    #selected_indices = subsets.find_low_correlation_subset(correlation_df, 10)
    #print(selected_indices)
    selected_indices = ['B_1_index', 'B_2_index', 'maxdiff_widths', 'modified_maxdiff_widths', 'cherry_index', 'average_ladder', 'I_root', 'stairs1', 'mean_I_prime', 'mean_I_w']
    X = pd.read_csv("../data/general_output/all_results_absolute.tsv", sep = "\t")
    to_drop = [x for x in X.columns if x not in selected_indices + ["tree_size"]]
    for x in to_drop:
        X.drop(x, axis=1, inplace=True)
    X.replace([np.inf, -np.inf], np.nan, inplace=True)
    X.dropna(axis=0, inplace=True)
    scaler = RobustScaler()#StandardScaler()
    X_scaled = pd.DataFrame(
    scaler.fit_transform(X),
    columns=X.columns,
    index=X.index
    )

    size = X_scaled[["tree_size"]]      # DataFrame with one column
    X_scaled.drop(columns="tree_size", inplace = True)
    reg = LinearRegression().fit(size, X_scaled)
    R = X_scaled - reg.predict(size)

    print(type(X_scaled))
    print(X_scaled.shape)
    print(type(size))
    print(size.shape)
    print(type(R))
    print(R.shape)

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(R)
    print(pca.explained_variance_)
    print(pca.explained_variance_ratio_)
    pca_df = pd.DataFrame(X_pca, columns = ["pc1", "pc2"])
    pca_df.to_csv("../data/general_output/pca_size.tsv", sep = "\t")

def plot_pca(color_prop):
    X_pca = pd.read_csv("../data/general_output/pca.tsv", sep = "\t")
    other_df = pd.read_csv("../data/general_output/all_results_absolute.tsv", sep = "\t").filter([color_prop], axis=1)
    X_pca = X_pca.join(other_df)
    plt.figure(figsize=(20,20))
    plt.scatter(X_pca["pc1"], X_pca["pc2"], s=10, c=X_pca[color_prop], norm=matplotlib.colors.LogNorm())
    plt.colorbar()
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.savefig("../data/plots/pca_" + color_prop + ".png")

def plot_indices(index1, index2):
    df = pd.read_csv("../data/general_output/all_results_absolute.tsv", sep = "\t")
    plt.figure(figsize=(20,20))
    plt.scatter(df[index1], df[index2], c=df["tree_size"], s=10)
    plt.xlabel(index1)
    plt.ylabel(index2)
    plt.savefig("../data/plots/" + index1 + "_" + index2 + ".png")



def correlate_with_pca(method="pearson", output_path=None):
    if method not in {"pearson", "spearman"}:
        raise ValueError('method must be "pearson" or "spearman"')
    all_results_path = "../data/general_output/all_results_absolute.tsv"
    pca_path = "../data/general_output/pca_size.tsv"

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



#plot_indices("I_root", "B_1_index")
#plot_indices("I_root", "tree_size")
#plot_indices("maximum_width", "stairs1")
#assert(False)

color_props = ["I_root", "B_1_index"]
pca()
correlate_with_pca()
assert(False)
for color_prop in color_props:
    plot_pca(color_prop)


