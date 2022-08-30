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
    return [category.strip() for category in parsed_categories]


def truncate(x):
    return x[1:] if x.startswith("u'") else x


def parse_attributes(attributes):
    if attributes is None:
        return None

    embedded_attrs = ["music", "businessParking", "goodForMeal", "bestNights", "ambience"]
    null_boolean_vals = ["True", "False", "None"]

    parsed_attributes = {}
    for (attr_key, attr_val) in attributes.items():
        if not attr_key.startswith("BYOB"):
            attr_key = attr_key[0].lower() + attr_key[1:]
        attr_val = attr_val.replace("u'", "'")

        if attr_key in embedded_attrs:
            attr_val = attr_val.replace("'", "\"")
            for val in null_boolean_vals:
                attr_val = attr_val.replace(val, f"\"{val}\"")

        parsed_attributes[attr_key] = attr_val
    return parsed_attributes


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
                case "attributes":
                    parsed_hotel["attributes"] = parse_attributes(hotel["attributes"])
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
