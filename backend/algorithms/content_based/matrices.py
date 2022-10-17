from pathlib import Path

import numpy as np
from scipy.sparse import dok_matrix, save_npz, load_npz

from algorithms.collaborative_filtering.utility_matrix import get_normalized_utility_matrix
from algorithms.content_based.map_attributes_to_index import create_map_attributes_to_index, enum_name_to_class, \
    embedded_attr_name_to_class, null_boolean_values
from authorization.models import User
from hotels.models import Hotel, Review

MATRICES_DIR = "matrices"


def create_hotel_matrix():
    map_attribute_to_index, no_columns = create_map_attributes_to_index()
    print(map_attribute_to_index)
    hotels = Hotel.objects.all()
    no_rows = len(hotels)
    hotel_matrix = dok_matrix((no_rows, no_columns), dtype=np.int32)
    for (hotel_index, hotel) in enumerate(hotels):
        attrs = hotel.attributes
        if attrs is not None:
            for (attr_key, attr_val) in attrs.items():
                if attr_key in embedded_attr_name_to_class.keys():
                    for (emb_attr_key, emb_attr_val) in attr_val.items():
                        column_index = map_attribute_to_index[attr_key][emb_attr_key][emb_attr_val]
                        hotel_matrix[hotel_index, column_index] = 1

                elif attr_key in enum_name_to_class.keys():
                    if attr_val is None:
                        column_index = map_attribute_to_index[attr_key][None]
                    else:
                        column_index = map_attribute_to_index[attr_key][attr_val.name]
                    hotel_matrix[hotel_index, column_index] = 1

                elif attr_val in null_boolean_values:
                    try:
                        column_index = map_attribute_to_index[attr_key][attr_val]
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
    reviews = Review.objects.all()
    users = User.objects.all()

    normalized_utility_matrix = get_normalized_utility_matrix()


if __name__ == "__main__":
    # create_hotel_matrix()
    create_user_matrix()
