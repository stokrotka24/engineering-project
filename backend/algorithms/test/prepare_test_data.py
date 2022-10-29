from algorithms.collaborative_filtering.utility_matrix import create_utility_matrix, create_binary_utility_matrix, \
    delete_matrices, create_normalized_utility_matrix

FIRST_TEST_USER_ID = 3
NO_USERS = 152760

FIRST_TEST_HOTEL_ID = 1
NO_HOTELS = 2977


def utility_matrix():
    create_utility_matrix(user_bias=FIRST_TEST_USER_ID, hotel_bias=FIRST_TEST_HOTEL_ID,
                          no_users=NO_USERS, no_hotels=NO_HOTELS)


def binary_utility_matrix(positive_threshold):
    create_binary_utility_matrix(positive_threshold=positive_threshold,
                                 user_bias=FIRST_TEST_USER_ID, hotel_bias=FIRST_TEST_HOTEL_ID,
                                 no_users=NO_USERS, no_hotels=NO_HOTELS)


def normalized_utility_matrix():
    create_normalized_utility_matrix()


def prepare_data():
    delete_matrices()
    utility_matrix()
    for i in range(1, 6):
        binary_utility_matrix(i)
    normalized_utility_matrix()


if __name__ == "__main__":
    prepare_data()
