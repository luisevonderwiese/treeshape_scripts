tree_dir = "../data/evonaps_dna/trees/rooted"
tree_names <- list.files(path=tree_dir, pattern="*.tree", full.names=FALSE, recursive=FALSE)

for (tree_name in tree_names) {
	print(tree_name)
	tree <- ape::read.tree(paste(tree_dir, tree_name, sep=""))
	results <- c()
	names <- c()
	times <- c()
	
	start.time <- Sys.time()
	results <- c(results, treebalance::areaPerPairI(tree))
	end.time <- Sys.time()
	times <- c(times, end.time - start.time)
	names <- c(names, "area_per_pair_index")

	start.time <- Sys.time()
	results <- c(results, treebalance::avgLeafDepI(tree))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "average_leaf_depth")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::avgVertDep(tree))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "average_vertex_depth")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::B1I(tree))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "B_1_index")
	
	start.time <- Sys.time()
	results <-c(results, treebalance::B2I(tree))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "B_2_index")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::cherryI(tree))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "cherry_index")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::collessI(tree, method="original"))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "colless_index")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::collessI(tree, method="corrected"))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "corrected_colless_index")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::collessI(tree, method="quadratic"))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "quadratic_colless_index")
	
	#start.time <- Sys.time()
	#results <- c(results, treebalance::colPlaLab(tree))
	#end.time <- Sys.time()
        #times <- c(times, end.time - start.time)
	#names <- c(names, "colijn_plazotte_rank")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::ewCollessI(tree))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "I_2_index")
	
	#start.time <- Sys.time()
	#results <- c(results, treebalance::furnasI(tree))
	#end.time <- Sys.time()
        #times <- c(times, end.time - start.time)
	#names <- c(names, "furnas_rank")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::IbasedI(tree, method="mean"))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "mean_I")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::IbasedI(tree, method="total"))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "total_I")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::IbasedI(tree, method="mean", correction="prime"))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "mean_I_prime")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::IbasedI(tree, method="total", correction="prime"))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "total_I_prime")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::IbasedI(tree, method="mean", correction="w"))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "mean_I_w")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::IbasedI(tree, method="total", correction="w"))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "total_I_w")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::maxDelW(tree, method="original"))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "maxdiff_widths")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::maxDelW(tree, method="modified"))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "modified_maxdiff_widths")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::maxDepth(tree))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "maximum_depth")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::maxWidth(tree))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "maximum_width")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::mCherryI(tree))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "modified_cherry_index")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::mWovermD(tree))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "max_width_over_max_depth")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::rogersI(tree))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "rogers_j_index")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::rQuartetI(tree))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "rooted_quartet_index")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::sackinI(tree))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "sackin_index")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::sShapeI(tree))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "s_shape")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::stairs1(tree))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "stairs1")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::stairs2(tree))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "stairs2")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::symNodesI(tree))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "symmetry_nodes_index")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::totCophI(tree))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "total_cophenetic_index")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::totIntPathLen(tree))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "total_internal_path_length")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::totPathLen(tree))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "total_path_length")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::varLeafDepI(tree))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "variance_of_leaves_depths")
	
	start.time <- Sys.time()
	results <- c(results, treebalance::weighL1dist(tree))
	end.time <- Sys.time()
        times <- c(times, end.time - start.time)
	names <- c(names, "d_index")
	
        if (!file.exists("../results/")){
                dir.create(file.path("../results/"))
        }
        if (!file.exists("../results/treebalance/")){
                dir.create(file.path("../results/treebalance/"))
        }
        if (!file.exists("../results/treebalance/metrics/")){
                dir.create(file.path("../results/treebalance/metrics/"))
        }
        if (!file.exists("../results/treebalance/benchmark/")){
                dir.create(file.path("../results/treebalance/benchmark/"))
        }
        if (!file.exists("../results/treebalance/metrics/evonaps_dna/")){
                dir.create(file.path("../results/treebalance/metrics/evonaps_dna/"))
        }
        if (!file.exists("../results/treebalance/benchmark/evonaps_dna/")){
                dir.create(file.path("../results/treebalance/benchmark/evonaps_dna/"))
        }

        data <- data.frame(names,results)
        write.csv(data, paste("../results/treebalance/metrics/evonaps_dna/", tree_name, ".csv", sep=""))
        data <- data.frame(names,times)
        write.csv(data, paste("../results/treebalance/benchmark/evonaps_dna/", tree_name, ".csv", sep=""))


}
