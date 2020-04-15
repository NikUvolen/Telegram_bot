# -*- coding: utf-8 -*-
import time
import json
from telebot import types
from core_file import bot
from core_file import smiles


# # Функция вывода клавиатуры.
# # -! Передавать столько сообщений, сколько Вы хотите клавиш
def keyboard(*args):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    for num in args:
        btn = types.KeyboardButton(num)
        markup.add(btn)

    return markup
# # =-=-==--=-=-==-=-=-==-==-=-==-==-=-==-=-=-=-


list_answers = []


def list_answers_save(message):
    msg = message.text
    list_answers.append(msg)
    return msg


# def write_json(person_dict, user_id):
#     data = [*person_dict]
#     with open('cache/{}.json'.format(user_id), 'w', encoding='utf-8') as file:
#         json.dump(data, file, indent=2, ensure_ascii=False)

def save_result(save_list, message):
    data = {
        'Chat_id': message.chat.id,
        'User_name': message.from_user.username,
        'First_and_last_name': [message.from_user.first_name, message.from_user.last_name],
        'Answers': save_list
    }
    with open('cache/{}.json'.format(data['Chat_id']), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def q1(chat_id):
    # очистка массива с ответами, если пользователь прописал ещё раз /quiz
    list_answers.clear()

    quest = bot.send_message(chat_id=chat_id,
                             text=' == Ты хочешь стать лицеистом?',
                             reply_markup=keyboard('Да!', 'Нет.', 'Не знаю('))
    bot.register_next_step_handler(quest, q2)


@bot.message_handler()
def q2(message):
    msg = list_answers_save(message)
    time.sleep(0.5)

    if msg == 'Да!':
        bot.send_message(chat_id=message.chat.id,
                         text=' == О, вот это по-нашему! ' + smiles['joy'])
    elif msg == 'Нет.':
        bot.send_message(chat_id=message.chat.id,
                         text=' == ' + smiles['sadness'])
    elif msg == 'Не знаю(':
        bot.send_message(chat_id=message.chat.id,
                         text=' == Пройди тест, может ты примешь решение ' + smiles['joy'])
    else:
        bot.send_message(chat_id=message.chat.id,
                         text=' == Вот как! ' + smiles['robot'])

    time.sleep(0.5)

    quest = bot.send_message(chat_id=message.chat.id,
                             text=' == В каком ты классе?',
                             reply_markup=keyboard('1-5', '6-9', '10-11'))

    bot.register_next_step_handler(quest, q3)


@bot.message_handler()
def q3(message):
    msg = list_answers_save(message)
    time.sleep(0.5)

    if msg == '1-5':
        bot.send_message(chat_id=message.chat.id,
                         text=' == Эх, тебе ещё рано идти к нам ' + smiles['sadness']
                              + ', НО мы ждём тебя! ' + smiles['joy'])
    elif msg == '6-9':
        bot.send_message(chat_id=message.chat.id,
                         text=' == О, тебе самое время к нам! Идём!' + smiles['joy'])
    elif msg == '10-11':
        bot.send_message(chat_id=message.chat.id,
                         text=' == Эй, пс! Хочешь буста для ЕГЭ? Окей, пошли к нам!')
    elif int(msg) < 1 or int(msg) > 11:
        bot.send_message(chat_id=message.chat.id,
                         text=' == Не знал, что такой существует ' + smiles['doubt'] + '. Ладно...')

    time.sleep(0.5)

    quest = bot.send_message(chat_id=message.chat.id,
                             text=' == Любишь вкусно поесть?)',
                             reply_markup=keyboard('Да, конечно!', 'Не-а', 'Не знаю...'))

    bot.register_next_step_handler(quest, q4)


@bot.message_handler()
def q4(message):
    msg = list_answers_save(message)
    time.sleep(0.5)

    if msg == 'Да, конечно!':
        bot.send_message(chat_id=message.chat.id,
                         text=' == Тогда тебе точно у нас понравится! В нашей столовой очень вкусно ' + smiles['joy'])
    elif msg == 'Не-а':
        bot.send_message(chat_id=message.chat.id,
                         text=' == Не верю!')

    time.sleep(0.5)

    quest = bot.send_message(chat_id=message.chat.id,
                             text=' == Напиши любимую фразу!')

    bot.register_next_step_handler(quest, q5)


@bot.message_handler()
def q5(message):
    msg = list_answers_save(message)
    time.sleep(0.5)

    quest = bot.send_message(chat_id=message.chat.id,
                             text=' == Сколько. Ты. Зарабатываешь. Оценок?',
                             reply_markup=keyboard('Много', 'Очень много!', 'Я уже сам сбился со счёту'))

    bot.register_next_step_handler(quest, q6)


@bot.message_handler()
def q6(message):
    msg = list_answers_save(message)
    time.sleep(0.5)

    if msg == 'Много':
        bot.send_message(chat_id=message.chat.id,
                         text='😎')
    elif msg == 'Очень много!':
        bot.send_message(chat_id=message.chat.id,
                         text='Да ты крут 😎')
    elif msg == 'Я уже сам сбился со счёту':
        bot.send_message(chat_id=message.chat.id,
                         text='Ого, это как так? 😎')

    time.sleep(0.5)

    quest = bot.send_message(chat_id=message.chat.id,
                             text=' == Какое-нибудь число (1-10)?')

    bot.register_next_step_handler(quest, end)


@bot.message_handler()
def end(message):
    msg = list_answers_save(message)

    bot.send_message(chat_id=message.from_user.id,
                     text=' == {}, спасибо за прохождение теста! '.format(message.from_user.first_name) + smiles['joy'])

    time.sleep(0.5)

    bot.send_message(chat_id=message.from_user.id,
                     text=' == Я думаю, что ты бы стал достойным лицеистом 😎')

    time.sleep(0.5)

    bot.send_message(chat_id=message.from_user.id,
                     text=' == Чтобы вернуться в меню, нажми на /menu',
                     reply_markup=keyboard('/menu'))

    save_result(list_answers, message)


bot.polling()
