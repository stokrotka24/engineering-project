import numpy as np
from scipy.sparse import load_npz
from similarities import cosine_similarity


def cosine_item_based(user_id, m, weighted_average=True):
    utility_matrix = load_npz("matrices/utility_matrix.npz")
    hotel_similarities = cosine_similarity(utility_matrix, 0)
    num_hotels = utility_matrix.shape[1]

    hotel_is_rated = {hotel_id: False for hotel_id in range(num_hotels)}

    user_ratings = utility_matrix.getrow(user_id)
    rated_hotels = user_ratings.indices
    user_ratings.todok()
    for hotel_id in rated_hotels:
        hotel_is_rated[hotel_id] = True

    c = 0
    for (hotel_id, is_rated) in hotel_is_rated.items():
        if not is_rated:
            hotel_similarities_row = hotel_similarities.getrow(hotel_id)
            # don't remove hotel_id because it will be removed during intersection
            similar_hotels = hotel_similarities_row.indices
            hotel_similarities_row.todok()

            rated_similar_hotels = np.intersect1d(rated_hotels, similar_hotels)
            # rated_similar_hotels = list(rated_similar_hotels)
            # rated_similar_hotels.remove(hotel_id)
            # rated_similar_hotels = np.array(rated_similar_hotels)
            num_rated_similar_hotels = len(rated_similar_hotels)
            if num_rated_similar_hotels > 0:
                c = c + 1
                hotel_similarity = [(h_id, hotel_similarities_row[0, h_id]) for h_id in rated_similar_hotels]
                hotel_similarity = sorted(
                    hotel_similarity,
                    key=lambda item: item[1],
                    reverse=True
                )
                hotel_similarity = hotel_similarity[:m]
                if weighted_average:
                    ratings_sum = sum([user_ratings[0, h_id] * similarity for (h_id, similarity) in hotel_similarity])
                    weights_sum = sum(similarity for (_, similarity) in hotel_similarity)
                else:
                    ratings_sum = sum([user_ratings[0, h_id] for (h_id, _) in hotel_similarity])
                    weights_sum = num_rated_similar_hotels
                print(ratings_sum / weights_sum)
    print(c)


cosine_item_based(372, 1000, True)
