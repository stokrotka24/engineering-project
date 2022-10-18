import unittest
import numpy as np
from numpy.testing import assert_almost_equal

from algorithms.content_based.matrices import get_hotel_matrix, get_user_matrix


class TestMatrices(unittest.TestCase):
    def test_hotel_matrix(self):
        hotel_matrix = get_hotel_matrix()
        hotel_to_col_indices = {908: [232, 235, 264, 319, 321], 939: [232, 235, 264, 319, 321], 2221: [232, 235, 239, 264, 320]}
        for (hotel_index, col_indices) in hotel_to_col_indices.items():
            hotel_row = hotel_matrix[hotel_index, :]
            # test attributes (categories are in random order so impossible to test them)
            self.assertEqual(hotel_row.indices[-5:].tolist(), col_indices)

    def test_user_matrix(self):
        user_id = 2
        hotel_matrix = get_hotel_matrix()

        user_matrix = get_user_matrix()
        user_row = np.squeeze(user_matrix[user_id].toarray())
        # test attributes (categories are in random order so impossible to test them)
        user_row = user_row[232:]

        expected_user_row = np.zeros(hotel_matrix.shape[1])
        expected_user_row[239] = - 2 / 3
        expected_user_row[319] = 1 / 3
        expected_user_row[320] = - 2 / 3
        expected_user_row[321] = 1 / 3
        expected_user_row = expected_user_row[232:]
        assert_almost_equal(user_row, expected_user_row, decimal=15)
