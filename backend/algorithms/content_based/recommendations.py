import numpy as np
from scipy.sparse import lil_matrix

from algorithms.collaborative_filtering.utility_matrix import get_utility_matrix, delete_matrices
from algorithms.content_based.matrices import get_hotel_matrix, get_user_matrix
from algorithms.content_based.similarities import cosine_similarity
from authorization.models import User


def update_recommendations():
    delete_matrices()

    hotel_matrix = get_hotel_matrix()
    user_matrix = get_user_matrix()
    similarities = cosine_similarity(user_matrix, hotel_matrix.T)

    utility_matrix = get_utility_matrix()
    similarities = lil_matrix(np.where((utility_matrix.toarray() == 0), similarities.toarray(), 0))

    users = User.objects.all()
    # TODO update recommendations for every user
    for (user_index, user) in enumerate(users[:3]):
        user_row = np.array(similarities.data[user_index])
        hotel_indices = np.array(similarities.rows[user_index])
        sorted_data_indices = user_row.argsort()[::-1]
        # print([sim for sim in user_row[sorted_data_indices]])
        # print([hotel_index + 1 for hotel_index in hotel_indices[sorted_data_indices]])
        recommendations = [{"hotel_id": hotel_index + 1} for hotel_index in hotel_indices[sorted_data_indices]]
        user.average_stars = float(str(user.average_stars))
        user.recommendations = recommendations
        user.save()


if __name__ == "__main__":
    update_recommendations()

