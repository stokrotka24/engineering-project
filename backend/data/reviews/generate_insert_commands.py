import json
import shelve
from pathlib import Path

from data.hotels.generate_insert_commands import get_hotels_from_dataset, add_property
from data.reviews.parse import parse_reviews


hotel_reviews_file = "data/reviews/hotels_reviews.txt"


def get_hotels_reviews_from_dataset():
    hotel_ids_file = "data/hotels/hotels_ids.txt"
    hotels_ids_path = Path(hotel_ids_file)
    if not hotels_ids_path.is_file():
        get_hotels_from_dataset(True)

    with open(hotel_ids_file) as f:
        hotels_ids = f.read().splitlines()

    print(hotels_ids)

    with open('data/yelp_dataset/yelp_academic_dataset_review.json') as f:
        reviews = f.readlines()
    print("Reviews read")

    no_hotels_reviews = 0
    max_hotel_review_len = 0
    f = open(hotel_reviews_file, "w")
    for (index, review) in enumerate(reviews):
        r = json.loads(review)
        if index % 10000 == 0:
            print(index)

        if r["business_id"] in hotels_ids:
            f.write(review)
            no_hotels_reviews += 1
            review_len = len(r["text"])
            if review_len > max_hotel_review_len:
                max_hotel_review_len = review_len

    f.close()
    print("No. reviews:", len(reviews))
    print("No. hotel reviews:", no_hotels_reviews)
    print("Max hotel review length:", max_hotel_review_len)


def add_reviews():
    hotel_reviews_path = Path(hotel_reviews_file)
    if not hotel_reviews_path.is_file():
        get_hotels_reviews_from_dataset()

    with open(hotel_reviews_file) as f:
        reviews = f.readlines()
    print("No. hotel reviews:", len(reviews))
    reviews = [json.loads(review) for review in reviews[:1000]]

    reviews = parse_reviews(reviews)

    properties = ["date", "content"]

    commands = ["from hotels.models import Review;"]

    with shelve.open('data/users/ids_map') as f:
        user_ids_map = f['ids_map']

    with shelve.open('data/hotels/ids_map') as f:
        hotel_ids_map = f['ids_map']

    for r in reviews:
        commands.append("r = Review(")
        for prop in properties:
            add_property(commands, prop, r[prop])
        add_property(commands, "user_id", user_ids_map.get(r["user_id"], 1))
        add_property(commands, "hotel_id", hotel_ids_map.get(r["hotel_id"], 1))
        add_property(commands, "stars", int(r["stars"]))
        commands.append("); r.save();")

    command = "".join(commands)
    with open("data/reviews/insert_commands.txt", "w") as f:
        f.write(command)


if __name__ == '__main__':
    add_reviews()
