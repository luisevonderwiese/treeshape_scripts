tree_dir = "../data/evonaps_dna/trees/rooted/"
tree_names <- list.files(path=tree_dir, pattern="*.tree", full.names=FALSE, recursive=FALSE)
for (tree_name in tree_names) {
	print(tree_name)
	tree <- ape::read.tree(paste(tree_dir, tree_name, sep=""))
	results <- c()
	names <- c()
	times <- c()

	start.time <- Sys.time()
	results <- c(results, treestats::area_per_pair(tree))
	names <- c(names, "area_per_pair_index")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
	results <- c(results, treestats::average_leaf_depth(tree))
	names <- c(names, "average_leaf_depth")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
	results <- c(results, treestats::avg_vert_depth(tree))
	names <- c(names, "average_vertex_depth")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
	results <- c(results, treestats::b1(tree))
	names <- c(names, "B_1_index")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
	results <- c(results, treestats::b2(tree))
	names <- c(names, "B_2_index")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
	results <- c(results, treestats::blum(tree))
	names <- c(names, "s_shape")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
	results <- c(results, treestats::cherries(tree))
	names <- c(names, "cherry_index")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
	results <- c(results, treestats::colless(tree))
	names <- c(names, "colless_index")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
	results <- c(results, treestats::colless_corr(tree))
	names <- c(names, "corrected_colless_index")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
	results <- c(results, treestats::colless_quad(tree))
	names <- c(names, "quadratic_colless_index")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
	results <- c(results, treestats::diameter(tree))
	names <- c(names, "diameter")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
	results <- c(results, treestats::ew_colless(tree))
	names <- c(names, "I_2_index")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
	results <- c(results, treestats::mean_i(tree))
	names <- c(names, "mean_I_prime")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
	results <- c(results, treestats::max_del_width(tree))
	names <- c(names, "modified_maxdiff_widths")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
	results <- c(results, treestats::max_depth(tree))
	names <- c(names, "maximum_depth")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	
	start.time <- Sys.time()
	results <- c(results, treestats::max_width(tree))
	names <- c(names, "maximum_width")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
	results <- c(results, treestats::mw_over_md(tree))
	names <- c(names, "max_width_over_max_depth")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
	results <- c(results, treestats::rogers(tree))
	names <- c(names, "rogers_j_index")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
	results <- c(results, treestats::root_imbalance(tree))
	names <- c(names, "root_imbalance")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
	results <- c(results, treestats::rquartet(tree))
	names <- c(names, "rooted_quartet_index")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
	results <- c(results, treestats::sackin(tree))
	names <- c(names, "sackin_index")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
	results <- c(results, treestats::stairs(tree))
	names <- c(names, "stairs1")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
	results <- c(results, treestats::stairs2(tree))
	names <- c(names, "stairs2")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	
	start.time <- Sys.time()
	results <- c(results, treestats::sym_nodes(tree))
	names <- c(names, "symmetry_nodes_index")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
	results <- c(results, treestats::tot_coph(tree))
	names <- c(names, "total_cophenetic_index")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
	results <- c(results, treestats::tot_internal_path(tree))
	names <- c(names, "total_internal_path_length")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
	results <- c(results, treestats::tot_path_length(tree))
	names <- c(names, "total_path_length")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
	results <- c(results, treestats::treeness(tree))
	names <- c(names, "treeness")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
	results <- c(results, treestats::var_leaf_depth(tree))
	names <- c(names, "variance_of_leaves_depths")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
        results <- c(results, treestats::max_ladder(tree))
        names <- c(names, "ladder_length")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
        results <- c(results, treestats::ILnumber(tree))
        names <- c(names, "IL_number")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
        results <- c(results, treestats::pitchforks(tree))
        names <- c(names, "pitchforks")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
        results <- c(results, treestats::four_caterpillars(tree))
        names <- c(names, "four_prong")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	start.time <- Sys.time()
        results <- c(results, treestats::double_cherries(tree))
        names <- c(names, "double_cherries")
        end.time <- Sys.time()
        times <- c(times, end.time - start.time)

	if (!file.exists("../results/")){
        	dir.create(file.path("../results/"))
	}
	if (!file.exists("../results/treestats/")){
                dir.create(file.path("../results/treestats/"))
        }
	if (!file.exists("../results/treestats/metrics/")){
                dir.create(file.path("../results/treestats/metrics/"))
        }
	if (!file.exists("../results/treestats/benchmark/")){
                dir.create(file.path("../results/treestats/benchmark/"))
        }
        if (!file.exists("../results/treestats/metrics/evonaps_dna/")){
                dir.create(file.path("../results/treestats/metrics/evonaps_dna/"))
        }
        if (!file.exists("../results/treestats/benchmark/evonaps_dna/")){
                dir.create(file.path("../results/treestats/benchmark/evonaps_dna/"))
        }

	data <- data.frame(names,results)
	write.csv(data,	paste("../results/treestats/metrics/evonaps_dna/", tree_name, ".csv", sep=""))
	data <- data.frame(names,times)
        write.csv(data, paste("../results/treestats/benchmark/evonaps_dna/", tree_name, ".csv", sep=""))

}
