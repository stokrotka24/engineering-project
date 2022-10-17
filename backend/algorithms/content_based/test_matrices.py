import unittest
from algorithms.content_based.matrices import get_hotel_matrix


class TestMatrices(unittest.TestCase):
    def test_hotel_matrix(self):
        hotel_matrix = get_hotel_matrix()

        hotel_row = hotel_matrix[0, :]
        expected_indices = [1, 3, 7, 10, 13, 16, 19, 22, 25, 28, 35, 39, 40, 43,
                            46, 49, 52, 55, 58, 61, 64, 67, 70, 73, 76, 79, 82,
                            85, 88, 91, 94, 100, 104, 105, 108, 111, 117, 118,
                            121, 124, 127, 130, 133, 136, 139, 142, 145, 148,
                            151, 154, 157, 160, 163, 166, 169, 172, 175, 178,
                            181, 184, 187, 190, 193, 196]
        self.assertEqual(hotel_row.indices.tolist(), expected_indices)
