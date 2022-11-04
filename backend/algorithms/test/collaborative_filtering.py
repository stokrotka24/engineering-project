import math
from collections import defaultdict
from statistics import mean

import numpy as np
from scipy.sparse import load_npz, diags

from algorithms.collaborative_filtering.recommendations import cosine_collaborative_filtering, \
    jaccard_collaborative_filtering, centered_cosine_collaborative_filtering
from algorithms.collaborative_filtering.utility_matrix import get_rating_mean_per_user
from algorithms.test.algorithm_type import AlgorithmType
from algorithms.test.prepare_test_data import binarize_matrix
from algorithms.test.similarity_type import SimilarityType


def mean_absolute_error(predicted_ratings, predicted_ratings_indices, utility_matrix):
    diffs = defaultdict(list)
    for (user_id, hotel_id) in predicted_ratings_indices:
        diffs[user_id].append(abs(predicted_ratings[user_id, hotel_id] - utility_matrix[user_id, hotel_id]))

    return mean(list(map(lambda li: mean(li), diffs.values())))


def root_mean_square_error(predicted_ratings, predicted_ratings_indices, utility_matrix):
    diffs = defaultdict(list)
    for (user_id, hotel_id) in predicted_ratings_indices:
        diffs[user_id].append((predicted_ratings[user_id, hotel_id] - utility_matrix[user_id, hotel_id]) ** 2)

    return mean(list(map(lambda li: math.sqrt(mean(li)), diffs.values())))


def test(similarity_type: SimilarityType, algorithm_type: AlgorithmType, n: int, weighted_average: bool,
         test_ratio: float = 0.2, **kwargs):
    test_utility_matrix = load_npz(f"matrices/utility_matrix_{test_ratio}.npz")
    utility_matrix = load_npz(f"matrices/utility_matrix.npz")
    deleted_ratings_indices = (utility_matrix - test_utility_matrix).todok().keys()

    match similarity_type:
        case SimilarityType.cosine_binary:
            positive_threshold = kwargs["positive_threshold"]
            bin_test_utility_matrix = binarize_matrix(utility_matrix, positive_threshold)
            predicted_ratings = \
                cosine_collaborative_filtering(axis=algorithm_type.value, n=n,
                                               weighted_average=weighted_average,
                                               utility_matrix=test_utility_matrix,
                                               utility_matrix_to_calc_similarities=bin_test_utility_matrix)
        case SimilarityType.cosine:
            predicted_ratings \
                = cosine_collaborative_filtering(axis=algorithm_type.value, n=n,
                                                 weighted_average=weighted_average,
                                                 utility_matrix=test_utility_matrix,
                                                 utility_matrix_to_calc_similarities=test_utility_matrix)

        case SimilarityType.jaccard:
            positive_threshold = kwargs["positive_threshold"]
            bin_test_utility_matrix = binarize_matrix(utility_matrix, positive_threshold)
            predicted_ratings \
                = jaccard_collaborative_filtering(axis=algorithm_type.value, n=n,
                                                  weighted_average=weighted_average,
                                                  utility_matrix=test_utility_matrix,
                                                  binary_utility_matrix=bin_test_utility_matrix)
        case SimilarityType.centered_cosine:
            rating_mean = get_rating_mean_per_user(test_utility_matrix)
            rating_mean = diags(diagonals=rating_mean, offsets=0)
            ones = test_utility_matrix.copy()
            ones.data = np.ones_like(test_utility_matrix.data)
            norm_test_utility_matrix = test_utility_matrix - rating_mean * ones
            predicted_ratings \
                = centered_cosine_collaborative_filtering(axis=algorithm_type.value, n=n,
                                                          weighted_average=weighted_average,
                                                          utility_matrix=test_utility_matrix,
                                                          normalized_utility_matrix=norm_test_utility_matrix)
            ones = utility_matrix.copy()
            ones.data = np.ones_like(utility_matrix.data)
            utility_matrix = utility_matrix - rating_mean * ones

    predicted_ratings_indices = list(filter(
        lambda indices: not np.isnan(predicted_ratings[indices[0], indices[1]]),
        deleted_ratings_indices))

    time = 0
    prediction_percentage = len(predicted_ratings_indices) / len(deleted_ratings_indices)
    mae = mean_absolute_error(predicted_ratings, predicted_ratings_indices, utility_matrix)
    rmse = root_mean_square_error(predicted_ratings, predicted_ratings_indices, utility_matrix)
    return time, prediction_percentage, mae, rmse


# print(test(similarity_type=SimilarityType.cosine,
#            algorithm_type=AlgorithmType.item_based,
#            n=1000,
#            weighted_average=True))
# print(test(similarity_type=SimilarityType.cosine_binary,
#            algorithm_type=AlgorithmType.user_based,
#            n=10000,
#            weighted_average=True,
#            test_ratio=0.2,
#            positive_threshold=4))
# print(test(similarity_type=SimilarityType.jaccard,
#            algorithm_type=AlgorithmType.user_based,
#            n=10000,
#            weighted_average=True,
#            test_ratio=0.2,
#            positive_threshold=4))
print(test(similarity_type=SimilarityType.centered_cosine,
           algorithm_type=AlgorithmType.user_based,
           n=100000,
           weighted_average=False))
