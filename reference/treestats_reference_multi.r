outdir = "../test/test_multi/treestats/"
if (!file.exists(outdir)){
	dir.create(file.path(outdir))
}

super_tree_dir = "../test/test_multi/trees/rooted/"
tree_paths <- list.files(path=super_tree_dir, full.names=FALSE, recursive=FALSE)
for (tree_path in tree_paths) {
	tree_name = tools::file_path_sans_ext(tree_path)
	print(tree_name)
	results_file_name <- paste(outdir, tree_name, "_absolute.tsv", sep="")
	results_df <- data.frame(index = c("value"))
	tree <- ape::read.tree(paste(super_tree_dir, tree_path, sep=""))

        res <- treestats::wiener(tree)
        results_df <- cbind(results_df, wiener_index = c(res))

	res <- treestats::area_per_pair(tree)
        results_df <- cbind(results_df, area_per_pair_index = c(res))
       
	res <- treestats::avg_vert_depth(tree)
        results_df <- cbind(results_df, average_vertex_depth = c(res))
        
	res <- treestats::b1(tree)
        results_df <- cbind(results_df, B_1_index = c(res))

        res <- treestats::b2(tree)
        results_df <- cbind(results_df, B_2_index = c(res))

        res <- treestats::max_del_width(tree)
        results_df <- cbind(results_df, modified_maxdiff_widths = c(res))

        res <- treestats::max_depth(tree)
        results_df <- cbind(results_df, maximum_depth = c(res))

	res <- treestats::max_width(tree)
        results_df <- cbind(results_df, maximum_width = c(res))

        res <- treestats::mw_over_md(tree)
        results_df <- cbind(results_df, max_width_over_max_depth = c(res))

        res <- treestats::rquartet(tree)
        results_df <- cbind(results_df, rooted_quartet_index = c(res))

        res <- treestats::tot_internal_path(tree)
        results_df <- cbind(results_df, total_internal_path_length = c(res))

	res <- treestats::var_leaf_depth(tree)
        results_df <- cbind(results_df, variance_of_leaves_depths = c(res))

        res <- treestats::ILnumber(tree)
        results_df <- cbind(results_df, IL_number = c(res))

	res <- treestats::max_betweenness(tree)
        results_df <- cbind(results_df, maximum_bcent = c(res))

	res <- treestats::max_closeness(tree)
        results_df <- cbind(results_df, maximum_closeness = c(res))

        res <- treestats::root_imbalance(tree)
        results_df <- cbind(results_df, root_imbalance = c(res))

	res <- treestats::double_cherries(tree)
        results_df <- cbind(results_df, double_cherries = c(res))

	res <- treestats::four_prong(tree)
        results_df <- cbind(results_df, four_caterpillars = c(res))#

	res <- treestats::diameter(tree)
        results_df <- cbind(results_df, diameter = c(res))

	#res <- treestats::max_ladder(tree)
        #results_df <- cbind(results_df, ladder_length = c(res))

	#res <- treestats::rogers(tree)
        #results_df <- cbind(results_df, rogers_j_index = c(res))

	#res <- treestats::avg_ladder(tree)
        #results_df <- cbind(results_df, average_ladder = c(res))


	write.table(results_df, file=results_file_name, quote=FALSE, sep='\t', col.names = NA)
}
