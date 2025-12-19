library(plyr);
library(bipartite);
library(rnetcarto);
library(igraph);
#library(tidyverse);

network_paths <- list.files(path="../data/chamberlain/networks/networks", full.names=TRUE, recursive=FALSE)
full_res <- c()
for (network_path in network_paths) {
	name <- strsplit(tail(strsplit(network_path[[1]], "/")[[1]], n = 1), "_")[[1]][1]
	m <- as.matrix(read.csv(network_path)[, -1])
  rownames(m) <- NULL
	colnames(m) <- NULL

	graph <-  get.adjacency(graph_from_biadjacency_matrix(m), sparse = FALSE)
	row <- data.frame(dataset = name, modularity = netcarto(graph)[[2]])

	row$connectance <- networklevel(m, "connectance")
	row$nestedness <- nested(m, "NODF2")
	#print(con)
	#row <- c(row, con)
	full_res <- rbind(full_res, row)
	print(full_res)
}
write.csv(full_res, "../data/chamberlain/network_metrics.csv", row.names = FALSE)
