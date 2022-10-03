import numpy as np


def jaccard_distance(a: np.array, b: np.array) -> float:
    """
    Calculate Jaccard distance between two 1-d vectors.

    Args:
        a: 1-d numpy array
        b: 1-d numpy array

    Returns:
        Jaccard distance between inputs.
    """

    if a.size != b.size:
        raise Exception("Vectors must have the same size to calc Jaccard distance")

    intersection = np.logical_and(a, b).sum()
    union = np.logical_or(a, b).sum()
    return 1 - intersection / union


def cosine_distance(a: np.array, b: np.array) -> float:
    """
    Calculate cosine distance between two 1-d vectors.

    Args:
        a: 1-d numpy array
        b: 1-d numpy array

    Returns:
        Cosine distance between inputs.
    """
    if a.size != b.size:
        raise Exception("Vectors must have the same size to calc cosine distance")

    dot_product = np.dot(a, b)
    norm_product = np.linalg.norm(a) * np.linalg.norm(b)
    return 1 - dot_product / norm_product


# TODO remove
# x = np.array([4444, 0, 1, 0])
# y = np.array([1, 0, 0, 1])
# print(jaccard_distance(x, y))
# x = np.array([3, 4])
# y = np.array([1, 0])
# print(cosine_distance(x, y))
