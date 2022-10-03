import sys
import os
from pathlib import Path
import django
import numpy as np
from scipy.sparse import dok_matrix, save_npz

from algorithms.collaborative_filtering.algorithm_type import AlgorithmType


def create_utility_matrix(algorithm_type):
    sys.path.append(Path(__file__).parent.parent.parent.__str__())
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
    django.setup()
    from authorization.models import User
    from hotels.models import Hotel, Review

    no_users = User.objects.count()
    print("No.users: ", no_users)

    no_hotels = Hotel.objects.count()
    print("No.hotels:", no_hotels)

    reviews = Review.objects.all()
    print("No.reviews:", len(reviews))

    # the numbering of users and hotels starts from 1, so we take this into account in the dimensions of the matrix
    utility_matrix = dok_matrix((no_users + 1, no_hotels + 1), dtype=np.uint8)

    for review in reviews:
        user_id = review.user_id
        hotel_id = review.hotel_id
        utility_matrix[user_id, hotel_id] = review.stars

    print("Utility matrix created")
    save_npz(f"collaborative_filtering/utility_matrix_{algorithm_type.name}", utility_matrix.tocsr(), True)
    print("Utility matrix saved")


if __name__ == "__main__":
    create_utility_matrix(AlgorithmType.item_based)
