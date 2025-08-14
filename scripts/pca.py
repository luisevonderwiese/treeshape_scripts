import os
import pandas as pd
from treeshape.indexlists import INDICES

import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def gather_results(base_dir):
    results_dir = os.path.join(base_dir, "rooting_variances")
    all_results = {}
    all_results["name"] = []
    for index in INDICES:
        all_results[index] = []
    
    for results_name in os.listdir(results_dir):
        print(results_name)
        df = pd.read_csv(os.path.join(results_dir, results_name), sep= "\t")
        short_name = results_name.split(".")[0]
        all_results["name"] += [short_name + "_" + str(i) for i in range(len(df))]
        for index in INDICES:
            all_results[index] += list(df[index])
    all_df = pd.DataFrame(all_results)
    all_df.to_csv(os.path.join(base_dir, "all_results.tsv"), sep = "\t")

def pca(base_dir):
    df = pd.read_csv(os.path.join(base_dir, "all_results.tsv"), sep = "\t")
    X = df.drop('name', axis=1)
    X.replace([np.inf, -np.inf], np.nan, inplace=True)
    X.drop('colijn_plazotta_rank', axis=1, inplace=True)
    X.drop('furnas_rank', axis=1, inplace=True)
    X.dropna(axis=0, inplace=True)
   
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    pca_df = pd.DataFrame(X_pca, columns = ["pc1", "pc2"])
    pca_df.to_csv(os.path.join(base_dir, "pca.tsv"), sep = "\t")

def plot_pca(base_dir):
    X_pca = pd.read_csv(os.path.join(base_dir, "pca.tsv"), sep = "\t")
    plt.figure(figsize=(20,20))
    plt.scatter(X_pca["pc1"], X_pca["pc2"], s=10)
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.savefig("../plots/pca.png")

#gather_results("../data/evonaps_dna")
#pca("../data/evonaps_dna")
plot_pca("../data/evonaps_dna")

