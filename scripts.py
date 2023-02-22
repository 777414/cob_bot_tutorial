import csv
import telegram
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters
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


def chek_user(id):
    with open('users.csv', 'r', newline='', encoding='utf-8') as csvfile:
        file_reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        return list(file_reader)[id]


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


def get_TOKEN():
        with open("secrets.yaml", "r") as stream:
            try:
                secrets = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return secrets['secrets']['api_key']


def check_user_is_malling(name_user, val):
    if not val:
        with open('users.csv', 'r', newline='', encoding='utf-8') as csvfile:
            file_writer = csv.reader(csvfile, delimiter = ";", lineterminator="\n")
            spisok = list(file_writer)
            ls = list(filter(lambda x: x[1] == name_user, spisok))
            ls2 = list(filter(lambda x: x, spisok))
            ls2 = list(filter(lambda x: x != ls, *ls2))
            print(ls2, ls)
            ls = ls[0]
            ls = ls[:-1] + [False]
            
        # with open('users.csv', 'w', newline='', encoding='utf-8') as csvfile:
        #     file_writer = csv.writer(csvfile, delimiter = ";", lineterminator="\n")
        #     file_writer.writerow(ls + ls2)

            return True
    else:
        return False
            



def check_is_malling(name_user):
        with open('users.csv', 'r', newline='', encoding='utf-8') as csvfile:
            file_reader = csv.reader(csvfile, delimiter=';', quotechar='|')
            ls = list(filter(lambda x: x[1] == name_user, file_reader))
        if ls[0][-1] == "False":
            return False
        else:
            return True


check_user_is_malling("Никита", False)




