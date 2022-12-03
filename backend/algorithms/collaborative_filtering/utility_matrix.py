import sys
import os
from pathlib import Path
import django
import numpy as np
from scipy.sparse import dok_matrix, save_npz, load_npz, diags

MATRICES_DIR = "matrices"
sys.path.append(Path(__file__).parent.parent.parent.__str__())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()
from authorization.models import User
from hotels.models import Hotel, Review


first_user_id = User.objects.first().id
first_hotel_id = Hotel.objects.first().id
last_user_id = User.objects.last().id
last_hotel_id = Hotel.objects.last().id


def create_utility_matrix(user_bias=first_user_id, hotel_bias=first_hotel_id,
                          max_user_id=last_user_id, max_hotel_id=last_hotel_id):
    """
    Creates standard utility matrix from user ratings.

    Args:
        user_bias: how many first users omit
        hotel_bias: how many first hotels omit
        max_user_id: maximum user id that will be included in matrix
        max_hotel_id: maximum user id that will be included in matrix
    """
    reviews = Review.objects.all()
    no_users = max_user_id - user_bias + 1
    no_hotels = max_hotel_id - hotel_bias + 1
    um = dok_matrix((no_users, no_hotels), dtype=np.int32)
    reviews_timestamps = dok_matrix((no_users, no_hotels), dtype=np.single)

    for review in reviews:
        user_id = review.user_id - user_bias
        hotel_id = review.hotel_id - hotel_bias
        # insert the newest review.stars
        if reviews_timestamps[user_id, hotel_id] < review.date.timestamp():
            um[user_id, hotel_id] = review.stars
            reviews_timestamps[user_id, hotel_id] = review.date.timestamp()

    print("Utility matrix created")
    um = um.tocsr()
    save_npz(f"{MATRICES_DIR}/utility_matrix", um, True)
    print("Utility matrix saved")


def get_utility_matrix():
    um_file = f"{MATRICES_DIR}/utility_matrix.npz"
    if not Path(um_file).is_file():
        create_utility_matrix()

    return load_npz(um_file)


def create_binary_utility_matrix(positive_threshold, user_bias=first_user_id, hotel_bias=first_hotel_id,
                                 max_user_id=last_user_id, max_hotel_id=last_hotel_id):
    """
    Creates and saves binary utility matrix:
        1 if rating is greater or equal to positive_threshold
        0 otherwise
    Binary utility matrix doesn't store explicit zeroes (even for items rated less than positive_threshold).

    Args:
        positive_threshold: number, above which rating will be treated as positive (=1)
        user_bias: how many first users omit
        hotel_bias: how many first hotels omit
        max_user_id: maximum user id that will be included in matrix
        max_hotel_id: maximum user id that will be included in matrix
    """
    reviews = Review.objects.all()
    no_users = max_user_id - user_bias + 1
    no_hotels = max_hotel_id - hotel_bias + 1
    bin_um = dok_matrix((no_users, no_hotels), dtype=np.int32)
    reviews_timestamps = dok_matrix((no_users, no_hotels), dtype=np.single)

    for review in reviews:
        user_id = review.user_id - user_bias
        hotel_id = review.hotel_id - hotel_bias

        if reviews_timestamps[user_id, hotel_id] < review.date.timestamp():
            if review.stars >= positive_threshold:
                bin_um[user_id, hotel_id] = 1
            else:
                bin_um[user_id, hotel_id] = 0
            reviews_timestamps[user_id, hotel_id] = review.date.timestamp()

    print("Binary utility matrix created")
    bin_um = bin_um.tocsr()
    bin_um.eliminate_zeros()
    save_npz(f"{MATRICES_DIR}/binary_utility_matrix_{positive_threshold}", bin_um, True)
    print("Binary utility matrix saved")


def get_binary_utility_matrix(positive_threshold):
    bin_um_file = f"{MATRICES_DIR}/binary_utility_matrix_{positive_threshold}.npz"
    if not Path(bin_um_file).is_file():
        create_binary_utility_matrix(positive_threshold)

    return load_npz(bin_um_file)


def get_rating_mean_per_user(utility_matrix):
    """
    Returns:
        vector with mean value of each row in utility matrix
    """

    rating_sum = utility_matrix.sum(axis=1).A1
    rating_num = np.diff(utility_matrix.indptr)
    rating_num[rating_num == 0] = 1  # to avoid division by 0
    return rating_sum / rating_num


def create_normalized_utility_matrix_no_acceleration():
    """
    Creates and saves normalized utility matrix (subtracting user's average).
    Normalized utility matrix doesn't store explicit zeroes (even for items rated equal to user's average).
    """
    um = get_utility_matrix()
    no_users, no_hotels = um.shape
    rating_mean = get_rating_mean_per_user(um)

    normalized_um = dok_matrix((no_users, no_hotels), dtype=np.float64)
    for user_id in range(no_users):
        user_row = um.getrow(user_id)
        hotel_ids = user_row.indices
        ratings = user_row.data
        for (hotel_id, rating) in zip(hotel_ids, ratings):
            normalized_um[user_id, hotel_id] = rating - rating_mean[user_id]

    normalized_um = normalized_um.tocsr()
    print("Normalized utility matrix created")
    save_npz(f"{MATRICES_DIR}/normalized_utility_matrix_no_acc", normalized_um, True)
    print("Normalized utility matrix saved")


def create_normalized_utility_matrix():
    """
    Creates and saves normalized utility matrix (subtracting user's average).
    Normalized utility matrix doesn't store explicit zeroes (even for items rated equal to user's average).
    """
    um = get_utility_matrix()
    rating_mean = get_rating_mean_per_user(um)

    rating_mean = diags(diagonals=rating_mean, offsets=0)
    ones = um.copy()
    ones.data = np.ones_like(um.data)
    normalized_um = um - rating_mean * ones
    print("Normalized utility matrix created")
    save_npz(f"{MATRICES_DIR}/normalized_utility_matrix", normalized_um, True)
    print("Normalized utility matrix saved")


def get_normalized_utility_matrix():
    normalized_um_file = f"{MATRICES_DIR}/normalized_utility_matrix.npz"
    if not Path(normalized_um_file).is_file():
        create_normalized_utility_matrix()

    return load_npz(normalized_um_file)


def delete_matrices():
    for file in os.listdir(MATRICES_DIR):
        os.remove(os.path.join(MATRICES_DIR, file))


if __name__ == "__main__":
    create_utility_matrix()
    create_binary_utility_matrix(3)
    create_normalized_utility_matrix_no_acceleration()
    create_normalized_utility_matrix()
