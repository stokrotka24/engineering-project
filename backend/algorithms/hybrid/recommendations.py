import numpy as np
from scipy.sparse import lil_matrix

from algorithms.collaborative_filtering.recommendations import predict_ratings
from algorithms.collaborative_filtering.similarities import cosine
from algorithms.content_based.matrices import get_hotel_matrix


def hybrid(utility_matrix, n, weighted_average):
    hotel_matrix = get_hotel_matrix()
    similarities = cosine(hotel_matrix, 1).toarray()

    no_rows = similarities.shape[0]
    top_similarities = lil_matrix(similarities.shape, dtype=np.float64)
    for row_index in range(no_rows):
        row_data = similarities[row_index]
        sorted_data_indices = row_data.argsort()[-(n + 1):]
        top_similarities.data[row_index] = row_data[sorted_data_indices].tolist()
        top_similarities.rows[row_index] = sorted_data_indices.tolist()

    top_similarities = top_similarities.tocsr()
    return predict_ratings(utility_matrix, utility_matrix, top_similarities, 0, weighted_average)