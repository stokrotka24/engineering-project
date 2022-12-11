import os
import numpy as np
from scipy.sparse import csr_matrix, lil_matrix

from algorithms.collaborative_filtering.similarities import jaccard, cosine
from algorithms.collaborative_filtering.utility_matrix import get_utility_matrix, delete_matrices
from authorization.models import User


def predict_ratings(utility_matrix_for_similarity_type, utility_matrix, similarities, axis, weighted_average=True):
    """
    Predicts users ratings for hotels from utility matrix.

    Args:
        utility_matrix_for_similarity_type: if similarity function is cosine for normalized data - it is normalized utility matrix
                                            otherwise - it is utility matrix
        utility_matrix:
        similarities: matrix of similarities (axis=0 - between hotels, axis=1 - between users)
        axis: which dimension of utility matrix is considered: 0 - columns (hotel based), 1 - rows (item based)
        weighted_average: True - prediction using weighted average, False -  prediction using arithmetic average

    Returns:
        Matrix with predicted users ratings for hotels
    """

    # Original utility matrix must be used, because binary & normalized matrices doesn't store explicit zeroes
    utility_matrix_ones = utility_matrix.copy()
    utility_matrix_ones.data = np.ones_like(utility_matrix.data)

    if weighted_average:
        if axis == 0:
            similarities = similarities.T
            ratings_sum = utility_matrix_for_similarity_type * similarities
            weights_sum = utility_matrix_ones * similarities
        else:
            ratings_sum = similarities * utility_matrix_for_similarity_type
            weights_sum = similarities * utility_matrix_ones
    else:
        similarities_ones = similarities.copy()
        similarities_ones.data = np.ones_like(similarities.data)

        if axis == 0:
            similarities_ones = similarities_ones.T
            ratings_sum = utility_matrix_for_similarity_type * similarities_ones
            weights_sum = utility_matrix_ones * similarities_ones
        else:
            ratings_sum = similarities_ones * utility_matrix_for_similarity_type
            weights_sum = similarities_ones * utility_matrix_ones

    return ratings_sum / weights_sum


def filter_similarities(similarities, n):
    """
    Filters similarities matrix:
        in each row matrix only n the most similar users/hotels will be left

    Returns:
        Filtered matrix of similarities between users/hotels
    """
    similarities = similarities.tolil()
    no_rows = similarities.shape[0]

    for row_index in range(no_rows):
        row_data = np.array(similarities.data[row_index])
        column_indices = np.array(similarities.rows[row_index])
        # get indices of n similar objects (n+1 because we'll get also the same object - similarity(A,A) = 1.0)
        sorted_data_indices = row_data.argsort()[-(n + 1):]
        similarities.data[row_index] = row_data[sorted_data_indices].tolist()
        similarities.rows[row_index] = column_indices[sorted_data_indices].tolist()

    similarities = similarities.tocsr()
    return similarities


def jaccard_cf(axis, n, weighted_average, utility_matrix, binary_utility_matrix):
    """
    Collaborative filtering algorithm using jaccard similarity

    Returns:
        Predicted users ratings for hotels
    """
    similarities = jaccard(binary_utility_matrix, axis)
    similarities = filter_similarities(similarities, n)
    return predict_ratings(utility_matrix, utility_matrix, similarities, axis, weighted_average)


def cosine_cf(axis, n, weighted_average, utility_matrix, utility_matrix_to_calc_similarities):
    """
    Collaborative filtering algorithm using cosine similarity

    Returns:
        Predicted users ratings for hotels
    """
    similarities = cosine(utility_matrix_to_calc_similarities, axis)
    similarities = filter_similarities(similarities, n)
    return predict_ratings(utility_matrix, utility_matrix, similarities, axis, weighted_average)


def cosine_normalized_data_cf(axis, n, weighted_average, utility_matrix,
                              normalized_utility_matrix):
    """
    Collaborative filtering algorithm for normalized ratings using cosine similarity

    Returns:
        Predicted users ratings for hotels
    """

    similarities = cosine(normalized_utility_matrix, axis)

    positive_similarities = similarities > 0
    similarities.data = similarities.data[similarities.data > 0]
    similarities.indices = positive_similarities.indices
    similarities.indptr = positive_similarities.indptr

    similarities = filter_similarities(similarities, n)

    return predict_ratings(normalized_utility_matrix, utility_matrix, similarities, axis, weighted_average)


def update_recommendations():
    """
    Updates recommendations from collaborative filtering algorithm in database
    """
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    delete_matrices()

    utility_matrix = get_utility_matrix()
    predicted_ratings = cosine_cf(0, 1000, True, utility_matrix, utility_matrix)
    predicted_ratings = np.nan_to_num(predicted_ratings, nan=0, copy=False)
    predicted_ratings = lil_matrix(np.where((utility_matrix.toarray() == 0), predicted_ratings, 0))

    users = User.objects.all()
    for (user_index, user) in enumerate(users):
        user_row = np.array(predicted_ratings.data[user_index])
        hotel_indices = np.array(predicted_ratings.rows[user_index])
        sorted_data_indices = user_row.argsort()[::-1]
        recommendations = [{"hotel_id": hotel_index + 1} for hotel_index in hotel_indices[sorted_data_indices]]
        if len(recommendations) > 0:
            user.average_stars = float(str(user.average_stars))
            user.recommendations = recommendations
            user.save()


if __name__ == "__main__":
    update_recommendations()
