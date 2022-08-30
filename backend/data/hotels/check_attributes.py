import json
from collections import defaultdict

with open('parsed_data.json') as file:
    hotels = json.load(file)

attributes = defaultdict(set)
hotels_without_attrs = 0

for hotel in hotels:
    if hotel["attributes"] is not None:
        hotel_attributes = hotel["attributes"]
        for (attr_key, attr_val) in hotel_attributes.items():
            attributes[attr_key].add(attr_val)
    else:
        hotels_without_attrs += 1

print("No. hotels without any attributes:", hotels_without_attrs)
# No. hotels without any attributes: 186

with open("attributes_keys.txt", "w") as file:
    for attr_key in attributes.keys():
        file.write(f"\"{attr_key}\", ")

with open("attributes.txt", "w") as file:
    for attr in attributes.items():
        file.write(str(attr) + '\n')
