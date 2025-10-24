set = "evonaps_dna"
outdir = paste("../data/", set, "/treestats/", sep = "")
if (!file.exists(outdir)){
	dir.create(file.path(outdir))
}

super_tree_dir = paste("../data/", set, "/trees/rooted/", sep = "")
tree_names <- list.dirs(path=super_tree_dir, full.names=FALSE, recursive=FALSE)
for (tree_name in tree_names) {
	print(tree_name)
	tree_dir = paste(super_tree_dir, tree_name, sep = "")
	big_results_df <- data.frame()
	big_times_df <- data.frame()
	root_names = list.files(path=tree_dir, pattern="*.tree", full.names=FALSE, recursive=FALSE)
	for (root_name in root_names) {
		sub <- strsplit(root_name, ".", fixed = TRUE)[[1]][1]
		parts <- strsplit(sub, "_")[[1]]
		root_type <- parts[1]
		root <- parts[2]
		tree <- ape::read.tree(paste(tree_dir, root_name, sep="/"))
		results_df <- data.frame(root = c(root), root_type = c(root_type))
		times_df <- data.frame(root = c(root), root_type = c(root_type))

                start.time <- Sys.time()
                res <- treestats::area_per_pair(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, area_per_pair_index = c(res))
                times_df <- cbind(times_df, area_per_pair_index = c(time))

                start.time <- Sys.time()
                res <- treestats::average_leaf_depth(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, average_leaf_depth = c(res))
                times_df <- cbind(times_df, average_leaf_depth = c(time))

                start.time <- Sys.time()
                res <- treestats::avg_vert_depth(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, average_vertex_depth = c(res))
                times_df <- cbind(times_df, average_vertex_depth = c(time))

                start.time <- Sys.time()
                res <- treestats::b1(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, B_1_index = c(res))
                times_df <- cbind(times_df, B_1_index = c(time))

                start.time <- Sys.time()
                res <- treestats::b2(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, B_2_index = c(res))
                times_df <- cbind(times_df, B_2_index = c(time))

                start.time <- Sys.time()
                res <- treestats::blum(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, s_shape = c(res))
                times_df <- cbind(times_df, s_shape = c(time))

                start.time <- Sys.time()
                res <- treestats::cherries(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, cherry_index = c(res))
                times_df <- cbind(times_df, cherry_index = c(time))

                start.time <- Sys.time()
                res <- treestats::colless(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, colless_index = c(res))
                times_df <- cbind(times_df, colless_index = c(time))

                start.time <- Sys.time()
                res <- treestats::colless_corr(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, corrected_colless_index = c(res))
                times_df <- cbind(times_df, corrected_colless_index = c(time))

                start.time <- Sys.time()
                res <- treestats::colless_quad(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, quadratic_colless_index = c(res))
                times_df <- cbind(times_df, quadratic_colless_index = c(time))

                start.time <- Sys.time()
                res <- treestats::diameter(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, diameter = c(res))
                times_df <- cbind(times_df, diameter = c(time))

                start.time <- Sys.time()
                res <- treestats::ew_colless(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, I_2_index = c(res))
                times_df <- cbind(times_df, I_2_index = c(time))

                start.time <- Sys.time()
                res <- treestats::mean_i(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, mean_I_prime = c(res))
                times_df <- cbind(times_df, mean_I_prime = c(time))

                start.time <- Sys.time()
                res <- treestats::max_del_width(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, modified_maxdiff_widths = c(res))
                times_df <- cbind(times_df, modified_maxdiff_widths = c(time))

                start.time <- Sys.time()
                res <- treestats::max_depth(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, maximum_depth = c(res))
                times_df <- cbind(times_df, maximum_depth = c(time))

                start.time <- Sys.time()
                res <- treestats::max_width(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, maximum_width = c(res))
                times_df <- cbind(times_df, maximum_width = c(time))

                start.time <- Sys.time()
                res <- treestats::mw_over_md(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, max_width_over_max_depth = c(res))
                times_df <- cbind(times_df, max_width_over_max_depth = c(time))

                start.time <- Sys.time()
                res <- treestats::rogers(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, rogers_j_index = c(res))
                times_df <- cbind(times_df, rogers_j_index = c(time))

                start.time <- Sys.time()
                res <- treestats::root_imbalance(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, root_imbalance = c(res))
                times_df <- cbind(times_df, root_imbalance = c(time))

                start.time <- Sys.time()
                res <- treestats::rquartet(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, rooted_quartet_index = c(res))
                times_df <- cbind(times_df, rooted_quartet_index = c(time))

                start.time <- Sys.time()
                res <- treestats::sackin(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, sackin_index = c(res))
                times_df <- cbind(times_df, sackin_index = c(time))

                start.time <- Sys.time()
                res <- treestats::stairs(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, stairs1 = c(res))
                times_df <- cbind(times_df, stairs1 = c(time))

                start.time <- Sys.time()
                res <- treestats::stairs2(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, stairs2 = c(res))
                times_df <- cbind(times_df, stairs2 = c(time))

                start.time <- Sys.time()
                res <- treestats::sym_nodes(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, symmetry_nodes_index = c(res))
                times_df <- cbind(times_df, symmetry_nodes_index = c(time))

                start.time <- Sys.time()
                res <- treestats::tot_coph(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, total_cophenetic_index = c(res))
                times_df <- cbind(times_df, total_cophenetic_index = c(time))

                start.time <- Sys.time()
                res <- treestats::tot_internal_path(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, total_internal_path_length = c(res))
                times_df <- cbind(times_df, total_internal_path_length = c(time))

                start.time <- Sys.time()
                res <- treestats::tot_path_length(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, total_path_length = c(res))
                times_df <- cbind(times_df, total_path_length = c(time))

                start.time <- Sys.time()
                res <- treestats::var_leaf_depth(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, variance_of_leaves_depths = c(res))
                times_df <- cbind(times_df, variance_of_leaves_depths = c(time))

                start.time <- Sys.time()
                res <- treestats::max_ladder(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, ladder_length = c(res))
                times_df <- cbind(times_df, ladder_length = c(time))

                start.time <- Sys.time()
                res <- treestats::ILnumber(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, IL_number = c(res))
                times_df <- cbind(times_df, IL_number = c(time))

                start.time <- Sys.time()
                res <- treestats::pitchforks(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, pitchforks = c(res))
                times_df <- cbind(times_df, pitchforks = c(time))

                start.time <- Sys.time()
                res <- treestats::four_prong(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, four_caterpillars = c(res))
                times_df <- cbind(times_df, four_caterpillars = c(time))

                start.time <- Sys.time()
                res <- treestats::double_cherries(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, double_cherries = c(res))
                times_df <- cbind(times_df, double_cherries = c(time))

                start.time <- Sys.time()
                res <- treestats::wiener(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, wiener_index = c(res))
                times_df <- cbind(times_df, wiener_index = c(time))

                start.time <- Sys.time()
                res <- treestats::max_betweenness(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, maximum_bcent = c(res))
                times_df <- cbind(times_df, maximum_bcent = c(time))

		big_results_df <- rbind(big_results_df, results_df)
		big_times_df <- rbind(big_times_df, times_df)

	}
        
	write.table(big_results_df, file=paste(outdir, tree_name, "_absolute.tsv", sep=""), quote=FALSE, sep='\t', col.names = NA)
	write.table(big_times_df, file=paste(outdir, tree_name, "_times.tsv", sep=""), quote=FALSE, sep='\t', col.names = NA)
}
