import json
from pathlib import Path

from data.hotels.generate_insert_commands import add_property
from data.reviews.generate_insert_commands import get_hotels_reviews_from_dataset
from data.users.parse import parse_users

users_file = "data/users/users.txt"


def get_users_with_hotels_reviews_from_dataset():
    users_ids_with_hotels_reviews_file = "data/users/users_ids.txt"
    users_ids_with_hotels_reviews_path = Path(users_ids_with_hotels_reviews_file)

    if not users_ids_with_hotels_reviews_path.is_file():
        hotels_reviews_file = "data/reviews/hotels_reviews.txt"
        hotels_reviews_path = Path(hotels_reviews_file)
        if not hotels_reviews_path.is_file():
            get_hotels_reviews_from_dataset()
        with open(hotels_reviews_file) as f:
            reviews = f.readlines()
        reviews = [json.loads(review) for review in reviews]
        f = open(users_ids_with_hotels_reviews_file, "w")
        for review in reviews:
            f.write(review["user_id"] + "\n")
        f.close()

    with open(users_ids_with_hotels_reviews_file) as f:
        users_ids = f.read().splitlines()

    user_id_occurred = {}
    for user_id in users_ids:
        user_id_occurred[user_id] = True

    with open("data/yelp_dataset/yelp_academic_dataset_user.json") as file:
        users = file.readlines()
    print("Users read")

    no_users = 0
    max_name_len = 0
    f = open(users_file, "w")
    for (index, user) in enumerate(users):
        u = json.loads(user)
        if index % 10000 == 0:
            print("Preprocessed ", index, "users")

        if user_id_occurred.get(u["user_id"], False):
            f.write(user)
            no_users += 1
            name_len = len(u["name"])
            if name_len > max_name_len:
                max_name_len = name_len
    f.close()
    print("No. users:", len(users))
    print("No. users with hotels reviews:", no_users)
    print("Max length of username: ", max_name_len)


def add_users():
    users_path = Path(users_file)
    if not users_path.is_file():
        get_users_with_hotels_reviews_from_dataset()

    with open(users_file) as f:
        users = f.readlines()
    print("No. users with hotels reviews:", len(users))
    users = [json.loads(user) for user in users]

    users = parse_users(users)

    properties = ["username", "email", "password", "id", "review_count",
                  "date_joined", "useful_votes", "funny_votes", "cool_votes",
                  "fans", "elite", "average_stars", "compliment_hot",
                  "compliment_more", "compliment_profile", "compliment_cute",
                  "compliment_list", "compliment_note", "compliment_plain", "compliment_cool",
                  "compliment_funny", "compliment_writer", "compliment_photos"]

    commands = ["from authorization.models import User;"]

    for u in users:
        commands.append("u = User.objects.create_user(")
        for prop in properties:
            add_property(commands, prop, u[prop])
        commands.append(");")

    command = "".join(commands)
    with open("data/users/insert_commands.txt", "w") as f:
        f.write(command)


if __name__ == '__main__':
    add_users()
