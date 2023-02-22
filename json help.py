import json
with open('Questions.json','r') as read_file:
    data=json.load(read_file)
    print(data['questions'][0]['id'])