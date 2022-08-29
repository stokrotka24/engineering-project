import json
import subprocess

with open("../data/hotels/parsed_data.json") as file:
    hotels = json.load(file)

command = "from hotels.models import Hotel, Attributes, WiFi;"

for h in hotels:
    command += f"h = Hotel(" \
               f"name=\"{h['name']}\"); h.save();"
    break

process = f"echo \'{command}\' | python ../manage.py shell"
print(process)
subprocess.call(process, shell=True)
