import json


def read_json(filepath):
    with open(filepath, mode='r') as file:
        return json.load(file)


def write_json(obj, filepath):
    with open(filepath, mode='w') as file:
        json.dump(obj, file)
