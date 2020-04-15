
# -*- coding: utf-8 -*-

from enum import Enum

proxy = 'socks5h://rQBuc6:Z96C76@45.32.155.5:48992'
TOKEN = '921731373:AAEn_BW6-XdC6CLq0icXiteT_NM8G9tetlA'
db_file = 'cache/database/database.vdb'


class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = '0'  # Начало нового диалога
    S_CHOICE = '1'
    S_MENU = '2'
    S_ENTER_QUIZ = '3'
    S_SEND_REED = '4'
    S_TALK = '5'
