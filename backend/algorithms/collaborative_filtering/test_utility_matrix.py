import time
import unittest

from scipy.sparse import load_npz

from utility_matrix import create_normalized_utility_matrix_no_acceleration, \
    create_normalized_utility_matrix, get_utility_matrix, get_binary_utility_matrix, get_normalized_utility_matrix


def func_name(f):
    def wrap(*args, **kwargs):
        print(f.__name__)
        f(*args, **kwargs)

    return wrap


class TestUtilityMatrices(unittest.TestCase):
    def test_utility_matrix(self):
        utility_matrix = get_utility_matrix()
        self.assertEqual(utility_matrix[2, 908], 2)

    def test_binary_utility_matrix(self):
        binary_utility_matrix = get_binary_utility_matrix(3)
        self.assertEqual(binary_utility_matrix[2, 908], 0)

    def test_normalized_utility_matrix(self):
        start = time.time()
        create_normalized_utility_matrix_no_acceleration()
        elapsed_no_acc = time.time() - start

        start = time.time()
        create_normalized_utility_matrix()
        elapsed = time.time() - start

        normalized_utility_matrix_1 = load_npz(f"matrices/normalized_utility_matrix_no_acc.npz")
        self.assertAlmostEqual(normalized_utility_matrix_1[2, 908], - 2/3, places=15)

        normalized_utility_matrix_2 = load_npz(f"matrices/normalized_utility_matrix.npz")
        self.assertAlmostEqual(normalized_utility_matrix_2[2, 908], - 2/3, places=15)

        self.assertTrue((normalized_utility_matrix_1 != normalized_utility_matrix_2).nnz == 0)

        print("no acc/with acc implementation time =",
              elapsed_no_acc / elapsed)

        user_id = 2

        um = get_utility_matrix()
        user_row = um.getrow(user_id)
        ratings_sum = sum(user_row.data)
        ratings_num = len(user_row.data)
        rating_mean = ratings_sum / ratings_num
        normalized_user_row = user_row.copy()
        normalized_user_row.astype(float)
        normalized_user_row.data = normalized_user_row.data - rating_mean
        normalized_um = get_normalized_utility_matrix()
        self.assertTrue((normalized_user_row != normalized_um[user_id]).nnz == 0)


if __name__ == '__main__':
    unittest.main()
