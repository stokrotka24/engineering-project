import os
import numpy as np

from algorithms.collaborative_filtering.similarities import jaccard_similarity, cosine_similarity
from algorithms.collaborative_filtering.utility_matrix import get_utility_matrix, \
    get_binary_utility_matrix, get_normalized_utility_matrix, delete_matrices
from authorization.models import User


def predict_ratings(utility_matrix_for_similarity_type, similarities, axis, n, weighted_average=True):
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

    utility_matrix = get_utility_matrix()
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


def jaccard_collaborative_filtering(axis, n, weighted_average, threshold=3):
    binary_utility_matrix = get_binary_utility_matrix(threshold)
    similarities = jaccard_similarity(binary_utility_matrix, axis)
    utility_matrix = get_utility_matrix()
    return predict_ratings(utility_matrix, similarities, axis, n, weighted_average)


# TODO add possibility to calc cosine similarities on binary matrix
def cosine_collaborative_filtering(axis, n, weighted_average):
    utility_matrix = get_utility_matrix()
    similarities = cosine_similarity(utility_matrix, axis)
    return predict_ratings(utility_matrix, similarities, axis, n, weighted_average)


def centered_cosine_collaborative_filtering(axis, n, weighted_average):
    normalized_utility_matrix = get_normalized_utility_matrix()
    similarities = cosine_similarity(normalized_utility_matrix, axis)
    return predict_ratings(normalized_utility_matrix, similarities, axis, n, weighted_average)


def update_recommendations():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    delete_matrices()

    predicted_ratings = cosine_collaborative_filtering(0, 1000, True)
    utility_matrix = get_utility_matrix()

    users = User.objects.all()
    # TODO update recommendations for every user
    for (user_index, user) in enumerate(users[:3]):
        ratings_indices = utility_matrix.getrow(user_index).indices
        predictions = predicted_ratings[user_index].A1
        predictions_indices = np.squeeze(np.argwhere(~np.isnan(predictions)))
        if predictions_indices.shape == ():  # case where we have prediction for one hotel
            predictions_indices = np.array([predictions_indices])

        predictions_indices = [hotel_index for hotel_index in predictions_indices if hotel_index not in ratings_indices]
        hotel_index_to_prediction = [(index, predictions[index]) for index in predictions_indices]
        hotel_index_to_prediction.sort(key=lambda t: t[1], reverse=True)
        recommendations = [{"hotel_id": hotel_index + 1} for (hotel_index, _) in hotel_index_to_prediction]

        if len(recommendations) > 0:
            user.average_stars = float(str(user.average_stars))
            user.recommendations = recommendations
            user.save()


if __name__ == "__main__":
    update_recommendations()
