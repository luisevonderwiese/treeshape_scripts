IMBALANCE = [
        "variance_of_leaves_depths",

        "maximum_depth",
        "average_leaf_depth",
        "average_vertex_depth",

        "colless_index",
        "sackin_index",
        "total_path_length",
        "total_internal_path_length",
        "s_shape",
        "rogers_j_index",
        "symmetry_nodes_index",
        "total_I",
        "total_I_prime",
        "total_I_w",
        "total_cophenetic_index",
        "quadratic_colless_index",

        "mean_I",
        "mean_I_prime",
        "mean_I_w",
        "I_2_index",
        "stairs1",

        "corrected_colless_index",

        #"colijn_plazotta_rank"
        ]

BALANCE = [
        "B_1_index",
        "B_2_index",
        "maximum_width",
        "modified_maxdiff_widths",
        "max_width_over_max_depth",
        "rooted_quartet_index",
        "stairs2",
        "furnas_rank"
        ]



def plot_against_size(base_dirs, selected_indices, stat, suffix = ""):
    plots_dir = "../data/general_plots/" + stat + "_size"
    if not os.path.isdir(plots_dir):
        os.makedirs(plots_dir)

    df = pd.read_csv(os.path.join("../data/general_output/" + stat + ".tsv"), sep = "\t")
    sizes = list(set(df["size"]))
    sizes.sort()
    plt.figure(figsize=(20, 10))
    for index in selected_indices:
        avg_stat = [np.mean(df[df["size"] == size][index]) for size in sizes]
        plt.scatter(sizes, avg_stat, label = index, s = 10)
        plt.plot(sizes, avg_stat)
    plt.legend(loc = "upper left")
    plt.xlabel("tree size n")
    plt.ylabel(stat)
    #plt.yscale("log")
    plt.savefig(os.path.join(plots_dir, "size_" + stat + suffix + ".png"))
    plt.clf()


def plot_size_correlations(selected_indices, mode, suffix = ""):
    plots_dir = "../data/general_plots/size_correlations"
    if not os.path.isdir(plots_dir):
        os.makedirs(plots_dir)
    df = pd.read_csv("../data/general_output/all_results_" + mode + ".tsv", sep = "\t")
    sizes = list(set(df["tree_size"]))
    sizes.sort()
    plt.figure(figsize=(20, 10))
    for index in selected_indices:
        if np.isnan(df[index]).all():
            continue
        avg_values = [np.mean(df[df["tree_size"] == size][index]) for size in sizes]
        plt.scatter(sizes, avg_values, label = index, s = 10)
        plt.plot(sizes, avg_values)
    plt.legend(loc = "upper left")
    plt.xlabel("tree size n")
    plt.ylabel("index values")
    #plt.yscale("log")
    plt.savefig(os.path.join(plots_dir, mode + suffix + ".png"))
    plt.clf()


##plot_correlations(base_dirs, "database", "groups_90") # grouping method deprecated, ignores index types
##plot_correlations(base_dirs, "database", "repr_90")
##plot_correlations(base_dirs, "rerooting", "groups_95") # grouping method deprecated
##plot_correlations(base_dirs, "rerooting", "repr_95")



experiment_groups = [[
"total_I",
"total_I_w",
"total_I_prime",
    "mean_I",
"mean_I_w",
"mean_I_prime"],

["average_leaf_depth",
"average_vertex_depth",
 "total_path_length",
"total_internal_path_length",
"variance_of_leaves_depths",
"sackin_index",
  "s_shape"
 ],

["d_index",
    "colless_index",
  "corrected_colless_index",
    "total_cophenetic_index",
"quadratic_colless_index"],

["cherry_index",
"modified_cherry_index",
"IL_number",
"pitchforks",
"four_caterpillars",
"double_cherries"],

["rooted_quartet_index",
 "B_2_index",
 "B_1_index",
 "I_2_index",
 "maximum_depth",
 "stairs2",
 "j1"],

["stairs1",
    "rogers_j_index",
"symmetry_nodes_index",
"maximum_width",
 "max_width_over_max_depth"],

["maxdiff_widths",
"modified_maxdiff_widths",
    "diameter",
"average_ladder",
"ladder_length"],

["area_per_pair_index",
    "wiener_index",
 "total_farness",
"mean_bcent",
"maximum_closeness",
"minimum_farness",
"maximum_farness",
"minimum_bcent",
"maximum_bcent",
  "bcent_variance",
],

["root_imbalance",
"bcent_root",
"I_root"]
]

for k, sublist in enumerate(experiment_groups):
    print(k)
    #plot_variances(base_dirs, sublist, "_" + str(k))
    #plot_against_size(base_dirs, sublist, stat = "kurtosis", suffix = "_" + str(k)) 
    #plot_size_correlations(sublist, suffix = "_" + str(k))


    index_types_values = {"node_indices":[
              "corrected_colless_index",
              "I_2_index",
              "stairs2",
              "j1",
              "stairs1"],
    "node_indices4":[
              "rogers_j_index",
              "symmetry_nodes_index"],
    "node_indices2": ["quadratic_colless_index"],
    "node_indices3": ["colless_index"],
    "I_based_indices":["mean_I",
              "mean_I_prime",
              "mean_I_w"],
    "I_based_indices2":["total_I",
              "total_I_prime",
              "total_I_w"],
    "depth_indices": ["sackin_index",
              "total_path_length",
              "total_internal_path_length"],
    "depth_indices_2":[
              "s_shape",
              "variance_of_leaves_depths",
              "B_1_index"],
    "depth_indices_3":[
              "average_leaf_depth",
              "average_vertex_depth",
              "maximum_depth",
              "B_2_index" ],
    "width_indices" : ["maximum_width",
              "maxdiff_widths",
              "modified_maxdiff_widths",
              "max_width_over_max_depth"],
    "structure_indices" : [
              "d_index",
              "ladder_length",
              "average_ladder",
              ],
    "structure_indices2": ["rooted_quartet_index"],
    "subgraph_indices": ["cherry_index",
              "modified_cherry_index",
              "IL_number",
              "pitchforks",
              "four_caterpillars",
              "double_cherries"],
    "distance_indices" : ["total_cophenetic_index"],
    "distance_indices2":["diameter",
              "area_per_pair_index"],
    "network_indices": ["wiener_index",
              "total_farness"],
    "network_indices2": ["maximum_bcent"],
    "network_indices3":["mean_bcent",
              "bcent_root",
              "maximum_farness",
              "minimum_farness"],
    "network_indices4" : ["minimum_bcent"],
    "network_indices5" : ["maximum_closeness"],
    "network_indices6": ["bcent_variance"],
    "root_indices": ["root_imbalance",
              "I_root"],
    #"ranking_indices" : ["colijn_plazotta_rank",
    #          "furnas_rank"]
    }

    index_types_max = {"node_indices":["colless_index",
          "corrected_colless_index",
          "quadratic_colless_index"],
"node_indices2":["stairs1",
          "rogers_j_index",
          "symmetry_nodes_index"],
"depth_indices": ["sackin_index",
          "total_path_length",
          "total_internal_path_length",
          "average_leaf_depth",
          "average_vertex_depth",
          "maximum_depth",
          "B_2_index" ],
"subgraph_indices": ["cherry_index",
          "modified_cherry_index"],
"distance_indices" : ["total_cophenetic_index"],
"root_indices": ["root_imbalance",
          "I_root"],
}

index_types_yule = {"node_indices":["colless_index"],
                    "node_indices2": ["corrected_colless_index"],
"depth_indices": ["sackin_index"],
"depth_indices2" : ["average_leaf_depth",
          "variance_of_leaves_depths"],
"depth_indices3" : ["B_2_index"],
"structure_indices": ["rooted_quartet_index"],
"subgraph_indices": ["cherry_index"],
"mixed_indices" : ["total_cophenetic_index",
                      "quadratic_colless_index"],
"distance_indices": ["area_per_pair_index"],
}

#for i, (index_type, indices) in enumerate(index_types_max.items()):
#    plot_size_correlations(indices, "relative_max", suffix = "_" + index_type)

#for i, (index_type, indices) in enumerate(index_types_yule.items()):
#    plot_size_correlations(indices, "relative_yule", suffix = "_" + index_type)


#for i, (index_type, indices) in enumerate(index_types_values.items()):
#    plot_size_correlations(indices, "absolute", suffix = "_" + index_type)
#    plot_size_correlations(indices, "relative_tips", suffix = "_" + index_type)



