import json
import os

def read_json(path):
    if os.path.isfile(path):
        with open(path, encoding='utf-8') as f:
            data = json.loads(f.read())
    else:
        data = {}
    return data
