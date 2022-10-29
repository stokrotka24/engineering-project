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

no_users = User.objects.count()
no_hotels = Hotel.objects.count()


def create_utility_matrix():
    reviews = Review.objects.all()
    um = dok_matrix((no_users, no_hotels), dtype=np.int32)
    reviews_timestamps = dok_matrix((no_users, no_hotels), dtype=np.single)

    for review in reviews:
        user_id = review.user_id
        hotel_id = review.hotel_id
        # insert the newest review.stars
        if reviews_timestamps[user_id - 1, hotel_id - 1] < review.date.timestamp():
            um[user_id - 1, hotel_id - 1] = review.stars
            reviews_timestamps[user_id - 1, hotel_id - 1] = review.date.timestamp()

    print("Utility matrix created")
    um = um.tocsr()
    save_npz(f"{MATRICES_DIR}/utility_matrix", um, True)
    print("Utility matrix saved")


def get_utility_matrix():
    um_file = f"{MATRICES_DIR}/utility_matrix.npz"
    if not Path(um_file).is_file():
        create_utility_matrix()

    return load_npz(um_file)


def create_binary_utility_matrix(positive_threshold):
    """
    Creates and saves binary utility matrix:
        1 if rating is greater or equal to positive_threshold
        0 otherwise
    Binary utility matrix doesn't store explicit zeroes (even for items rated less than positive_threshold).

    Args:
        positive_threshold: number, above which rating will be treated as positive (=1)

    Returns:
        -
    """
    reviews = Review.objects.all()
    bin_um = dok_matrix((no_users, no_hotels), dtype=np.int32)
    reviews_timestamps = dok_matrix((no_users, no_hotels), dtype=np.single)

    for review in reviews:
        user_id = review.user_id
        hotel_id = review.hotel_id

        if reviews_timestamps[user_id - 1, hotel_id - 1] < review.date.timestamp():
            if review.stars >= positive_threshold:
                bin_um[user_id - 1, hotel_id - 1] = 1
            else:
                bin_um[user_id - 1, hotel_id - 1] = 0
            reviews_timestamps[user_id - 1, hotel_id - 1] = review.date.timestamp()

    print("Binary utility matrix created")
    bin_um = bin_um.tocsr()
    bin_um.eliminate_zeroes()
    save_npz(f"{MATRICES_DIR}/binary_utility_matrix_{positive_threshold}", bin_um, True)
    print("Binary utility matrix saved")


def get_binary_utility_matrix(positive_threshold):
    bin_um_file = f"{MATRICES_DIR}/binary_utility_matrix_{positive_threshold}.npz"
    if not Path(bin_um_file).is_file():
        create_binary_utility_matrix(positive_threshold)

    return load_npz(bin_um_file)


def get_rating_mean_per_user(utility_matrix):
    rating_sum = utility_matrix.sum(axis=1).A1
    rating_num = np.diff(utility_matrix.indptr)
    rating_num[rating_num == 0] = 1  # to avoid division by 0
    return rating_sum / rating_num


def create_normalized_utility_matrix_no_acceleration():
    """
        Creates and saves normalized utility matrix (subtracting user's average).
        Normalized utility matrix doesn't store explicit zeroes (even for items rated equal to user's average).

        Returns:
            -
        """
    um = get_utility_matrix()
    rating_mean = get_rating_mean_per_user(um)

    normalized_um = dok_matrix((no_users, no_hotels), dtype=np.float64)
    for user_id in range(no_users):
        user_row = um.getrow(user_id)
        hotel_ids = user_row.indices
        ratings = user_row.data
        data_size = len(ratings)
        for i in range(data_size):
            normalized_um[user_id, hotel_ids[i]] = ratings[i] - rating_mean[user_id]

    print("Normalized utility matrix created")
    save_npz(f"{MATRICES_DIR}/normalized_utility_matrix_no_acc", normalized_um.tocsr(), True)
    print("Normalized utility matrix saved")


def create_normalized_utility_matrix():
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
