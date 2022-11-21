from pathlib import Path

import numpy as np
from scipy.sparse import dok_matrix, save_npz, load_npz, csr_matrix

from algorithms.collaborative_filtering.utility_matrix import get_normalized_utility_matrix, get_utility_matrix
from algorithms.content_based.map_features_to_index import enum_name_to_class, \
    embedded_attr_name_to_class, create_map_feature_to_index
from hotels.models import Hotel

MATRICES_DIR = "matrices"


def create_hotel_matrix():
    map_feature_to_col_index, no_columns = create_map_feature_to_index()
    print(map_feature_to_col_index)
    hotels = Hotel.objects.all()
    no_rows = len(hotels)
    hotel_matrix = dok_matrix((no_rows, no_columns), dtype=np.int32)
    for (hotel_index, hotel) in enumerate(hotels):
        categories = hotel.categories
        for category in categories:
            column_index = map_feature_to_col_index[category['name']]
            hotel_matrix[hotel_index, column_index] = 1

        attrs = hotel.attributes
        if attrs is not None:
            for (attr_key, attr_val) in attrs.items():
                if attr_key in embedded_attr_name_to_class.keys():
                    for (emb_attr_key, emb_attr_val) in attr_val.items():
                        if emb_attr_val:
                            column_index = map_feature_to_col_index[attr_key][emb_attr_key]
                            hotel_matrix[hotel_index, column_index] = 1

                elif attr_key in enum_name_to_class.keys():
                    if attr_val is not None:
                        column_index = map_feature_to_col_index[attr_key][attr_val.name]
                        hotel_matrix[hotel_index, column_index] = 1

                elif attr_val:
                    try:
                        column_index = map_feature_to_col_index[attr_key]
                        hotel_matrix[hotel_index, column_index] = 1
                    except KeyError:
                        pass
                        # print("Unsupported attribute:", attr_key)

    hotel_matrix = hotel_matrix.tocsr()
    save_npz("matrices/hotel_matrix.npz", hotel_matrix, True)
    return hotel_matrix


def get_hotel_matrix():
    hotel_matrix_file = f"{MATRICES_DIR}/hotel_matrix.npz"
    if not Path(hotel_matrix_file).is_file():
        return create_hotel_matrix()

    return load_npz(hotel_matrix_file)


def create_user_matrix():
    hotel_matrix = get_hotel_matrix()
    normalized_utility_matrix = get_normalized_utility_matrix()
    utility_matrix = get_utility_matrix()
    utility_matrix_ones = utility_matrix.copy()
    utility_matrix_ones.data = np.ones_like(utility_matrix.data)

    ratings_sum = normalized_utility_matrix * hotel_matrix
    ratings_num = utility_matrix_ones * hotel_matrix
    user_matrix = ratings_sum / ratings_num

    user_matrix[np.isnan(user_matrix)] = 0
    user_matrix = csr_matrix(user_matrix)

    save_npz("matrices/user_matrix.npz", user_matrix, True)
    return user_matrix


def get_user_matrix():
    user_matrix_file = f"{MATRICES_DIR}/user_matrix.npz"
    if not Path(user_matrix_file).is_file():
        return create_user_matrix()

    return load_npz(user_matrix_file)


if __name__ == "__main__":
    create_hotel_matrix()
    create_user_matrix()
