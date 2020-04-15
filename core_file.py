# -*- coding: utf-8 -*-

import time
import apiai
import json

# Импорт сторонних библиотек
import telebot
from telebot import apihelper, types

# Импорт функций из локальных директорий
from bot_config import config
import dbworker
import question.questions as quest
from bot_config.config import proxy


bot = telebot.TeleBot(config.TOKEN)
apihelper.proxy = {'https': proxy}
smiles = {'joy': '😄',
          'doubt': '😕',
          'robot': '🤖',
          'sadness': '🥺'}


def keyboard(*args):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    for num in args:
        btn = types.KeyboardButton(num)
        markup.add(btn)

    return markup


# функция reset возвращает user'а в начало
@bot.message_handler(commands=['reset'])
def cmd_reset(message):
    bot.send_message(chat_id=message.chat.id,
                     text=' == Что ж, нажми на /menu, чтобы открыть его  == ',
                     reply_markup=keyboard('/menu'))
    dbworker.set_state(message.chat.id, config.States.S_MENU.value)


# функция старта
@bot.message_handler(commands=['start'])
def start(message):
    # запись в переменную state стадию пользователя
    state = dbworker.get_current_state(message.from_user.id)

    if state == config.States.S_ENTER_QUIZ.value:
        bot.send_message(message.chat.id,
                         ' == Кажется, кто-то не закончил проходить викторину ' + smiles['doubt'] + ' == ')
    elif state == config.States.S_MENU.value:
        bot.send_message(message.chat.id,
                         ' == Эй, ты уже писал(а) это ' + smiles['joy'] + '. Выбери что-нибудь в меню == ')
    elif state == config.States.S_CHOICE.value:
        bot.send_message(message.chat.id,
                         ' == Твой выбор ждёт тебя ' + smiles['robot'] + '! ==')
    elif state == config.States.S_TALK.value:
        bot.send_message(message.chat.id,
                         ' == Ты уйдёшь не попрощавшись? ' + smiles['sadness'] + ' == ')
    else:
        bot.send_message(message.from_user.id, '	== Привет! Я Quiz V0.0.6 (beta-test) ' + smiles['joy'] + ' == ')
        # TODO: установить таймеры ответа
        time.sleep(0)

        # Приветствие ботом пользователя
        bot.send_message(message.from_user.id,
                         '	== Рад тебя видеть, {}! =='.format(message.from_user.first_name))
        time.sleep(0)

        bot.send_message(message.from_user.id, ' == Нажми на /menu, чтобы перейти в него == ')
        dbworker.set_state(message.from_user.id, config.States.S_MENU.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_MENU.value)
def menu(message):
    if message.text == '/menu':
        # Вывод админ меню
        if message.from_user.id == 531500833:
            bot.send_message(message.from_user.id, ' == Привет, Создатель! Вот тебе моё меню! == ',
                             reply_markup=keyboard('/quiz', '/reed', '/talk'))
            bot.send_message(message.from_user.id,
                             '''
[ /quiz ] - сыграть раунд в Quiz
[ /reed ] - посмотреть свой счёт
[ /talk ] - просто поговорить с ботом о жизни
                             ''')
        else:
            bot.send_message(message.from_user.id, ' == Вот тебе моё меню! == ',
                             reply_markup=keyboard('/quiz', '/reed', '/talk'))
            bot.send_message(message.from_user.id,
                             '''
[ /quiz ] - сыграть раунд в Quiz
[ /talk ] - просто поговорить с ботом о жизни
                             ''')

        dbworker.set_state(message.from_user.id, config.States.S_CHOICE.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_CHOICE.value)
def choice(message):
    if message.text == '/quiz':
        bot.send_message(message.from_user.id, ' == Режим: >> quiz << == ')
        bot.send_message(message.from_user.id,
                         ' == Хорошо, вот тебе небольшая шуточная викторина == ',
                         reply_markup=keyboard('Поехали!'))
        dbworker.set_state(message.from_user.id, config.States.S_ENTER_QUIZ.value)

    elif message.text == '/reed':
        bot.send_message(message.from_user.id, ' == Хорошо, вот твой счёт за последнюю игру! == ')
        dbworker.set_state(message.from_user.id, config.States.S_SEND_REED.value)

    elif message.text == '/talk':
        bot.send_message(message.from_user.id, ' == Если хочешь вернуть в меню, напиши /reset! == ')
        bot.send_message(message.from_user.id, ' == Режим: >> talk << == ')
        dbworker.set_state(message.from_user.id, config.States.S_TALK.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_ENTER_QUIZ.value)
def quiz(message):
    quest.q1(message.from_user.id)
    dbworker.set_state(message.from_user.id, config.States.S_MENU.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_SEND_REED.value)
def reed(message):
    pass


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.from_user.id) == config.States.S_TALK.value)
def talk(message):
    request = apiai.ApiAI('c339ca90c180455fb909135d8fb06379').text_request()
    request.lang = 'ru'
    request.session_id = 'BatlabAIBot'
    request.query = message.text

    response_json = json.loads(request.getresponse().read().decode('utf-8'))
    response = response_json['result']['fulfillment']['speech']

    if message.text.lower() == 'кто ты?' or message.text.lower() == 'ты кто?':
        bot.send_message(message.chat.id, 'Я - quiz бот, написанный на языке python')
    elif message.text.lower() == 'где ты живёшь?' or message.text.lower() == 'ты где живешь?':
        bot.send_message(message.chat.id, 'Я родился в Усолье-Сибирском ' + smiles['joy']
                         + '! Я ещё маленький и пока-что его не знаю, но мне он нравится!')
    elif response:
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, 'Я Вас не совсем понял!')


if __name__ == '__main__':
    bot.polling(none_stop=True)
