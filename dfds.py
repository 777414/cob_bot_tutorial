import json
with open('Questions_Data.json', 'r') as read_file:
    data=json.load(read_file)
    print(data['questions'][0]['id'])