import random
import shelve

import numpy as np
from scipy.sparse import save_npz, diags, dok_matrix, load_npz, csr_matrix

from algorithms.collaborative_filtering.utility_matrix import create_utility_matrix, delete_matrices, \
    get_rating_mean_per_user
from algorithms.content_based.matrices import get_hotel_matrix

FIRST_TEST_USER_ID = 3
NO_USERS = 152760

FIRST_TEST_HOTEL_ID = 1
NO_HOTELS = 2977


def create_test_utility_matrix():
    create_utility_matrix(user_bias=FIRST_TEST_USER_ID, hotel_bias=FIRST_TEST_HOTEL_ID,
                          no_users=NO_USERS, no_hotels=NO_HOTELS)


def delete_ratings_in_utility_matrix(utility_matrix, delete_ratio=0.25, file_infix=""):
    print("Delete ratio:", delete_ratio)
    utility_matrix = utility_matrix.todok()
    ratings_indices = list(utility_matrix.keys())
    no_ratings_to_delete = round(delete_ratio * len(ratings_indices))
    print("Real delete ratio:", no_ratings_to_delete / len(ratings_indices))
    ratings_indices_to_delete = random.sample(ratings_indices, no_ratings_to_delete)
    with shelve.open(f"matrices/{file_infix}deleted_ratings_{delete_ratio}.bin") as f:
        f['deleted_ratings'] = ratings_indices_to_delete

    updated_utility_matrix = utility_matrix.copy()
    for indices in ratings_indices_to_delete:
        updated_utility_matrix.pop(indices)

    updated_utility_matrix = updated_utility_matrix.tocsr()
    save_npz(f"matrices/{file_infix}utility_matrix_{delete_ratio}.npz", updated_utility_matrix, True)


def prepare_user_matrix(delete_ratio=0.25):
    hotel_matrix = get_hotel_matrix()

    utility_matrix = load_npz(f"matrices/utility_matrix_{delete_ratio}.npz")
    normalized_utility_matrix = normalize_matrix(utility_matrix)

    utility_matrix_ones = utility_matrix.copy()
    utility_matrix_ones.data = np.ones_like(utility_matrix.data)

    ratings_sum = normalized_utility_matrix * hotel_matrix
    ratings_num = utility_matrix_ones * hotel_matrix
    user_matrix = ratings_sum / ratings_num

    user_matrix[np.isnan(user_matrix)] = 0
    user_matrix = csr_matrix(user_matrix)

    save_npz(f"matrices/user_matrix_{delete_ratio}.npz", user_matrix, True)
    return user_matrix


def binarize_matrix(utility_matrix, positive_threshold):
    binary_utility_matrix = utility_matrix.copy()
    data = list(binary_utility_matrix.data)
    binary_utility_matrix.data = np.array([1 if elem >= positive_threshold else 0 for elem in data])
    binary_utility_matrix.eliminate_zeros()
    return binary_utility_matrix


def normalize_matrix(utility_matrix):
    rating_mean = get_rating_mean_per_user(utility_matrix)
    rating_mean = diags(diagonals=rating_mean, offsets=0)
    ones = utility_matrix.copy()
    ones.data = np.ones_like(utility_matrix.data)
    normalized_utility_matrix = utility_matrix - rating_mean * ones
    return normalized_utility_matrix


def filter_utility_matrix_by_active_users(utility_matrix, min_reviews_number=5):
    no_reviews = np.diff(utility_matrix.indptr)
    is_active_user = no_reviews >= min_reviews_number

    no_selected_users = is_active_user.sum()
    no_all_users, no_hotels = utility_matrix.shape
    filtered_utility_matrix = dok_matrix((no_selected_users, no_hotels), dtype=np.int32)

    row_index = 0
    for user_id in range(no_all_users):
        if is_active_user[user_id]:
            user_row = utility_matrix.getrow(user_id)
            user_row = list(zip(user_row.indices, user_row.data))
            for (column_index, rating) in user_row:
                filtered_utility_matrix[row_index, column_index] = rating
            row_index += 1

    print(f"Filtered utility matrix (min_reviews_number = {min_reviews_number})"
          f" shape: {filtered_utility_matrix.shape}")
    filtered_utility_matrix = filtered_utility_matrix.tocsr()
    save_npz("matrices/filtered_utility_matrix.npz", filtered_utility_matrix, True)
    return filtered_utility_matrix


def prepare_data():
    delete_matrices()
    create_test_utility_matrix()
    um = load_npz("matrices/utility_matrix.npz")
    print(f"Utility matrix shape: {um.shape}")
    delete_ratios = [0.05, 0.1, 0.15, 0.2, 0.25]
    for delete_ratio in delete_ratios:
        delete_ratings_in_utility_matrix(um, delete_ratio)

    f_um = filter_utility_matrix_by_active_users(um)
    for delete_ratio in delete_ratios:
        delete_ratings_in_utility_matrix(f_um, delete_ratio, "filtered_")


if __name__ == "__main__":
    prepare_data()
