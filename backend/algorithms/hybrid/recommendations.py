import sys

import numpy as np
from scipy.sparse import lil_matrix, csr_matrix

from algorithms.collaborative_filtering.recommendations import cosine_cf
from algorithms.collaborative_filtering.utility_matrix import get_binary_utility_matrix, get_utility_matrix
from algorithms.content_based.matrices import get_hotel_matrix, get_user_matrix
from algorithms.content_based.similarities import cosine
from algorithms.test.algorithm_type import AlgorithmType


def hybrid():
    utility_matrix = get_utility_matrix()
    predicted_ratings = cosine_cf(AlgorithmType.user_based.value,
                                  5000, False, utility_matrix, get_binary_utility_matrix(3))
    predicted_ratings = np.nan_to_num(predicted_ratings, nan=0, copy=False)
    predicted_ratings = csr_matrix(predicted_ratings)

    # hotel_matrix = get_hotel_matrix()
    # user_matrix = get_user_matrix()
    # similarities = cosine(user_matrix, hotel_matrix.T)
    # similarities = lil_matrix(np.where((utility_matrix.toarray() == 0), similarities.toarray(), 0))
    # no_users = similarities.shape[0]
    #
    # for user_index in range(no_users):
    #     print(user_index)
    #     row_data = np.array(similarities.data[user_index])
    #     column_indices = np.array(similarities.rows[user_index])
    #     sorted_data_indices = row_data.argsort()[::-1]
    #     similarities.data[user_index] = row_data[sorted_data_indices].tolist()
    #     similarities.rows[user_index] = column_indices[sorted_data_indices].tolist()
    #     # print(similarities.data[user_index])
    #     # print(similarities.rows[user_index])
    #
    #     predictions = predicted_ratings[user_index].A1
    #     print(predictions)
    #     predictions_indices = np.squeeze(np.argwhere(~np.isnan(predictions)))
    #     if predictions_indices.shape == ():  # case where we have prediction for one hotel
    #         predictions_indices = np.array([predictions_indices])
    #
    #     print(predictions_indices)
    #     print(lil_matrix(predictions_indices))
    #
    #     if user_index == 10:
    #         sys.exit()


def update_recommendations():
    hybrid()


hybrid()
