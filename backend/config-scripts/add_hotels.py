import json


def add_property(commands, prop_name, prop):
    commands.append(f"{prop_name}=\"{prop}\",")


def add_categories(commands, categories):
    commands.append("categories=[")
    for category in categories:
        commands.append(f"{{\"name\": \"{category}\"}},")
    commands.append("],")


def add_embedded_attributes(commands, attr_name, attrs, attrs_keys):
    if not attrs or attrs == "\"None\"":
        attrs = {}
    else:
        attrs = json.loads(attrs)
    commands.append(f"\"{attr_name}\": {{")
    for attr_key in attrs_keys:
        commands.append(f"\"{attr_key}\": {attrs.get(attr_key)},")
    commands.append("},")


def add_attributes(commands, attributes):
    if not attributes:
        return

    commands.append("attributes={")

    attributes_keys = ["businessAcceptsCreditCards", "wiFi", "restaurantsPriceRange2", "byAppointmentOnly",
                       "restaurantsDelivery", "restaurantsGoodForGroups", "goodForKids", "outdoorSeating",
                       "restaurantsReservations", "hasTV", "restaurantsTakeOut", "noiseLevel", "restaurantsAttire",
                       "businessAcceptsBitcoin", "music", "businessParking", "goodForMeal", "BYOBCorkage", "smoking",
                       "BYOB", "restaurantsTableService", "caters", "alcohol", "dogsAllowed", "wheelchairAccessible",
                       "happyHour", "goodForDancing", "bestNights", "ambience", "coatCheck", "bikeParking", "corkage",
                       "driveThru", "open24Hours", "acceptsInsurance", "restaurantsCounterService", ]

    wifi_map = {"'no'": "WiFi.no", "'paid'": "WiFi.paid", "'free'": "WiFi.free", None: None}
    noise_map = {"'quiet'": "NoiseLevel.quiet", "'average'": "NoiseLevel.average",
                 "'loud'": "NoiseLevel.loud", "'very_loud'": "NoiseLevel.very_loud",
                 "None": None, None: None}
    restaurants_attire_map = {"'dressy'": "RestaurantsAttire.dressy", "'casual'": "RestaurantsAttire.casual",
                              "'formal'": "RestaurantsAttire.formal", None: None}
    byob_corkage = {"'no'": "BYOBCorkage.no", "'yes_corkage'": "BYOBCorkage.yes_corkage",
                    "'yes_free'": "BYOBCorkage.yes_free", None: None}
    smoking = {"'outdoor'": "Smoking.outdoor", "'yes'": "Smoking.yes", "'no'": "Smoking.no", None: None}
    alcohol = {"'full_bar'": "Alcohol.full_bar", "'beer_and_wine'": "Alcohol.beer_and_wine",
               "'none'": "Alcohol.none", None: None}
    attr_to_map = {"wiFi": wifi_map, "noiseLevel": noise_map, "restaurantsAttire": restaurants_attire_map,
                   "BYOBCorkage": byob_corkage, "smoking": smoking, "alcohol": alcohol, None: None}

    music = ["dj", "background_music", "no_music", "jukebox", "live", "video", "karaoke"]
    parking = ["garage", "street", "validated", "lot", "valet"]
    good_meal = ["dessert", "latenight", "lunch", "dinner", "brunch", "breakfast"]
    best_nights = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    ambience = ["touristy", "hipster", "romantic",  "divey", "intimate", "trendy", "upscale", "classy", "casual"]
    embedded_attrs_keys_map = {"music": music, "businessParking": parking, "goodForMeal": good_meal,
                               "bestNights": best_nights, "ambience": ambience}

    for attr_key in attributes_keys:
        match attr_key:
            case "music" | "businessParking" | "goodForMeal" | "bestNights" | "ambience":
                add_embedded_attributes(commands, attr_key, attributes.get(attr_key), embedded_attrs_keys_map[attr_key])
            case _:
                attr_val = attributes.get(attr_key)
                attr_map = attr_to_map.get(attr_key)

                if attr_map:
                    commands.append(f"\"{attr_key}\": {attr_map[attr_val]},")
                else:
                    commands.append(f"\"{attr_key}\": {attr_val},")

    commands.append("}")


def add_hotels():
    with open("../data/hotels/parsed_data.json") as file:
        hotels = json.load(file)

    properties = ["id", "name", "address", "city",
                  "state", "postal_code", "latitude",
                  "longitude", "review_count"]

    commands = ["from hotels.models import Hotel, WiFi, NoiseLevel, RestaurantsAttire, BYOBCorkage, Smoking, Alcohol;"]

    for h in hotels:
        print(h)
        commands.append("h = Hotel(")
        for prop in properties:
            add_property(commands, prop, h[prop])
        add_property(commands, "stars", int(h["stars"]))
        add_categories(commands, h["categories"])
        add_attributes(commands, h["attributes"])
        commands.append("); h.save();")

    command = "".join(commands)
    with open("g.py", "w") as f:
        f.write(command)


if __name__ == '__main__':
    add_hotels()
