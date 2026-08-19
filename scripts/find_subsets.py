import os
import pandas as pd

from subsets import *


for i in range(2, 11):
    correlation_df = pd.read_csv("../data/general_output/database_correlations_spearman.tsv", sep = "\t", index_col = 0)
    correlation_df.drop('colijn_plazotta_rank', axis=1, inplace=True)
    correlation_df = correlation_df[correlation_df["index1"] != "colijn_plazotta_rank"]

    selected_indices = find_low_correlation_subset(correlation_df, i)
    print(selected_indices)

