import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
from treeshape.indexlists import INDICES

plotgroups = [
["mean_I",
"mean_I_prime",
"mean_I_w",
"stairs2",
"I_2_index",
"stemminess",
"corrected_colless_index"
],

["I_root",
"root_imbalance"
],

["stairs1",
"treeness",
],
["double_cherries",
"pitchforks",
"ladder_length",
"four_caterpillars"
],
[
"d_index",
"average_leaf_depth",
"average_vertex_depth"
],
[
"IL_number",
"diameter",
"cherry_index",
],
["colless_index",
"total_internal_path_length",
"sackin_index",
],
[
"total_I",
"total_I_prime",
"total_I_w",
],
[
"variance_of_leaves_depths",
"rogers_j_index",
"symmetry_nodes_index",
"s_shape",
],
[
"total_path_length",
"wiener_index",
"total_cophenetic_index",
"quadratic_colless_index",
],
[
"B_1_index",
"B_2_index",
"maximum_depth",
"maximum_width",
"maxdiff_widths",
"modified_maxdiff_widths",
"max_width_over_max_depth",
"modified_cherry_index",
"area_per_pair_index",
],
[
"colijn_plazotta_rank",
"furnas_rank",
],
[
"rooted_quartet_index",
],
[
"rogers_j_index",
"modified_maxdiff_widths",
"cherry_index",
"area_per_pair_index",
"diameter",
"corrected_colless_index"
],
[
"mean_I",
"quadratic_colless_index",
"rooted_quartet_index"
],



]

def plot(base_dir, name):
    results_dir = os.path.join(base_dir, "rooting_variances")
    df = pd.read_csv(os.path.join(results_dir, name), sep= "\t")
    df = df.sort_values('root_type')
    max_values = {}
    plot_dir = os.path.join("plots", name.split(".")[0])
    if not os.path.isdir(plot_dir):
        os.makedirs(plot_dir)
    for i, plotgroup in enumerate(plotgroups):
        plt.figure(figsize=(20,20))
        for index in plotgroup:
            values = df[index]
            plt.scatter(range(len(values)), values, label = index)
        plt.legend()
        plt.savefig(os.path.join(plot_dir, "scatter_" + str(i)  +  ".png"))
        plt.clf()


def plot_means(base_dir, limit):
    results_dir = os.path.join(base_dir, "rooting_variances_relative")
    means = {}
    for index in INDICES:
        means[index] = []
    for results_name in os.listdir(results_dir)[:limit]:
        df = pd.read_csv(os.path.join(results_dir, results_name), sep= "\t")
        for index in INDICES:
            means[index].append(np.nanmean(df[index], dtype=np.float64))
    plt.figure(figsize=(20,20))
    cnt = 0
    for index in INDICES:
        if not np.isnan(means[index]).all():
            values = df[index]
            plt.scatter(range(len(values)), values, s = 10, label = index)
            cnt += 1
        if cnt == 10:
            plt.legend()
            plt.savefig("scatter_means_0.png")
            plt.figure(figsize=(20,20))
    plt.legend()
    plt.savefig("scatter_means_1.png")



#plot("../data/evonaps_dna", "M46800.nwk.tsv")
plot_means("../data/evonaps_dna", 100)
