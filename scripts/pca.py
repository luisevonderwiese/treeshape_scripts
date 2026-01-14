import os
import pandas as pd
from treeshapy.treeshapy import INDICES

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import util

def pca(mode):
    df = pd.read_csv("../data/general_output/all_results_" + mode + ".tsv", sep = "\t")
    X = df.drop('rooted_tree_name', axis=1)
    X = X.drop('tree_size', axis=1)
    X.replace([np.inf, -np.inf], np.nan, inplace=True)
    X.drop('colijn_plazotta_rank', axis=1, inplace=True)
    #X.drop('furnas_rank', axis=1, inplace=True)
    X.dropna(axis=0, inplace=True)
    print(X) 
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
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

modes = ["absolute", "relative_tips"]

color_props = ["tree_size", "sackin_index"]

for mode in modes:
    pca(mode)
    for color_prop in color_props:
        plot_pca(mode, color_prop)


