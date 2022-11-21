import time
import numpy as np
from scipy.sparse import load_npz

from algorithms.hybrid.recommendations import hybrid
from algorithms.test.collaborative_filtering import mean_absolute_error, root_mean_square_error


def test_algorithm(n: int, weighted_average: bool,
                   file_prefix="", test_ratio: float = 0.2):
    test_utility_matrix = load_npz(f"matrices/{file_prefix}utility_matrix_{test_ratio}.npz")
    utility_matrix = load_npz(f"matrices/{file_prefix}utility_matrix.npz")
    deleted_ratings_indices = (utility_matrix - test_utility_matrix).todok().keys()

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
    return elapsed_time, prediction_ability, mae, rmse


if __name__ == "__main__":
    print(test_algorithm(n=590, weighted_average=False))
