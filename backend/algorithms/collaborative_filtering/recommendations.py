import time

import numpy as np
from scipy.sparse import load_npz
from similarities import cosine_similarity


def cosine_item_based(m, weighted_average=True):
    utility_matrix = load_npz("matrices/utility_matrix.npz")

    utility_matrix_ones = utility_matrix.copy()
    utility_matrix_ones.data = np.ones_like(utility_matrix.data)

    hotel_similarities = cosine_similarity(utility_matrix, 0)

    if weighted_average:
        ratings_sum = utility_matrix * hotel_similarities
        weights_sum = utility_matrix_ones * hotel_similarities
    else:
        hotel_similarities_ones = hotel_similarities.copy()
        hotel_similarities_ones.data = np.ones_like(hotel_similarities.data)

        ratings_sum = utility_matrix * hotel_similarities_ones
        weights_sum = utility_matrix_ones * hotel_similarities_ones

    return ratings_sum / weights_sum


predicted_rating = cosine_item_based(1000, False)
