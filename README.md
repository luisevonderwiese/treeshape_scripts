# Scripts for large-scale evaluation of tree shape indices

## Requirements:
- Set up the Conda Environment
```
conda env create -f environment.yml
conda acitvate treeshape-scripts
```
- Data: <br>
Load all trees from [EvoNAPS](). Place trees inferred for DNA data in `data/evonaps_dna/trees/unrooted`. Place trees inferred for AA data in `data/evonaps_aa/trees/unrooted`. <br>
Load all trees from [RAxMLGrove](https://github.com/angtft/RAxMLGrove). Place them in `data/grove/trees/unrooted`.


## Execution:

### Main Experiment
```
cd scripts/
python root_all_possible.py # create all possible rooted trees for each unrooted tree
python evaluate_parallel.py # evaluate tree shape indices using treeshapy
python stats.py # compute summary statistics
python plots.py # create plots
python benchmark_plots.py # create benchmark plots
python pca.py # run pca
python subsets.py # determine subsets with minimum pairwise correlation
```
 ### Case Study
```
cd case_study/
python yule.py # sample trees
python experiment.py # run experiments

```
### Verification
```
cd scripts/
Rscript treestats_reference.r # evaluate tree shape indices with treestats
correctness_comparison.py # compare treeshapy and treestats results
python sample_multi.py # sample multifurcating trees
python evaluate_multi.py # evaluate tree shape indices on multifurcating trees using treeshapy
Rscript treestats_reference_multi.r # evaluate tree shape indices on multifurcating trees using treestats
python correctness_multi.py # compare treeshapy and treestats results for multifurcating trees
```
