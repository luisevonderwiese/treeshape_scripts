# Scripts for large-scale evaluation of tree shape indices

## Requirements:
- Set up the Conda Environment
```
conda env create -f environment.yml
```
- Data
```

```

## Execution:

### Main Experiment
```
cd scripts/
python root_all_possible.py
python evaluate_parallel.py
python stats.py
python plots.py
python benchmark_plots.py
python pca.py
python subsets.py
```
 ### Case Study
```
cd case_study/
python yule.py
python experiment.py

```
### Verification
```
cd scripts/
Rscript treestats_reference.r 
correctness_comparison.py
python sample_multi.py
python evaluate_multi.py
Rscript treestats_reference_multi.r 
python correctness_multi.py
```
