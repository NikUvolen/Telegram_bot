# -*- coding: utf-8 -*-

import os
import json
import time


# функция, которая записывает данные пользователей
def write_json(person_dict, user_id):
    data = [*person_dict]
    with open('cache/{}.json'.format(user_id), 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


# функция, которая загружает базу данных вопросов в массив
def load_quests_json():
    with open(os.path.join('question', 'questions_rus.json'), 'r', encoding='utf-8') as quest:
        quest_sets = json.load(quest)
    quest_list = []

    for item in quest_sets:
        question = item["Question"]
        a = item["a"]
        b = item["b"]
        c = item["c"]
        d = item["d"]
        answer = item["answer"]
        quest_list.append((question, a, b, c, d, answer))


# функция вывода счёта пользователя
def account_counting(user_id):
    try:
        with open('cache/{}.json'.format(user_id)) as ds:
            data_store = json.load(ds)
    # Если файл JSON повреждён или не найден, то всё начнётся сначала
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data_store = []
    return data_store



