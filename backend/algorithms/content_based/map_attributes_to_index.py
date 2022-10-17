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
    Parking, GoodForMeal, BestNights, Ambience

map_attribute_to_index = dict()
curr_col_index = 0

enum_name_to_class = {"wiFi": WiFi, "noiseLevel": NoiseLevel, "restaurantsAttire": RestaurantsAttire,
                      "BYOBCorkage": BYOBCorkage, "smoking": Smoking, "alcohol": Alcohol}
embedded_attr_name_to_class = {"music": Music, "businessParking": Parking, "goodForMeal": GoodForMeal,
                               "bestNights": BestNights, "ambience": Ambience}
boolean_values = [True, False]


def add_null_boolean_field(field_name):
    global curr_col_index

    map_attribute_to_index[field_name] = dict()
    for val in boolean_values:
        map_attribute_to_index[field_name][val] = curr_col_index
        curr_col_index += 1


def get_embedded_keys(embedded_class):
    return [
        key
        for key in vars(embedded_class).keys()
        if not key.startswith('_') and key != "Meta"
    ]


def add_enum_choices(enum_name):
    global curr_col_index
    map_attribute_to_index[enum_name] = dict()
    enum_class = enum_name_to_class[enum_name]
    enum_keys = get_embedded_keys(enum_class)

    for enum_key in enum_keys:
        map_attribute_to_index[enum_name][enum_key] = curr_col_index
        curr_col_index += 1

    curr_col_index += 1


def add_embedded_attr(embedded_attr_name):
    global curr_col_index
    map_attribute_to_index[embedded_attr_name] = dict()
    embedded_class = embedded_attr_name_to_class[embedded_attr_name]
    embedded_keys = get_embedded_keys(embedded_class)

    for embedded_key in embedded_keys:
        map_attribute_to_index[embedded_attr_name][embedded_key] = dict()
        for val in boolean_values:
            map_attribute_to_index[embedded_attr_name][embedded_key][val] = curr_col_index
            curr_col_index += 1


def create_map_attributes_to_index():
    attributes_fields = Attributes._meta.fields

    for attr_field in attributes_fields:
        if isinstance(attr_field, NullBooleanField):
            add_null_boolean_field(attr_field.attname)
        elif isinstance(attr_field, EmbeddedField):
            add_embedded_attr(attr_field.attname)
        elif isinstance(attr_field, EnumChoiceField):
            add_enum_choices(attr_field.attname)
        else:
            print("Unsupported type:", type(attr_field))

    return map_attribute_to_index, curr_col_index


if __name__ == "__main__":
    create_map_attributes_to_index()
    print(map_attribute_to_index)
