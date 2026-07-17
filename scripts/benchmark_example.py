import os
import matplotlib.pyplot as plt
import pandas as pd

from treeshapy.treeshapy import INDICES
import util

base_dir = "../data/evonaps_dna"
sizes_df = pd.read_csv(os.path.join(base_dir, "tree_sizes.tsv"), sep = "\t")
sizes_df = sizes_df.astype({"tree_name": str})
tree_name = sizes_df[sizes_df["num_tips"] == 100].iloc[0]["tree_name"]
df_path = os.path.join(base_dir, "treeshapy", tree_name + "_times.tsv")
times_python = pd.read_csv(df_path, sep = "\t")
all_times = [(sum([row[index] for index in INDICES])) for _, row in times_python.iterrows()]
example_time = all_times[0]
print(all_times)






