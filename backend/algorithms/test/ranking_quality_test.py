import math
import shelve
import time
from collections import defaultdict
from scipy.sparse import load_npz
from algorithms.content_based.matrices import create_hotel_matrix
from algorithms.content_based.similarities import cosine
from algorithms.test.prepare_test_data import prepare_user_matrix


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
    length = len(l1)

    d = 0
    for i in range(length):
        for j in range(i + 1, length):
            elem1 = l1[i]
            elem2 = l1[j]

            if l2.index(elem1) > l2.index(elem2):
                d += 1
    return d


def discounted_cumulative_gain(recommendation_list, user_id, ratings):
    hotel_id = recommendation_list[0]
    s = ratings[user_id, hotel_id]
    for (index, hotel_id) in enumerate(recommendation_list[1:]):
        s += ratings[user_id, hotel_id] / math.log2(index + 2)
    return s


def calc_mean_per_list_size(d: dict):
    return list(map(lambda t: (t[0], sum(t[1]) / len(t[1])), d.items()))


def calc_ranking_quality_measures(recommendations, deleted_ratings, utility_matrix):
    deleted_ratings_map = defaultdict(list)
    for (user_id, hotel_id) in deleted_ratings:
        deleted_ratings_map[user_id].append(hotel_id)

    infinity_norms = defaultdict(list)
    sum_squared_errors = defaultdict(list)
    kendall_tau_distances = defaultdict(list)
    discounted_cumulative_gains = defaultdict(list)
    max_discounted_cumulative_gains = defaultdict(list)
    normalized_discounted_cumulative_gains = defaultdict(list)
    min_normalized_discounted_cumulative_gains = defaultdict(list)

    for (user_id, hotel_indices) in deleted_ratings_map.items():
        if user_id % 5000 == 0:
            print(user_id)
        recommendations_for_user = []
        user_ratings = []
        for hotel_id in hotel_indices:
            recommendations_for_user.append((hotel_id, recommendations[user_id, hotel_id]))
            user_ratings.append((hotel_id, utility_matrix[user_id, hotel_id]))

        recommendations_for_user.sort(key=lambda t: t[1], reverse=True)
        hotel_sorted_by_recommendation = list(map(lambda t: t[0], recommendations_for_user))
        user_ratings.sort(key=lambda t: t[1], reverse=True)
        hotel_sorted_by_ratings = list(map(lambda t: t[0], user_ratings))

        infinity_norms[len(hotel_indices)] \
            .append(infinity_norm_for_indices_difference(hotel_sorted_by_ratings, hotel_sorted_by_recommendation))
        sum_squared_errors[len(hotel_indices)] \
            .append(sum_squared_error(hotel_sorted_by_ratings, hotel_sorted_by_recommendation))
        kendall_tau_distances[len(hotel_indices)] \
            .append(kendall_tau_distance(hotel_sorted_by_ratings, hotel_sorted_by_recommendation))

        dcg = discounted_cumulative_gain(hotel_sorted_by_recommendation, user_id, utility_matrix)
        discounted_cumulative_gains[len(hotel_indices)].append(dcg)
        max_dcg = discounted_cumulative_gain(hotel_sorted_by_ratings, user_id, utility_matrix)
        max_discounted_cumulative_gains[len(hotel_indices)].append(max_dcg)
        normalized_discounted_cumulative_gains[len(hotel_indices)] \
            .append(dcg / max_dcg)

        reversed_hotels = hotel_sorted_by_ratings.copy()
        reversed_hotels.reverse()
        min_dcg = discounted_cumulative_gain(reversed_hotels, user_id, utility_matrix)
        min_normalized_discounted_cumulative_gains[len(hotel_indices)] \
            .append(min_dcg / max_dcg)

    infinity_norms = calc_mean_per_list_size(infinity_norms)
    print("infinity_norms\n", infinity_norms)

    sum_squared_errors = calc_mean_per_list_size(sum_squared_errors)
    print("sum_squared_errors\n", sum_squared_errors)

    kendall_tau_distances = calc_mean_per_list_size(kendall_tau_distances)
    print("kendall_tau_distances\n", kendall_tau_distances)

    discounted_cumulative_gains = calc_mean_per_list_size(discounted_cumulative_gains)
    print("discounted_cumulative_gains\n", discounted_cumulative_gains)

    max_discounted_cumulative_gains = calc_mean_per_list_size(max_discounted_cumulative_gains)
    print("max_discounted_cumulative_gains\n", max_discounted_cumulative_gains)

    normalized_discounted_cumulative_gains = calc_mean_per_list_size(normalized_discounted_cumulative_gains)
    print("normalized_discounted_cumulative_gains\n", normalized_discounted_cumulative_gains)

    min_normalized_discounted_cumulative_gains = calc_mean_per_list_size(min_normalized_discounted_cumulative_gains)
    print("min_normalized_discounted_cumulative_gains\n", min_normalized_discounted_cumulative_gains)


def test(delete_ratio=0.2):
    start = time.time()
    hotel_matrix = create_hotel_matrix()
    user_matrix = prepare_user_matrix(delete_ratio)
    similarities = cosine(user_matrix, hotel_matrix)
    end = time.time()
    print(f"Time: {end - start}")

    utility_matrix = load_npz("matrices/utility_matrix.npz")
    file = shelve.open(f"matrices/deleted_ratings_{delete_ratio}.bin")
    deleted_ratings = file["deleted_ratings"]
    calc_ranking_quality_measures(similarities, deleted_ratings, utility_matrix)


if __name__ == "__main__":
    test(0.2)
