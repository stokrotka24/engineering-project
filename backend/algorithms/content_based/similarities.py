from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize


def cosine(user_matrix, hotel_matrix) -> csr_matrix:
    """
    Calculates cosine similarities between each row of user matrix and each row of hotel matrix.
    It represents similarity between users and hotels.

    Args:
        user_matrix:
        hotel_matrix:

    Returns:
        similarity matrix
    """
    normalized_user_matrix = normalize(user_matrix, axis=1)
    normalized_hotel_matrix = normalize(hotel_matrix, axis=1)
    normalized_hotel_matrix = normalized_hotel_matrix.T
    return normalized_user_matrix * normalized_hotel_matrix
