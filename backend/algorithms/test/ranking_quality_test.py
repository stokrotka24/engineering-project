import math
import shelve
import time
from collections import defaultdict
from scipy.sparse import load_npz, save_npz
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


def calc_ranking_quality_measures(recommendations, deleted_ratings, utility_matrix, file):
    deleted_ratings_map = defaultdict(list)
    for (user_id, hotel_id) in deleted_ratings:
        deleted_ratings_map[user_id].append(hotel_id)

    infinity_norms = defaultdict(list)
    sum_squared_errors = defaultdict(list)
    kendall_tau_distances = defaultdict(list)
    discounted_cumulative_gains = defaultdict(list)
    normalized_discounted_cumulative_gains = defaultdict(list)

    for (user_id, hotel_indices) in deleted_ratings_map.items():
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
        normalized_discounted_cumulative_gains[len(hotel_indices)] \
            .append(dcg / max_dcg)

    infinity_norms = calc_mean_per_list_size(infinity_norms)
    sum_squared_errors = calc_mean_per_list_size(sum_squared_errors)
    kendall_tau_distances = calc_mean_per_list_size(kendall_tau_distances)
    discounted_cumulative_gains = calc_mean_per_list_size(discounted_cumulative_gains)
    normalized_discounted_cumulative_gains = calc_mean_per_list_size(normalized_discounted_cumulative_gains)

    with open(file, "a") as f:
        f.write(f"{infinity_norms}\n")
        f.write(f"{sum_squared_errors}\n")
        f.write(f"{kendall_tau_distances}\n")
        f.write(f"{discounted_cumulative_gains}\n")
        f.write(f"{normalized_discounted_cumulative_gains}\n")


def content_based(delete_ratio=0.2):
    start = time.time()
    hotel_matrix = create_hotel_matrix()
    user_matrix = prepare_user_matrix(delete_ratio)
    similarities = cosine(user_matrix, hotel_matrix)
    elapsed_time = time.time() - start
    save_npz(f"matrices/similarities_{delete_ratio}.npz", similarities, True)
    return elapsed_time


def test_content_based_ranking(delete_ratio=0.2, deleted_ratings=None, ranking_file="results/content_based.txt"):
    utility_matrix = load_npz("matrices/utility_matrix.npz")
    if deleted_ratings is None:
        file = shelve.open(f"matrices/deleted_ratings_{delete_ratio}.bin")
        deleted_ratings = file["deleted_ratings"]
    similarities = load_npz(f"matrices/similarities_{delete_ratio}.npz")
    calc_ranking_quality_measures(similarities, deleted_ratings, utility_matrix, ranking_file)


def measure_content_based_average_time(no_tests=10):
    elapsed_time = 0
    for i in range(no_tests):
        elapsed_time += content_based()

    with open("results/cb_cf_time.txt", "a") as f:
        f.write(f"content_based: {elapsed_time / no_tests} s")


if __name__ == "__main__":
    measure_content_based_average_time()
    test_content_based_ranking()
