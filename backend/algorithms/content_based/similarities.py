from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize


def cosine_similarity(matrix1, matrix2) -> csr_matrix:
    normalized_matrix1 = normalize(matrix1, axis=1)
    normalized_matrix2 = normalize(matrix2, axis=0)
    return normalized_matrix1 * normalized_matrix2
