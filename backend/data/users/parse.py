from datetime import datetime

import pytz


def parse_date(date_joined):
    return datetime.strptime(date_joined, "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.timezone('Europe/Warsaw'))


def parse_users(users):
    parsed_users = []

    for (index, user) in enumerate(users):
        parsed_user = {}

        for user_property in user:
            match user_property:
                case "user_id":
                    parsed_user["id"] = user["user_id"]
                case "name":
                    parsed_user["username"] = user["name"]
                case "yelping_since":
                    parsed_user["date_joined"] = parse_date(user["yelping_since"])
                case "useful" | "funny" | "cool":
                    parsed_user[user_property + "_votes"] = user[user_property]
                case "friends":
                    pass
                case other:
                    parsed_user[other] = user[other]

        parsed_user["email"] = f"test{index}@example.com"
        parsed_user["password"] = "test"
        parsed_users.append(parsed_user)

    return parsed_users
