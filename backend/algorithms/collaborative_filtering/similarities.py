import numpy as np
from scipy.sparse import load_npz, csr_matrix, csc_matrix

from sklearn.preprocessing import normalize


# caution: operation astype(float) change order of .data and .indices
def jaccard_similarity_no_acceleration(matrix: csr_matrix, axis) -> csc_matrix | csr_matrix:
    """
    Calculates jaccard similarities between each row (axis=1)/each column (axis=0) of matrix.

    Args:
        matrix: binary utility matrix
        axis: which dimension of matrix is considered

    Returns:
        csc_matrix (if axis =  0)
        csr_matrix (if axis =  1)

    """

    matrix_copy = matrix.copy().astype(float)
    sum_by_axis = matrix_copy.getnnz(axis=axis)

    if axis == 0:
        intersection_a_b: csc_matrix = matrix_copy.T * matrix_copy
    else:
        intersection_a_b: csr_matrix = matrix_copy * matrix_copy.T
    # dim1 = row if axis = 0 else col
    # dim2 = col if axis = 0 else row
    dim1_indices = intersection_a_b.indices  # dim1 indexes for subsequent data in intersection_a_b.data
    size_a = sum_by_axis[dim1_indices]
    num_nnz_per_dim2 = intersection_a_b.getnnz(axis=0)  # number of nonzero elements in every dim2
    size_b = np.repeat(sum_by_axis, num_nnz_per_dim2)

    union_a_b = size_a + size_b - intersection_a_b.data
    union_a_b[union_a_b == 0] = 1
    intersection_a_b.data /= union_a_b

    return intersection_a_b


def jaccard(matrix: csr_matrix, axis) -> csc_matrix | csr_matrix:
    """
    Calculates jaccard similarities between each row (axis=1)/each column (axis=0) of matrix.

    Args:
        matrix: binary utility matrix
        axis: which dimension of matrix is considered

    Returns:
        csc_matrix (if axis =  0)
        csr_matrix (if axis =  1)

    """

    matrix_copy = matrix.copy().astype(float)
    sum_by_axis = matrix_copy.getnnz(axis=axis)

    if axis == 0:
        intersection_a_b: csc_matrix = matrix_copy.T * matrix_copy
        row_indices = intersection_a_b.indices  # row indexes for subsequent data in intersection_a_b.data
        size_a = sum_by_axis[row_indices]

        num_nnz_per_col = intersection_a_b.getnnz(axis=0)  # number of nonzero elements in every column
        size_b = np.repeat(sum_by_axis, num_nnz_per_col)
    else:
        intersection_a_b: csr_matrix = matrix_copy * matrix_copy.T
        num_nnz_per_row = intersection_a_b.getnnz(axis=1)  # number of nonzero elements in every row
        size_a = np.repeat(sum_by_axis, num_nnz_per_row)

        col_indices = intersection_a_b.indices  # col indexes for subsequent data in intersection_a_b.data
        size_b = sum_by_axis[col_indices]

    union_a_b = size_a + size_b - intersection_a_b.data
    union_a_b[union_a_b == 0] = 1
    intersection_a_b.data /= union_a_b

    return intersection_a_b


def cosine(matrix, axis) -> csr_matrix:
    """
        Calculates cosine similarities between each row (axis=1)/each column (axis=0) of matrix.

        Args:
            matrix: binary utility matrix
            axis: which dimension of matrix is considered

        Returns:
            csc_matrix (if axis =  0)
            csr_matrix (if axis =  1)

        """
    normalized_matrix_by_axis = normalize(matrix, axis=axis)
    if axis == 0:
        return normalized_matrix_by_axis.T * normalized_matrix_by_axis
    return normalized_matrix_by_axis * normalized_matrix_by_axis.T

