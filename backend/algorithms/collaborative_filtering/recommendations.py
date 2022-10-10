import time

import numpy as np
from scipy.sparse import load_npz
from similarities import cosine_similarity


def cosine(utility_matrix, axis, n, weighted_average=True):
    similarities = cosine_similarity(utility_matrix, axis).tolil()
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


def cosine_item_based(utility_matrix, n, weighted_average=True):
    hotel_similarities = cosine_similarity(utility_matrix, 0).tolil()
    no_rows = hotel_similarities.shape[0]

    for row_index in range(no_rows):
        row_data = np.array(hotel_similarities.data[row_index])
        column_indices = np.array(hotel_similarities.rows[row_index])
        # get indices of n similar hotels (n+1 because we'll get also the same hotel - similarity(A,A) = 1.0)
        sorted_data_indices = row_data.argsort()[-(n + 1):]
        hotel_similarities.data[row_index] = row_data[sorted_data_indices].tolist()
        hotel_similarities.rows[row_index] = column_indices[sorted_data_indices].tolist()

    hotel_similarities = hotel_similarities.tocsr()
    hotel_similarities = hotel_similarities.T

    utility_matrix_ones = utility_matrix.copy()
    utility_matrix_ones.data = np.ones_like(utility_matrix.data)

    if weighted_average:
        ratings_sum = utility_matrix * hotel_similarities
        weights_sum = utility_matrix_ones * hotel_similarities
    else:
        hotel_similarities_ones = hotel_similarities.copy()
        hotel_similarities_ones.data = np.ones_like(hotel_similarities.data)

        ratings_sum = utility_matrix * hotel_similarities_ones
        weights_sum = utility_matrix_ones * hotel_similarities_ones

    return ratings_sum / weights_sum


def cosine_user_based(utility_matrix, n, weighted_average=True):
    print(time.time())
    user_similarities = cosine_similarity(utility_matrix, 1).tolil()
    no_rows = user_similarities.shape[0]

    print(time.time())
    for row_index in range(no_rows):
        row_data = np.array(user_similarities.data[row_index])
        column_indices = np.array(user_similarities.rows[row_index])
        # get indices of n similar users (n+1 because we'll get also the same user - similarity(A,A) = 1.0)
        sorted_data_indices = row_data.argsort()[-(n + 1):]
        user_similarities.data[row_index] = row_data[sorted_data_indices].tolist()
        user_similarities.rows[row_index] = column_indices[sorted_data_indices].tolist()

    user_similarities = user_similarities.tocsr()
    print(time.time())

    utility_matrix_ones = utility_matrix.copy()
    utility_matrix_ones.data = np.ones_like(utility_matrix.data)

    if weighted_average:
        ratings_sum = user_similarities * utility_matrix
        weights_sum = user_similarities * utility_matrix_ones
    else:
        user_similarities_ones = user_similarities.copy()
        user_similarities_ones.data = np.ones_like(user_similarities.data)

        ratings_sum = user_similarities_ones * utility_matrix
        weights_sum = user_similarities_ones * utility_matrix_ones

    print(time.time())
    return ratings_sum / weights_sum


if __name__ == "__main__":
    um = load_npz("matrices/utility_matrix.npz")
    print(um[372, 680])
    um[372, 680] = 0
    um.eliminate_zeros()
    # num_ratings = len(um.getrow(372).data)
    # print(num_ratings)
    # predicted_rating = cosine_item_based(um, 2997, False)
    # print(predicted_rating[372, 680])
    # x = predicted_rating[372, :]
    # x = x[~np.isnan(x)]
    # x = csr_matrix(x)
    #
    # print(type(predicted_rating))
    # print(type(x))
    # print(x)
    # print(len(x.data) - num_ratings)
    # # print([~numpy .isnan(x)])
    predicted_rating = cosine(um, 1, 5500, True)
    print(predicted_rating[372, 680])
