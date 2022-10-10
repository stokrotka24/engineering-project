import sys
import time

import numpy as np
from scipy.sparse import load_npz
from similarities import cosine_similarity


def cosine_item_based(utility_matrix, m, weighted_average=True):
    hotel_similarities = cosine_similarity(utility_matrix, 0).tolil()
    no_rows = hotel_similarities.shape[0]

    for row_index in range(no_rows):
        row_data = np.array(hotel_similarities.data[row_index])
        column_indices = np.array(hotel_similarities.rows[row_index])
        # get indices of m similar hotels (m+1 because we'll get also the same hotel - similarity(A,A) = 1.0)
        sorted_data_indices = row_data.argsort()[-(m + 1):]
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


if __name__ == "__main__":
    um = load_npz("matrices/utility_matrix.npz")
    print(um[372, 680])
    um[372, 680] = 0
    um.eliminate_zeros()
    # num_ratings = len(um.getrow(372).data)
    # print(num_ratings)
    predicted_rating = cosine_item_based(um, 150, False)
    print(predicted_rating[372, 680])
    # print(predicted_rating[372, :][~numpy.isnan(x)])

