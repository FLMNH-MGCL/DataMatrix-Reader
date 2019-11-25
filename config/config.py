import json
from pprint import pprint
import os

filename='./config.json'

with open(filename, 'r') as json_file:
    data = json.load(json_file)
    print(data['multipleOrientations']['state'])
    if data['multipleOrientations']['state'] is True:
        data['multipleOrientations']['state'] = False
    else:
        data['multipleOrientations']['state'] = True
    print(data['multipleOrientations']['state'])

os.remove(filename)
with open(filename, 'w') as new_file:
    json.dump(data, new_file, indent=4)


