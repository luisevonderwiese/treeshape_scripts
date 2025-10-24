set = "evonaps_dna"
outdir = paste("../data/", set, "/treebalance/", sep = "")
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
                res <- treebalance::areaPerPairI(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]] 
                results_df <- cbind(results_df, area_per_pair_index = c(res))
                times_df <- cbind(times_df, area_per_pair_index = c(time))

                start.time <- Sys.time()
                res <- treebalance::avgLeafDepI(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, average_leaf_depth = c(res))
                times_df <- cbind(times_df, average_leaf_depth = c(time))

                start.time <- Sys.time()
                res <- treebalance::B1I(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, B_1_index = c(res))
                times_df <- cbind(times_df, B_1_index = c(time))

                start.time <- Sys.time()
                res <- treebalance::B2I(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, B_2_index = c(res))
                times_df <- cbind(times_df, B_2_index = c(time))

                start.time <- Sys.time()
                res <- treebalance::cherryI(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, cherry_index = c(res))
                times_df <- cbind(times_df, cherry_index = c(time))

                start.time <- Sys.time()
                res <- treebalance::collessI(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, colless_index = c(res))
                times_df <- cbind(times_df, colless_index = c(time))

                start.time <- Sys.time()
                res <- treebalance::collessI(tree, method = "corrected")
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, corrected_colless_index = c(res))
                times_df <- cbind(times_df, corrected_colless_index = c(time))

                start.time <- Sys.time()
                res <- treebalance::collessI(tree, method = "quadratic")
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, quadratic_colless_index = c(res))
                times_df <- cbind(times_df, quadratic_colless_index = c(time))

                # start.time <- Sys.time()
                # res <- treebalance::colPlaLab(tree)
                # end.time <- Sys.time()
                # time <- difftime(end.time, start.time, units = "secs")[[1]]
                # results_df <- cbind(results_df, colijn_plazotte_rank = c(res))
                # times_df <- cbind(times_df, colijn_plazotte_rank = c(time))

                start.time <- Sys.time()
                res <- treebalance::ewCollessI(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, I_2_index = c(res))
                times_df <- cbind(times_df, I_2_index = c(time))

                # start.time <- Sys.time()
                # res <- treebalance::furnasI(tree)
                # end.time <- Sys.time()
                # time <- difftime(end.time, start.time, units = "secs")[[1]]
                # results_df <- cbind(results_df, furnas_rank = c(res))
                # times_df <- cbind(times_df, furnas_rank = c(time))

                start.time <- Sys.time()
                res <- treebalance::IbasedI(tree, method = "mean")
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, mean_I = c(res))
                times_df <- cbind(times_df, mean_I = c(time))

                start.time <- Sys.time()
                res <- treebalance::IbasedI(tree, method = "total")
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, total_I = c(res))
                times_df <- cbind(times_df, total_I = c(time))

                start.time <- Sys.time()
                res <- treebalance::IbasedI(tree, method = "mean", correction = "prime")
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, mean_I_prime = c(res))
                times_df <- cbind(times_df, mean_I_prime = c(time))

                start.time <- Sys.time()
                res <- treebalance::IbasedI(tree, method = "total", correction = "prime")
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, total_I_prime = c(res))
                times_df <- cbind(times_df, total_I_prime = c(time))

                start.time <- Sys.time()
                res <- treebalance::IbasedI(tree, method = "mean", correction = "w")
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, mean_I_w = c(res))
                times_df <- cbind(times_df, mean_I_w = c(time))

                start.time <- Sys.time()
                res <- treebalance::IbasedI(tree, method = "total", correction = "w")
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, total_I_w = c(res))
                times_df <- cbind(times_df, total_I_w = c(time))

                start.time <- Sys.time()
                res <- treebalance::maxDelW(tree, method = "original")
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, maxdiff_widths = c(res))
                times_df <- cbind(times_df, maxdiff_widths = c(time))

                start.time <- Sys.time()
                res <- treebalance::maxDelW(tree, method = "modified")
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, modified_maxdiff_widths = c(res))
                times_df <- cbind(times_df, modified_maxdiff_widths = c(time))

                start.time <- Sys.time()
                res <- treebalance::maxDepth(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, maximum_depth = c(res))
                times_df <- cbind(times_df, maximum_depth = c(time))

                start.time <- Sys.time()
                res <- treebalance::maxWidth(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, maximum_width = c(res))
                times_df <- cbind(times_df, maximum_width = c(time))

                start.time <- Sys.time()
                res <- treebalance::mCherryI(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, modified_cherry_index = c(res))
                times_df <- cbind(times_df, modified_cherry_index = c(time))

                start.time <- Sys.time()
                res <- treebalance::mWovermD(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, max_width_over_max_depth = c(res))
                times_df <- cbind(times_df, max_width_over_max_depth = c(time))

                start.time <- Sys.time()
                res <- treebalance::rogersI(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, rogers_j_index = c(res))
                times_df <- cbind(times_df, rogers_j_index = c(time))

                start.time <- Sys.time()
                res <- treebalance::rQuartetI(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, rooted_quartet_index = c(res))
                times_df <- cbind(times_df, rooted_quartet_index = c(time))

                start.time <- Sys.time()
                res <- treebalance::sackinI(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, sackin_index = c(res))
                times_df <- cbind(times_df, sackin_index = c(time))

                start.time <- Sys.time()
                res <- treebalance::sShapeI(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, s_shape = c(res))
                times_df <- cbind(times_df, s_shape = c(time))

                start.time <- Sys.time()
                res <- treebalance::stairs1(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, stairs1 = c(res))
                times_df <- cbind(times_df, stairs1 = c(time))

                start.time <- Sys.time()
                res <- treebalance::stairs2(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, stairs2 = c(res))
                times_df <- cbind(times_df, stairs2 = c(time))

                start.time <- Sys.time()
                res <- treebalance::symNodesI(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, symmetry_nodes_index = c(res))
                times_df <- cbind(times_df, symmetry_nodes_index = c(time))

                start.time <- Sys.time()
                res <- treebalance::totCophI(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, total_cophenetic_index = c(res))
                times_df <- cbind(times_df, total_cophenetic_index = c(time))

                start.time <- Sys.time()
                res <- treebalance::totIntPathLen(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, total_internal_path_length = c(res))
                times_df <- cbind(times_df, total_internal_path_length = c(time))

                start.time <- Sys.time()
                res <- treebalance::totPathLen(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, total_path_length = c(res))
                times_df <- cbind(times_df, total_path_length = c(time))

                start.time <- Sys.time()
                res <- treebalance::varLeafDepI(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, variance_of_leaves_depths = c(res))
                times_df <- cbind(times_df, variance_of_leaves_depths = c(time))

                start.time <- Sys.time()
                res <- treebalance::weighL1dist(tree)
                end.time <- Sys.time()
                time <- difftime(end.time, start.time, units = "secs")[[1]]
                results_df <- cbind(results_df, d_index = c(res))
                times_df <- cbind(times_df, d_index = c(time))

		big_results_df <- rbind(big_results_df, results_df)
		big_times_df <- rbind(big_times_df, times_df)

	}
        
	write.table(big_results_df, file=paste(outdir, tree_name, "_absolute.tsv", sep=""), quote=FALSE, sep='\t', col.names = NA)
	write.table(big_times_df, file=paste(outdir, tree_name, "_times.tsv", sep=""), quote=FALSE, sep='\t', col.names = NA)
}
