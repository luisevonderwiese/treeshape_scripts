import os
import math
import numpy as np

import itertools


def subset_score(subset, weights):
    return sum([weights[i][j] for i, j in itertools.combinations(subset, 2)])


def find_low_correlation_subset(correlations, n):
    names = list(correlations["index1"])
    correlations.drop("index1", axis = 1, inplace = True)
    matrix = correlations.to_numpy().tolist()
    size = len(matrix)

    weights = [[abs(matrix[i][j]) for j in range(size)] for i in range(size)]

    best_subset: tuple[int, ...] | None = None
    best_score = math.inf
    for subset in itertools.combinations(range(size), n):
        score = subset_score(subset, weights)
        if score < best_score:
            best_score = score
            best_subset = subset
        assert best_subset is not None
    return [names[i] for i in best_subset]
