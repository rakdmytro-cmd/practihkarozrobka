import json

def encode(data):
    return (json.dumps(data) + "\n").encode()

def decode(data):
    return json.loads(data)