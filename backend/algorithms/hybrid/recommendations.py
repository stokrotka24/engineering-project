import numpy as np
from scipy.sparse import lil_matrix

from algorithms.collaborative_filtering.recommendations import predict_ratings
from algorithms.collaborative_filtering.similarities import cosine
from algorithms.content_based.matrices import get_hotel_matrix


def hybrid(utility_matrix, n, weighted_average):
    """
    Predict ratings for users from utility matrix based on hotel similarities
    from content based algorithm.

    Args:
        utility_matrix:
        n: how many the most similar hotels will be taken into consideration
           in ratings prediction
        weighted_average: True - prediction using weighted average, False -  prediction using arithmetic average

    Returns:
        Predicted users ratings for hotels
    """
    hotel_matrix = get_hotel_matrix()
    similarities = cosine(hotel_matrix, 1).toarray()

    no_rows = similarities.shape[0]
    top_similarities = lil_matrix(similarities.shape, dtype=np.float64)
    # in each row matrix only n the most similar hotels will be left
    for row_index in range(no_rows):
        row_data = similarities[row_index]
        # get indices of n similar objects (n+1 because we'll get also the same object - similarity(A,A) = 1.0)
        sorted_data_indices = row_data.argsort()[-(n + 1):]
        top_similarities.data[row_index] = row_data[sorted_data_indices].tolist()
        top_similarities.rows[row_index] = sorted_data_indices.tolist()

    top_similarities = top_similarities.tocsr()
    return predict_ratings(utility_matrix, utility_matrix, top_similarities, 0, weighted_average)