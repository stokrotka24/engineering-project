from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize


def cosine(user_matrix, hotel_matrix) -> csr_matrix:
    normalized_user_matrix = normalize(user_matrix, axis=1)
    normalized_hotel_matrix = normalize(hotel_matrix, axis=1)
    normalized_hotel_matrix = normalized_hotel_matrix.T
    return normalized_user_matrix * normalized_hotel_matrix
