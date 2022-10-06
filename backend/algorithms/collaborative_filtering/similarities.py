import numpy as np
from scipy.sparse import load_npz, csr_matrix, csc_matrix

from sklearn.preprocessing import normalize


# caution: operation astype(float) change order of .data and .indices
def jaccard_similarity_no_acceleration(matrix: csr_matrix, axis) -> csc_matrix | csr_matrix:
    """
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
    dim1_indices = intersection_a_b.indices  # dim1 indexes for subsequent data in intersection_a_b.data
    size_a = sum_by_axis[dim1_indices]
    num_nnz_per_dim2 = intersection_a_b.getnnz(axis=0)  # number of nonzero elements in every dim2
    size_b = np.repeat(sum_by_axis, num_nnz_per_dim2)

    union_a_b = size_a + size_b - intersection_a_b.data
    union_a_b[union_a_b == 0] = 1
    intersection_a_b.data /= union_a_b

    return intersection_a_b


def jaccard_similarity(matrix: csr_matrix, axis) -> csc_matrix | csr_matrix:
    """
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


def cosine_similarity(matrix, axis) -> csr_matrix:
    normalized_matrix_by_axis = normalize(matrix, axis=axis)
    if axis == 0:
        return normalized_matrix_by_axis.T * normalized_matrix_by_axis
    return normalized_matrix_by_axis * normalized_matrix_by_axis.T

# um = load_npz("matrices/utility_matrix.npz")
# cos_um = my_cosine_similarity(um, 0)
# for i in cos_um.data:
#     if i > 0.1 and i < 0.9:
#         print(i)
# print(cos_um.data)
# print(cos_um.shape)

# cos_um = my_cosine_similarity(um, 1)
# for i in cos_um.data:
#     if 0.8 < i < 0.9:
#         print(i)
# print(cos_um.data)
# print(cos_um.shape)
