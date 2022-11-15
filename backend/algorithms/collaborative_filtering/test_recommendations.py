import time
import unittest

import numpy as np
from scipy.sparse import csr_matrix

from algorithms.collaborative_filtering.recommendations import jaccard_cf
from algorithms.test.algorithm_type import AlgorithmType


class TestRecommendations(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.um = csr_matrix(np.array(
            [[3, 4, 0, 4, 5],
             [0, 3, 0, 0, 0],
             [0, 3, 0, 5, 3],
             [0, 1, 0, 2, 0],
             [4, 0, 0, 0, 3],
             [5, 2, 1, 0, 3]]
        ))

        cls.bin_um_positive_threshold_3 = csr_matrix(np.array(
            [[1, 1, 0, 1, 1],
             [0, 1, 0, 0, 0],
             [0, 1, 0, 1, 1],
             [0, 0, 0, 0, 0],
             [1, 0, 0, 0, 1],
             [1, 0, 0, 0, 1]]
        ))

    def test_jaccard_item_based_weighted_average_True(self):
        predicted_ratings = jaccard_cf(axis=AlgorithmType.item_based.value, n=2,
                                       weighted_average=True,
                                       utility_matrix=self.um,
                                       binary_utility_matrix=self.bin_um_positive_threshold_3)
        self.assertTrue(np.isnan(predicted_ratings[0, 2]))
        self.assertTrue(np.isnan(predicted_ratings[1, 0]))
        self.assertTrue(np.isnan(predicted_ratings[1, 2]))
        self.assertEqual(3, predicted_ratings[1, 3])
        self.assertTrue(np.isnan(predicted_ratings[1, 4]))
        self.assertEqual(3.5, predicted_ratings[2, 0])
        self.assertTrue(np.isnan(predicted_ratings[2, 2]))
        self.assertTrue(2, np.isnan(predicted_ratings[3, 0]))
        self.assertTrue(np.isnan(predicted_ratings[3, 2]))
        self.assertTrue(2, np.isnan(predicted_ratings[3, 4]))
        self.assertTrue(3, np.isnan(predicted_ratings[4, 1]))
        self.assertTrue(np.isnan(predicted_ratings[4, 2]))
        self.assertTrue(3, np.isnan(predicted_ratings[4, 3]))
        self.assertTrue(np.isnan(predicted_ratings[5, 2]))
        self.assertTrue(17/7, np.isnan(predicted_ratings[5, 3]))


if __name__ == '__main__':
    unittest.main()
