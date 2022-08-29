import json


def select_hotels(businesses):
    hotels = []

    for business in businesses:
        parsed_business = json.loads(business)
        if parsed_business["categories"] is not None:
            categories = parsed_business["categories"].split(",")
            categories = [cat.strip() for cat in categories]
            if "Hotels" in categories:
                hotels.append(parsed_business)

    return hotels


def parse_categories(categories):
    parsed_categories = categories.split(",")
    return [{"name": category.strip()} for category in parsed_categories]


# def parse_attributes(attributes):
#     if attributes is None:
#         return None
#
#     attributes_keys = \
#         ["BusinessAcceptsCreditCards", "WiFi", "RestaurantsPriceRange2", "ByAppointmentOnly",
#          "RestaurantsDelivery", "RestaurantsGoodForGroups", "GoodForKids", "OutdoorSeating",
#          "RestaurantsReservations", "HasTV", "RestaurantsTakeOut", "NoiseLevel", "RestaurantsAttire",
#          "BusinessAcceptsBitcoin", "Music", "BusinessParking", "GoodForMeal", "BYOBCorkage",
#          "Smoking", "BYOB", "RestaurantsTableService", "Caters", "Alcohol", "DogsAllowed",
#          "WheelchairAccessible", "HappyHour", "GoodForDancing", "BestNights", "Ambience", "CoatCheck",
#          "BikeParking", "Corkage", "DriveThru", "Open24Hours", "AcceptsInsurance", "RestaurantsCounterService"]
#
#     null_boolean_map = {"True": True, "False": False, "None": None, None: None}
#     wifi_map = {"'no'": "WiFiValue.no", "'paid'": "WiFiValue.paid",
#                 "u'paid'": "WiFiValue.paid", "u'free'": "WiFiValue.free",
#                 "u'no'": "WiFiValue.no", "'free'": "WiFiValue.free"}
#
#     parsed_attributes = {}
#     for attr_key in attributes_keys:
#         match attr_key:
#             case "WiFi":
#                 parsed_attributes["wiFi"] = wifi_map[attributes["WiFi"]]
#                 print(parsed_attributes)
#                 sys.exit()
#             case other:
#                 parsed_attributes[other[0].lower() + other[1:]] = null_boolean_map[attributes[other]]
#
#     return parsed_attributes


def parse_hotel_properties(hotels):
    parsed_hotels = []

    for hotel in hotels:
        parsed_hotel = {}
        for hotel_property in hotel:
            match hotel_property:
                case "business_id":
                    parsed_hotel["id"] = hotel["business_id"]
                case "is_open" | "hours":
                    pass
                case "categories":
                    parsed_hotel["categories"] = parse_categories(hotel["categories"])
                case other:
                    parsed_hotel[other] = hotel[other]
        parsed_hotels.append(parsed_hotel)

    return parsed_hotels


def parse_hotels():
    with open("../yelp_dataset/yelp_academic_dataset_business.json") as file:
        businesses = file.readlines()
    print("No. businesses:", len(businesses))

    hotels = select_hotels(businesses)
    print("No.hotels:", len(hotels))

    hotels = parse_hotel_properties(hotels)
    with open("parsed_data.json", "w") as file:
        json.dump(hotels, file, indent=4)


if __name__ == "__main__":
    parse_hotels()
