import random

from algorithms.collaborative_filtering.recommendations import cosine_collaborative_filtering
from algorithms.collaborative_filtering.utility_matrix import get_utility_matrix


def test(test_ratio=0.25):
    deleted_reviews = {}

    utility_matrix = get_utility_matrix()
    print(len(utility_matrix.data) / (utility_matrix.shape[0] * utility_matrix.shape[1]))
    no_users = utility_matrix.shape[0]
    updated_utility_matrix = utility_matrix.copy()

    for user_id in range(no_users):
        if user_id % 1000 == 0:
            print(user_id)
        hotel_indices = utility_matrix.getrow(user_id).indices
        no_indices_to_delete = round(test_ratio * len(hotel_indices))
        indices_to_delete = random.choices(list(hotel_indices), k=no_indices_to_delete)
        deleted_reviews[user_id] = indices_to_delete
        for hotel_index in indices_to_delete:
            updated_utility_matrix[user_id, hotel_index] = 0

    updated_utility_matrix.eliminate_zeros()
    print(len(updated_utility_matrix.data) / (updated_utility_matrix.shape[0] * updated_utility_matrix.shape[1]))

    predicted_ratings = cosine_collaborative_filtering(axis=0, n=1000, weighted_average=True,
                                                       utility_matrix=updated_utility_matrix,
                                                       utility_matrix_to_calc_similarities=updated_utility_matrix)


    diffs = []
    for user_id in range(no_users):
        for hotel_index in deleted_reviews[user_id]:
            if predicted_ratings[user_id, hotel_index] > 0:
                diff = abs(predicted_ratings[user_id, hotel_index] - float(utility_matrix[user_id, hotel_index]))
                diffs.append(diff)
                print(utility_matrix[user_id, hotel_index])
                print(predicted_ratings[user_id, hotel_index])
                print(diff)
                print()
    print(sum(diffs)/len(diffs))

test()
