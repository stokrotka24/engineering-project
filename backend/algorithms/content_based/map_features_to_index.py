import os
import sys
from pathlib import Path

import django
from django.db.models import NullBooleanField
from enumchoicefield.fields import EnumChoiceField
from djongo.models import EmbeddedField

sys.path.append(Path(__file__).parent.parent.parent.__str__())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()
from hotels.models import WiFi, NoiseLevel, RestaurantsAttire, BYOBCorkage, Smoking, Alcohol, Attributes, Music, \
    Parking, GoodForMeal, BestNights, Ambience, Hotel

map_feature_to_index = dict()
current_column_index = 0

enum_name_to_class = {"wiFi": WiFi, "noiseLevel": NoiseLevel, "restaurantsAttire": RestaurantsAttire,
                      "BYOBCorkage": BYOBCorkage, "smoking": Smoking, "alcohol": Alcohol}
embedded_attr_name_to_class = {"music": Music, "businessParking": Parking, "goodForMeal": GoodForMeal,
                               "bestNights": BestNights, "ambience": Ambience}


def map_categories_to_index():
    global current_column_index

    hotels = Hotel.objects.all()
    categories = set()
    for hotel in hotels:
        for category in hotel.categories:
            categories.add(category['name'])

    for category in categories:
        map_feature_to_index[category] = current_column_index
        current_column_index += 1


def get_embedded_keys(embedded_class):
    return [
        key
        for key in vars(embedded_class).keys()
        if not key.startswith('_') and key != "Meta"
    ]


def add_enum_choices(enum_name):
    global current_column_index
    map_feature_to_index[enum_name] = dict()
    enum_class = enum_name_to_class[enum_name]
    enum_keys = get_embedded_keys(enum_class)

    for enum_key in enum_keys:
        map_feature_to_index[enum_name][enum_key] = current_column_index
        current_column_index += 1


def add_embedded_attr(embedded_attr_name):
    global current_column_index
    map_feature_to_index[embedded_attr_name] = dict()
    embedded_class = embedded_attr_name_to_class[embedded_attr_name]
    embedded_keys = get_embedded_keys(embedded_class)

    for embedded_key in embedded_keys:
        map_feature_to_index[embedded_attr_name][embedded_key] = current_column_index
        current_column_index += 1


def map_attributes_to_index():
    global current_column_index
    attributes_fields = Attributes._meta.fields

    for attr_field in attributes_fields:
        if isinstance(attr_field, NullBooleanField):
            map_feature_to_index[attr_field.attname] = current_column_index
            current_column_index += 1
        elif isinstance(attr_field, EmbeddedField):
            add_embedded_attr(attr_field.attname)
        elif isinstance(attr_field, EnumChoiceField):
            add_enum_choices(attr_field.attname)
        else:
            print("Unsupported type:", type(attr_field))


def create_map_feature_to_index():
    map_categories_to_index()
    map_attributes_to_index()
    return map_feature_to_index, current_column_index


if __name__ == "__main__":
    create_map_feature_to_index()
    print(map_feature_to_index)
