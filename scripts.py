import json
import pandas as pd
import yaml
import random as rnd

def add_user(users:dict, user_fullname: str):
    list_row = [len(users), user_fullname, 0, False, True]
    users.loc[len(users)] = list_row

def save_users(users:pd.DataFrame):
    users.to_csv('users.csv', sep=';', index=False)

def save_secrets(secrets:dict):
    with open("secrets.yaml", "w") as stream:
        yaml.dump(secrets, stream, default_flow_style=False)

def check_user(secrets:dict, id:str):
    return id in secrets['secrets']['chat_ids']

def get_leaders(users:pd.DataFrame):
    users.sort_values(["rating"], 
                    axis=0,
                    ascending=[False], 
                    inplace=True)
    top = 10 if len(users) > 10 else len(users)
    return users.head(top)

def get_mailng_list(secrets:dict, users:pd.DataFrame):
    mailng_list = []
    for chat_id in secrets['secrets']['chat_ids']:
        user_id = get_user_by_chatid(secrets, chat_id)
        if users.iloc[user_id]['is_mailing']:
            mailng_list.append(chat_id)
    return mailng_list

def get_random_question(question_data:dict):
    return rnd.choice(question_data['questions'])

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
    return users.iloc[user_id]['is_mailing']

def update_user_mailng(users:pd.DataFrame, secrets:dict, chat_id:str, value:bool):
    user_id = get_user_by_chatid(secrets, chat_id)
    users.at[user_id, 'is_mailing'] = value
            
def update_user_score(users:pd.DataFrame, secrets:dict, chat_id:str):
    user_id = get_user_by_chatid(secrets, chat_id)
    users.at[user_id, 'rating'] += 1

def read_users():
    df = pd.read_csv('users.csv', sep=';')
    return df

def read_questions():
    with open('Questions_Data.json', 'r', encoding='utf-8') as questions_file:
        return json.loads(questions_file.read())