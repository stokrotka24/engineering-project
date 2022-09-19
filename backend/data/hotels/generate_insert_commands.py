import json
import shelve

from data.hotels.parse import parse_hotels


def get_hotels_from_dataset(save_hotels_ids=False):
    with open("data/yelp_dataset/yelp_academic_dataset_business.json") as file:
        businesses = file.readlines()
    print("No. businesses:", len(businesses))

    hotels = []

    for business in businesses:
        parsed_business = json.loads(business)
        if parsed_business["categories"] is not None:
            categories = parsed_business["categories"].split(",")
            categories = [cat.strip() for cat in categories]

            if "Hotels" in categories:
                hotels.append(parsed_business)

    if save_hotels_ids:
        f = open("data/hotels/hotels_ids.txt", "w")
        for hotel in hotels:
            f.write(hotel["business_id"] + "\n")
        f.close()

    return hotels


def add_property(commands, prop_name, prop):
    commands.append(f"{prop_name}=\"{prop}\",")


def add_categories(commands, categories):
    categories.remove("Hotels")

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
    byob_corkage_map = {"'no'": "BYOBCorkage.no", "'yes_corkage'": "BYOBCorkage.yes_corkage",
                        "'yes_free'": "BYOBCorkage.yes_free", None: None}
    smoking_map = {"'outdoor'": "Smoking.outdoor", "'yes'": "Smoking.yes", "'no'": "Smoking.no", None: None}
    alcohol_map = {"'full_bar'": "Alcohol.full_bar", "'beer_and_wine'": "Alcohol.beer_and_wine",
                   "'none'": "Alcohol.none", None: None}
    attr_to_map = {"wiFi": wifi_map, "noiseLevel": noise_map, "restaurantsAttire": restaurants_attire_map,
                   "BYOBCorkage": byob_corkage_map, "smoking": smoking_map, "alcohol": alcohol_map}

    music = ["dj", "background_music", "no_music", "jukebox", "live", "video", "karaoke"]
    parking = ["garage", "street", "validated", "lot", "valet"]
    good_meal = ["dessert", "latenight", "lunch", "dinner", "brunch", "breakfast"]
    best_nights = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    ambience = ["touristy", "hipster", "romantic", "divey", "intimate", "trendy", "upscale", "classy", "casual"]
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
                    attr_val = attr_map[attr_val]

                commands.append(f"\"{attr_key}\": {attr_val},")

    commands.append("}")


def add_hotels():
    hotels = get_hotels_from_dataset()
    print("No.hotels:", len(hotels))

    hotels = parse_hotels(hotels)

    properties = ["name", "address", "city",
                  "state", "postal_code", "latitude",
                  "longitude", "review_count"]

    commands = ["from hotels.models import Hotel, WiFi, NoiseLevel, RestaurantsAttire, BYOBCorkage, Smoking, Alcohol;"]

    ids_map = {}
    for (index, h) in enumerate(hotels):
        ids_map[h["id"]] = index + 1
        commands.append("h = Hotel(")
        for prop in properties:
            add_property(commands, prop, h[prop])
        add_property(commands, "stars", float(h["stars"]))
        add_categories(commands, h["categories"])
        add_attributes(commands, h["attributes"])
        commands.append("); h.save();")

    with shelve.open('data/hotels/ids_map') as f:
        f['ids_map'] = ids_map

    command = "".join(commands)
    with open("data/hotels/insert_commands.txt", "w") as f:
        f.write(command)


if __name__ == '__main__':
    add_hotels()
