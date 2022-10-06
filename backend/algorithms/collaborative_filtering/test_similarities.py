import time
import unittest

import numpy as np
from numpy.testing import assert_array_equal, assert_allclose
from scipy.sparse import csr_matrix, load_npz

import similarities
from sklearn.metrics import pairwise, pairwise_distances

from test_utility_matrix import func_name


class TestSimilarities(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.binary_utility_matrix = csr_matrix(np.array(
            [[1, 1, 0, 1, 1],
             [0, 1, 0, 0, 0],
             [0, 1, 0, 1, 1],
             [0, 0, 0, 0, 0],
             [1, 0, 0, 0, 1],
             [0, 0, 0, 0, 1]]
        ))
        # cls.binary_utility_matrix = load_npz("matrices/binary_utility_matrix_3.npz")
        cls.utility_matrix = csr_matrix(np.array(
            [[3, 4, 0, 4, 5],
             [0, 3, 0, 0, 0],
             [0, 3, 0, 5, 3],
             [0, 1, 0, 2, 0],
             [4, 0, 0, 0, 3],
             [5, 2, 1, 0, 3]]
        ))
        # cls.utility_matrix = load_npz("matrices/utility_matrix.npz")

    @func_name
    def test_jaccard_similarity_item_based(self):
        start = time.time()
        actual = similarities.jaccard_similarity(self.binary_utility_matrix, 0)
        elapsed = time.time() - start
        actual = actual.tolil()
        actual.setdiag(1.0)
        actual = actual.toarray()

        binary_utility_matrix_transpose = self.binary_utility_matrix.T.astype(bool).toarray()
        start = time.time()
        expected = 1 - pairwise_distances(binary_utility_matrix_transpose, metric='jaccard')
        elapsed_lib = time.time() - start

        print("library/tested implementation time =", elapsed_lib / elapsed)  # but library works worse for real bin_um

        assert_allclose(actual, expected, rtol=0, atol=1.0e-15)

    @func_name
    def test_jaccard_similarity_user_based(self):
        start = time.time()
        actual = similarities.jaccard_similarity(self.binary_utility_matrix, 1)
        elapsed = time.time() - start
        actual = actual.tolil()
        actual.setdiag(1.0)
        actual = actual.toarray()

        binary_utility_matrix = self.binary_utility_matrix.astype(bool).toarray()
        start = time.time()
        expected = 1 - pairwise_distances(binary_utility_matrix, metric='jaccard')
        elapsed_lib = time.time() - start

        print("library/tested implementation time =", elapsed_lib / elapsed)  # but library works worse for real bin_um

        assert_allclose(actual, expected, rtol=0, atol=1.0e-15)

    @func_name
    def test_jaccard_similarity_item_based_no_acceleration(self):
        start = time.time()
        result_no_acc = similarities.jaccard_similarity_no_acceleration(self.binary_utility_matrix, 0)
        elapsed_no_acc = time.time() - start

        start = time.time()
        result = similarities.jaccard_similarity_no_acceleration(self.binary_utility_matrix, 0)
        elapsed = time.time() - start

        print("no acc/with acc implementation time =",
              elapsed_no_acc / elapsed)  # but library works worse for real bin_um

        self.assertTrue((result_no_acc != result).nnz == 0)

    @func_name
    def test_jaccard_similarity_user_based_no_acceleration(self):
        start = time.time()
        result_no_acc = similarities.jaccard_similarity_no_acceleration(self.binary_utility_matrix, 1)
        elapsed_no_acc = time.time() - start

        start = time.time()
        result = similarities.jaccard_similarity_no_acceleration(self.binary_utility_matrix, 1)
        elapsed = time.time() - start

        print("no acc/with acc implementation time =",
              elapsed_no_acc / elapsed)  # but library works worse for real bin_um

        self.assertTrue((result_no_acc != result).nnz == 0)

    @func_name
    def test_cosine_similarity_item_based(self):
        start = time.time()
        actual = similarities.cosine_similarity(self.utility_matrix, 0)
        elapsed = time.time() - start
        actual = actual.toarray()

        utility_matrix_transpose = self.utility_matrix.T
        start = time.time()
        expected = pairwise.cosine_similarity(utility_matrix_transpose, utility_matrix_transpose)
        elapsed_lib = time.time() - start

        print("library/tested implementation time =", elapsed_lib / elapsed)

        assert_array_equal(actual, expected)

    @func_name
    def test_cosine_similarity_user_based(self):
        start = time.time()
        actual = similarities.cosine_similarity(self.utility_matrix, 1)
        elapsed = time.time() - start
        actual = actual.toarray()

        start = time.time()
        expected = pairwise.cosine_similarity(self.utility_matrix, self.utility_matrix)
        elapsed_lib = time.time() - start

        print("library/tested implementation time =", elapsed_lib / elapsed)

        assert_array_equal(actual, expected)


if __name__ == '__main__':
    unittest.main()
