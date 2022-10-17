import unittest
from algorithms.content_based.matrices import get_hotel_matrix


class TestMatrices(unittest.TestCase):
    def test_hotel_matrix(self):
        hotel_matrix = get_hotel_matrix()

        hotel_row = hotel_matrix[0, :]
        expected_indices = [0, 2]
        self.assertEqual(hotel_row.indices.tolist(), expected_indices)
