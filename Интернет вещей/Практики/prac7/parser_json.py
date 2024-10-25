import json

with open('data.json', 'r') as file:
    result = json.load(file)
print(result)
