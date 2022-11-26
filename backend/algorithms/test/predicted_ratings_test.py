import math
import time
from collections import defaultdict
from statistics import mean
import numpy as np
from scipy.sparse import load_npz, diags

from algorithms.collaborative_filtering.recommendations import cosine_cf, \
    jaccard_cf, cosine_normalized_data_cf
from algorithms.collaborative_filtering.utility_matrix import get_rating_mean_per_user
from algorithms.hybrid.recommendations import hybrid
from algorithms.test.algorithm_type import AlgorithmType
from algorithms.test.ranking_quality_test import calc_ranking_quality_measures
from algorithms.test.prepare_test_data import binarize_matrix, NO_HOTELS, NO_USERS
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


def test_algorithm(similarity_type: SimilarityType, algorithm_type: AlgorithmType, n: int, weighted_average: bool,
                   file_prefix="", test_ratio: float = 0.2, ranking_quality_measures=False, **kwargs):
    test_utility_matrix = load_npz(f"matrices/{file_prefix}utility_matrix_{test_ratio}.npz")
    utility_matrix = load_npz(f"matrices/{file_prefix}utility_matrix.npz")
    deleted_ratings_indices = (utility_matrix - test_utility_matrix).todok().keys()

    match similarity_type:
        case SimilarityType.cosine_binary:
            positive_threshold = kwargs["positive_threshold"]
            bin_test_utility_matrix = binarize_matrix(test_utility_matrix, positive_threshold)
            start = time.time()
            predicted_ratings = \
                cosine_cf(axis=algorithm_type.value, n=n,
                          weighted_average=weighted_average,
                          utility_matrix=test_utility_matrix,
                          utility_matrix_to_calc_similarities=bin_test_utility_matrix)
            end = time.time()

        case SimilarityType.cosine:
            start = time.time()
            predicted_ratings \
                = cosine_cf(axis=algorithm_type.value, n=n,
                            weighted_average=weighted_average,
                            utility_matrix=test_utility_matrix,
                            utility_matrix_to_calc_similarities=test_utility_matrix)
            end = time.time()

        case SimilarityType.jaccard:
            positive_threshold = kwargs["positive_threshold"]
            bin_test_utility_matrix = binarize_matrix(test_utility_matrix, positive_threshold)
            start = time.time()
            predicted_ratings \
                = jaccard_cf(axis=algorithm_type.value, n=n,
                             weighted_average=weighted_average,
                             utility_matrix=test_utility_matrix,
                             binary_utility_matrix=bin_test_utility_matrix)
            end = time.time()

        case SimilarityType.cosine_normalized:
            start = time.time()
            rating_mean = get_rating_mean_per_user(test_utility_matrix)
            rating_mean = diags(diagonals=rating_mean, offsets=0)
            ones = test_utility_matrix.copy()
            ones.data = np.ones_like(test_utility_matrix.data)
            norm_test_utility_matrix = test_utility_matrix - rating_mean * ones
            predicted_ratings \
                = cosine_normalized_data_cf(axis=algorithm_type.value, n=n,
                                            weighted_average=weighted_average,
                                            utility_matrix=test_utility_matrix,
                                            normalized_utility_matrix=norm_test_utility_matrix)
            ones = utility_matrix.copy()
            ones.data = np.ones_like(utility_matrix.data)
            utility_matrix = utility_matrix - rating_mean * ones
            end = time.time()
        case _:
            start = time.time()
            predicted_ratings = \
                hybrid(utility_matrix=test_utility_matrix, n=n, weighted_average=weighted_average)
            end = time.time()

    predicted_ratings_indices = list(filter(
        lambda indices: not np.isnan(predicted_ratings[indices[0], indices[1]]),
        deleted_ratings_indices))

    elapsed_time = end - start
    prediction_ability = len(predicted_ratings_indices) / len(deleted_ratings_indices)
    mae = mean_absolute_error(predicted_ratings, predicted_ratings_indices, utility_matrix)
    rmse = root_mean_square_error(predicted_ratings, predicted_ratings_indices, utility_matrix)

    if ranking_quality_measures:
        calc_ranking_quality_measures(deleted_ratings=predicted_ratings_indices,
                                      recommendations=predicted_ratings,
                                      utility_matrix=utility_matrix)
    return elapsed_time, prediction_ability, mae, rmse


binary_similarities_types = [SimilarityType.jaccard, SimilarityType.cosine_binary]
similarities_types = [SimilarityType.cosine, SimilarityType.cosine_normalized]
algorithm_types = [alg_type for alg_type in AlgorithmType]
bool_values = [False, True]
positive_threshold_values = [i for i in range(1, 6)]
n_values = {AlgorithmType.item_based: [i for i in range(1, 6)] + [i for i in range(10, NO_HOTELS // 5, 10)],
            AlgorithmType.user_based: [i for i in range(1, 6)] + [i for i in range(10, 55, 10)] + [100] +
                                      [i for i in range(200, 2000, 200)] +
                                      [i for i in range(2000, 5000, 1000)] +
                                      [i for i in range(5000, NO_USERS // 10, 5000)]}


def test_jaccard_and_cosine_binary(file_prefix=""):
    for similarity_type in binary_similarities_types:
        for algorithm_type in algorithm_types:
            for weighted_average in bool_values:
                for positive_threshold in positive_threshold_values:
                    with open(
                            f"{file_prefix}results/{algorithm_type}/{similarity_type}_{weighted_average}_{positive_threshold}",
                            "a") as f:
                        for n in n_values[algorithm_type]:
                            print(similarity_type, algorithm_type, n, weighted_average, positive_threshold)
                            elapsed_time, pr, mae, rmse = test_algorithm(similarity_type=similarity_type,
                                                                         algorithm_type=algorithm_type,
                                                                         n=n, weighted_average=weighted_average,
                                                                         file_prefix=file_prefix,
                                                                         test_ratio=0.2,
                                                                         positive_threshold=positive_threshold)
                            f.write(f"{n} {elapsed_time} {pr} {mae} {rmse}\n")


def test_cosine_and_centered_cosine(file_prefix=""):
    for similarity_type in similarities_types:
        for algorithm_type in algorithm_types:
            for weighted_average in bool_values:
                with open(f"{file_prefix}results/{algorithm_type}/{similarity_type}_{weighted_average}",
                          "a") as f:
                    for n in n_values[algorithm_type]:
                        print(similarity_type, algorithm_type, n, weighted_average)
                        elapsed_time, pr, mae, rmse = test_algorithm(similarity_type=similarity_type,
                                                                     algorithm_type=algorithm_type,
                                                                     n=n, weighted_average=weighted_average,
                                                                     file_prefix=file_prefix)

                        f.write(f"{n} {elapsed_time} {pr} {mae} {rmse}\n")


def test_hybrid(file_prefix=""):
    for weighted_average in bool_values:
        with open(f"{file_prefix}results/hybrid/{weighted_average}",
                  "a") as f:
            for n in n_values[AlgorithmType.item_based]:
                print("hybrid", n, weighted_average)
                elapsed_time, pr, mae, rmse = test_algorithm(similarity_type=None, algorithm_type=None,
                                                             n=n, weighted_average=weighted_average,
                                                             file_prefix=file_prefix)

                f.write(f"{n} {elapsed_time} {pr} {mae} {rmse}\n")


if __name__ == "__main__":
    test_jaccard_and_cosine_binary()
    test_cosine_and_centered_cosine()
    test_hybrid()
    test_jaccard_and_cosine_binary("filtered_")
    test_cosine_and_centered_cosine("filtered_")
    test_hybrid("filtered_")