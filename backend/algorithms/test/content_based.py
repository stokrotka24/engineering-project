import math
import shelve
from collections import defaultdict
from scipy.sparse import load_npz
from algorithms.content_based.matrices import get_hotel_matrix, get_user_matrix
from algorithms.content_based.similarities import cosine_similarity


def infinity_norm_for_indices_difference(l1: list, l2: list):
    max_difference = 0
    for (index1, elem) in enumerate(l1):
        index2 = l2.index(elem)
        difference = abs(index2 - index1)
        if difference > max_difference:
            max_difference = difference
    return max_difference


def sum_squared_error(l1: list, l2: list):
    s = 0
    for (index1, elem) in enumerate(l1):
        index2 = l2.index(elem)
        s += (index2 - index1) ** 2
    return s


def kendall_tau_distance(l1: list, l2: list):
    pass


def discounted_cumulative_gain(recommendation_list, user_id, ratings):
    hotel_id = recommendation_list[0]
    s = ratings[user_id, hotel_id]
    for (index, hotel_id) in enumerate(recommendation_list[1:]):
        s += ratings[user_id, hotel_id] / math.log2(index + 2)
    return s


def calc_mean_per_list_size(d: dict):
    return list(map(lambda t: (t[0], sum(t[1]) / len(t[1])), d.items()))


def test(delete_ratio=0.0):
    hotel_matrix = get_hotel_matrix()
    user_matrix = get_user_matrix()
    similarities = cosine_similarity(user_matrix, hotel_matrix.T)

    utility_matrix = load_npz("matrices/utility_matrix.npz")
    if delete_ratio > 0.0:
        file = shelve.open("matrices/deleted_ratings_0.2.bin")
        ratings = file["deleted_ratings"]
    else:
        utility_matrix = utility_matrix.todok()
        ratings = list(utility_matrix.keys())

    ratings_map = defaultdict(list)
    for (user_id, hotel_id) in ratings:
        ratings_map[user_id].append(hotel_id)

    infinity_norms = defaultdict(list)
    sum_squared_errors = defaultdict(list)
    discounted_cumulative_gains = defaultdict(list)
    normalized_discounted_cumulative_gains = defaultdict(list)

    for (user_id, hotel_indices) in ratings_map.items():
        if user_id % 1000 == 0:
            print(user_id)
        similarities_for_user = []
        user_ratings = []
        for hotel_id in hotel_indices:
            similarities_for_user.append((hotel_id, similarities[user_id, hotel_id]))
            user_ratings.append((hotel_id, utility_matrix[user_id, hotel_id]))

        similarities_for_user.sort(key=lambda t: t[1], reverse=True)
        hotel_sorted_by_recommendation = list(map(lambda t: t[0], similarities_for_user))
        user_ratings.sort(key=lambda t: t[1], reverse=True)
        hotel_sorted_by_ratings = list(map(lambda t: t[0], user_ratings))

        infinity_norms[len(hotel_indices)] \
            .append(infinity_norm_for_indices_difference(hotel_sorted_by_ratings, hotel_sorted_by_recommendation))
        # print(infinity_norm_for_indices_difference(hotel_sorted_by_ratings, hotel_sorted_by_recommendation))
        sum_squared_errors[len(hotel_indices)] \
            .append(sum_squared_error(hotel_sorted_by_ratings, hotel_sorted_by_recommendation))
        # print(sum_squared_error(hotel_sorted_by_ratings, hotel_sorted_by_recommendation))

        dcg = discounted_cumulative_gain(hotel_sorted_by_recommendation, user_id, utility_matrix)
        discounted_cumulative_gains[len(hotel_indices)].append(dcg)
        # print(discounted_cumulative_gain(hotel_sorted_by_recommendation, user_id, utility_matrix))
        normalized_discounted_cumulative_gains[len(hotel_indices)] \
            .append(dcg / discounted_cumulative_gain(hotel_sorted_by_ratings, user_id, utility_matrix))

    infinity_norms = calc_mean_per_list_size(infinity_norms)
    print("infinity_norms\n", infinity_norms)

    sum_squared_errors = calc_mean_per_list_size(sum_squared_errors)
    print("sum_squared_errors\n", sum_squared_errors)

    discounted_cumulative_gains = calc_mean_per_list_size(discounted_cumulative_gains)
    print("discounted_cumulative_gains\n", discounted_cumulative_gains)

    normalized_discounted_cumulative_gains = calc_mean_per_list_size(normalized_discounted_cumulative_gains)
    print("normalized_discounted_cumulative_gains\n", normalized_discounted_cumulative_gains)


test(0.0)
