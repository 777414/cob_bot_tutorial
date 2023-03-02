import csv
import pandas as pd
import yaml


    # id;user_name;rating;is_banned;is_mailing
# ls = list(map(lambda x: (x[1], x[3]), list(file_reader)[1:]))
# print(sorted(ls, key=lambda x: x[1]))
def add_user(list, val, chat_id):
    if val:
        with open('users.csv', 'a', newline='', encoding='utf-8') as csvfile:
            file_writer = csv.writer(csvfile, delimiter = ";", lineterminator="\n")
            file_writer.writerow(list)
        with open("secrets.yaml", "r") as stream:
            try:
                secrets = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
            secrets['secrets']['chat_ids'].append(chat_id)
        with open("secrets.yaml", "w") as stream:
            yaml.dump(secrets, stream, default_flow_style=False)
        return True
    else:
        return False


def check_user(secrets:dict, id:str):
    return id in secrets['secrets']['chat_ids']


def check_chat_id(chat_id):
    with open("secrets.yaml", "r") as stream:
        try:
            secrets = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    if chat_id in secrets['secrets']['chat_ids']:
        return False
    else:
        return True

def check_name_user(name):
    if name:
        return name
    else:
        return "None"


def read_secrets():
        with open("secrets.yaml", "r") as stream:
            try:
                secrets = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return secrets

def get_user_by_chatid(secrets:dict, chat_id:str):
    return secrets['secrets']['chat_ids'].index(chat_id)

def check_user_is_malling(users: pd.DataFrame, secrets:dict, chat_id:str):
    user_id = get_user_by_chatid(secrets, chat_id)
    return users[user_id]['is_mailing'] == 'True'
            
def read_users():
       df = pd.read_csv('users.csv', sep=';')
       return df

def save_users(users:pd.DataFrame):
    users.to_csv('users.csv', sep=';', index=False)

def save_secrets(secrets:dict):
    with open("secrets.yaml", "w") as stream:
        yaml.dump(secrets, stream, default_flow_style=False)

def check_is_malling(name_user):
        with open('users.csv', 'r', newline='', encoding='utf-8') as csvfile:
            file_reader = csv.reader(csvfile, delimiter=';', quotechar='|')
            ls = list(filter(lambda x: x[1] == name_user, file_reader))
        if ls[0][-1] == "False":
            return False
        else:
            return True
s = read_secrets()
s['secrets']['chat_ids'].append(111111)
print(s)
save_secrets(s)