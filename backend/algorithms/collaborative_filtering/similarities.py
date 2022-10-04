from scipy.sparse import load_npz
from sklearn.preprocessing import normalize


def jaccard_similarity():
    pass


def cosine_similarity(matrix, axis):
    # TODO write normalize on my own
    normalized_matrix_by_axis = normalize(matrix, axis=axis)
    if axis == 0:
        return normalized_matrix_by_axis.T * normalized_matrix_by_axis
    return normalized_matrix_by_axis * normalized_matrix_by_axis.T


um = load_npz("matrices/utility_matrix.npz")
cos_um = cosine_similarity(um, 0)
# for i in cos_um.data:
#     if i > 0.1 and i < 0.9:
#         print(i)
print(cos_um.data)
print(cos_um.shape)

cos_um = cosine_similarity(um, 1)
for i in cos_um.data:
    if i > 0.8 and i < 0.9:
        print(i)
print(cos_um.data)
print(cos_um.shape)
