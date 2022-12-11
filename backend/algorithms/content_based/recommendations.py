import numpy as np
from scipy.sparse import lil_matrix

from algorithms.collaborative_filtering.utility_matrix import get_utility_matrix, delete_matrices
from algorithms.content_based.matrices import get_hotel_matrix, get_user_matrix
from algorithms.content_based.similarities import cosine
from authorization.models import User


def update_recommendations():
    """
        Updates recommendations from content based algorithm in database
    """
    delete_matrices()

    hotel_matrix = get_hotel_matrix()
    user_matrix = get_user_matrix()
    similarities = cosine(user_matrix, hotel_matrix)

    utility_matrix = get_utility_matrix()
    similarities = lil_matrix(np.where((utility_matrix.toarray() == 0), similarities.toarray(), 0))

    users = User.objects.all()
    for (user_index, user) in enumerate(users):
        user_row = np.array(similarities.data[user_index])
        hotel_indices = np.array(similarities.rows[user_index])
        sorted_data_indices = user_row.argsort()[::-1]
        recommendations = [{"hotel_id": hotel_index + 1} for hotel_index in hotel_indices[sorted_data_indices]]
        user.average_stars = float(str(user.average_stars))
        user.recommendations = recommendations
        user.save()


if __name__ == "__main__":
    update_recommendations()


