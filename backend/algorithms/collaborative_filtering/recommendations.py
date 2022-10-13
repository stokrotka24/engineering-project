import numpy as np

from algorithms.collaborative_filtering.similarities import jaccard_similarity, cosine_similarity
from algorithms.collaborative_filtering.utility_matrix import get_utility_matrix, \
    get_binary_utility_matrix, get_normalized_utility_matrix


def predict_ratings(utility_matrix, similarities, axis, n, weighted_average=True):
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

    utility_matrix_ones = utility_matrix.copy()
    utility_matrix_ones.data = np.ones_like(utility_matrix.data)

    if weighted_average:
        if axis == 0:
            similarities = similarities.T
            ratings_sum = utility_matrix * similarities
            weights_sum = utility_matrix_ones * similarities
        else:
            ratings_sum = similarities * utility_matrix
            weights_sum = similarities * utility_matrix_ones
    else:
        similarities_ones = similarities.copy()
        similarities_ones.data = np.ones_like(similarities.data)

        if axis == 0:
            similarities_ones = similarities_ones.T
            ratings_sum = utility_matrix * similarities_ones
            weights_sum = utility_matrix_ones * similarities_ones
        else:
            ratings_sum = similarities_ones * utility_matrix
            weights_sum = similarities_ones * utility_matrix_ones

    return ratings_sum / weights_sum


def jaccard_collaborative_filtering(axis, n, weighted_average, threshold):
    binary_utility_matrix = get_binary_utility_matrix(threshold)
    #
    # binary_utility_matrix[372, 680] = 0
    # binary_utility_matrix.eliminate_zeros()

    similarities = jaccard_similarity(binary_utility_matrix, axis)
    utility_matrix = get_utility_matrix()
    #
    # utility_matrix[372, 680] = 0
    # utility_matrix.eliminate_zeros()

    return predict_ratings(utility_matrix, similarities, axis, n, weighted_average)


def cosine_collaborative_filtering(axis, n, weighted_average):
    utility_matrix = get_utility_matrix()
    #
    # utility_matrix[372, 680] = 0
    # utility_matrix.eliminate_zeros()

    similarities = cosine_similarity(utility_matrix, axis)
    return predict_ratings(utility_matrix, similarities, axis, n, weighted_average)


def centered_cosine_collaborative_filtering(axis, n, weighted_average):
    normalized_utility_matrix = get_normalized_utility_matrix()
    similarities = cosine_similarity(normalized_utility_matrix, axis)
    return predict_ratings(normalized_utility_matrix, similarities, axis, n, weighted_average)


if __name__ == "__main__":
    # um = load_npz("matrices/utility_matrix.npz")
    # um[372, 680] = 0
    # um.eliminate_zeros()
    # save_npz("matrices/utility_matrix.npz", um, True)
    # create_normalized_utility_matrix()

    n = 15000
    # r = jaccard_collaborative_filtering(1, n, True, 3)
    # print(r[372, 680])

    # r = cosine_collaborative_filtering(1, n, False)
    # print(r[372, 680])
    utility_matrix = get_utility_matrix()
    rating_sum = utility_matrix.sum(axis=1).A1
    rating_num = np.diff(utility_matrix.indptr)
    rating_num[rating_num == 0] = 1  # to avoid division by 0
    rating_mean = rating_sum / rating_num
    #
    r = centered_cosine_collaborative_filtering(1, n, False)
    print(r[372, 680])
    print(rating_mean[372])
    print(r[372, 680] + rating_mean[372])
