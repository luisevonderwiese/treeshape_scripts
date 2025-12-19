import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../data/chamberlain/network_metrics.csv")
colless_df = pd.read_csv("../data/chamberlain/colless_index.csv")

df = pd.merge(df, colless_df, on = "dataset")

plots_dir = "../data/chamberlain/plots"

if not os.path.isdir(plots_dir):
    os.makedirs(plots_dir)

for metric in ["modularity", "nestedness", "connectance"]:
    plt.scatter(df["colless_index"], df[metric], s = 10)
    plt.xlabel("colless_index")
    plt.ylabel(metric)
    plt.savefig(os.path.join(plots_dir, metric + ".png"))
    plt.clf()
