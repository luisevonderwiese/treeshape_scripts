import os
import numpy as np
import pandas as pd
from tabulate import tabulate
from treeshapy.treeshapy import INDICES

modes = ["absolute", "relative_tips", "relative_max", "relative_yule"]
dfs = {}
for mode in ["absolute", "relative_tips", "relative_max", "relative_yule"]:
    df = pd.read_csv("../data/general_output/size_correlations_" + mode + ".tsv", sep = "\t")
    df = df.drop("Unnamed: 0", axis = 1)
    df = df.drop("corr_log", axis = 1)
    df = df.drop("corr_nlogn", axis = 1)
    df = df.drop("corr_quadratic", axis = 1)
    df = df.drop("corr_exp", axis = 1)
    dfs[mode] = df

INDICES = ["colless_index",
          "corrected_colless_index",
          "quadratic_colless_index",
          "I_2_index",
          "stairs2",
          "j1",
          "stairs1",
          "rogers_j_index",
          "symmetry_nodes_index",
          "mean_I",
          "total_I",
          "mean_I_prime",
          "total_I_prime",
          "mean_I_w",
          "total_I_w",
          "average_leaf_depth",
          "sackin_index",
          "total_path_length",
          "total_internal_path_length",
          "average_vertex_depth",
          "s_shape",
          "maximum_depth",
          "variance_of_leaves_depths",
          "B_1_index",
          "B_2_index" ,
          "maximum_width",
          "maxdiff_widths",
          "modified_maxdiff_widths",
          "max_width_over_max_depth",
          "d_index",
          "rooted_quartet_index",
          "ladder_length",
          "average_ladder",
          "cherry_index",
          "modified_cherry_index",
          "IL_number",
          "pitchforks",
          "four_caterpillars",
          "double_cherries",
          "total_cophenetic_index",
          "diameter",
          "area_per_pair_index",
          "wiener_index",
          "total_farness",
          "mean_bcent",
          "bcent_root",
          "maximum_farness",
          "minimum_bcent",
          "maximum_bcent",
          "bcent_variance",
          "maximum_closeness",
          "minimum_farness",
          "root_imbalance",
          "I_root"]


def colored_cell(v):
    if v != v:
        return "\cellcolor{gray!25} "
    if abs(v) < 0.3:
        return "\cellcolor{green!25}$" + str(round(v, 2)) + "$"
    if abs(v) > 0.7:
        return "\cellcolor{red!25}$" + str(round(v, 2)) + "$"
    return "\cellcolor{yellow!25}$" + str(round(v, 2)) + "$"


res = []
res_latex = []
for index in INDICES:
    res_row = [index]
    res_row_latex = ["\codeword{" + index + "}"]
    for mode in modes:
        df = dfs[mode]
        sub_df = df[df["index"] == index]
        if len(sub_df) == 0:
            v = float("nan")
        else:
            v = sub_df.iloc[0]["corr_linear"]
        res_row.append(v)
        res_row_latex.append(colored_cell(v))
    res.append(res_row)
    res_latex.append(res_row_latex)
tab = tabulate(res, headers = ["index"] + modes, tablefmt = "pipe")
print(tab)
tab = tabulate(res_latex, headers = ["index"] + modes, tablefmt = "latex_raw")
print(tab)


assert(False)

# other analyses (old)

for mode in modes:
    df = pd.read_csv("../data/general_output/size_correlations_" + mode + ".tsv", sep = "\t")
    res = []
    df = df.drop("Unnamed: 0", axis = 1)
    for i, row in df.iterrows():
        if not np.isnan(list(row.drop("index"))).all():
            res.append(list(row))
    tab = tabulate(res, headers = df.columns, tablefmt = "pipe")
    print(mode)
    print(tab)


for index in INDICES:
    res = []
    for mode in modes:
        df = dfs[mode]
        sub_df = df[df["index"] == index]
        if len(sub_df) == 0:
            continue
        row = sub_df.iloc[0]
        row2 = row.drop("index")
        if np.isnan(list(row2)).all():
            continue
        row2 = row2.astype("float")
        for k, v in row2.items():
            row2[k] = abs(v)
        m = row2.nlargest(1)
        max_key = m.keys()[0]
        max_val = row[max_key]
        res.append([mode, max_key, max_val])
    tab = tabulate(res, headers = ["mode", "corr_mode", "corr"], tablefmt = "pipe")
    print(index)
    print(tab)


res = []
for index in INDICES:
    res_row = [index]
    for mode in modes:
        df = dfs[mode]
        sub_df = df[df["index"] == index]
        if len(sub_df) == 0:
            continue
        row = sub_df.iloc[0].drop("index")
        all_nan = True
        all_low = True
        for k in row.keys():
            corr = row[k]
            if corr == corr:
                all_nan = False
                if abs(corr) > 0.3:
                    all_low = False
        if all_nan:
            res_row.append("0")
        elif all_low:
            res_row.append("1")
        else:
            res_row.append("(1)")
    res.append(res_row)
tab = tabulate(res, headers = ["index"] + modes, tablefmt = "pipe")
print(tab)

