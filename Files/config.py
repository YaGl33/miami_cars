import configparser

from aiogram.types import KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup

API = '5922115053:AAGbgEquH8AxFOPrgwqSx6sjC9eJ1OvDjgk'

admin_password = "asyd98asuajsa2"

config = configparser.ConfigParser()

config.read("config.ini")
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
# client = TelegramClient(username, int(api_id), api_hash)


titles_main = [
    'Телеграм каналы',
    'Ключевые слова',
    'Слова исключения',
    'Текст рекламного сообщения',
    'Запуск',
    'Документация'
]
titles_channels = [
    'Добавить телеграм канал',
    'Удалить телеграм канал',
    'Обратно в меню'
]
titles_confirmation = [
    'Подтвердить',
    'Отмена'
]
titles_words = [
    'Задать ключевое слово',
    'Удалить слова',
    'Обратно в меню'
]
titles_i_words = [
    'Добавить слово исключение',
    'Удалить слово',
    'Обратно в меню'
]
titles_message = [
    'Ввести новое сообщение',
    'Удалить сообщение',
    'Обратно в меню'
]


class ChannelsButtons(KeyboardButton):
    add_channel = KeyboardButton(text=titles_channels[0])
    del_channel = KeyboardButton(text=titles_channels[1])
    back_to_menu = KeyboardButton(text=titles_channels[2])


class MenuButtons(KeyboardButton):
    tg_channels = KeyboardButton(text=titles_main[0])
    words = KeyboardButton(text=titles_main[1])
    i_words = KeyboardButton(text=titles_main[2])
    message_text = KeyboardButton(text=titles_main[3])
    running = KeyboardButton(text=titles_main[4])
    doc = KeyboardButton(text=titles_main[5])


class ConfirmationButtons(KeyboardButton):
    confirm = KeyboardButton(text=titles_confirmation[0])
    back_to_menu = KeyboardButton(text=titles_confirmation[1])


class BackToMenuButtons(KeyboardButton):
    back_to_menu = KeyboardButton(text=titles_confirmation[1])


class WordsButtons(KeyboardButton):
    add_new_words = KeyboardButton(text=titles_words[0])
    del_words = KeyboardButton(text=titles_words[1])
    back_to_menu = KeyboardButton(text=titles_words[2])


class I_WordsButton(KeyboardButton):
    add_new_i_word = KeyboardButton(text=titles_i_words[0])
    del_i_word = KeyboardButton(text=titles_i_words[1])
    back_to_menu = KeyboardButton(text=titles_i_words[2])


class MessageButtons(KeyboardButton):
    remake_message = KeyboardButton(text=titles_message[0])
    del_message = KeyboardButton(text=titles_message[1])
    back_to_menu = KeyboardButton(text=titles_message[2])


class Channels(StatesGroup):
    channel_url = State()


class Words(StatesGroup):
    word = State()


class i_Words(StatesGroup):
    i_word = State()


class Messages(StatesGroup):
    message = State()


class Deleting(StatesGroup):
    value_num = State()
    confirmation = State()


class DeletingWords(StatesGroup):
    value_num = State()
    confirmation = State()


class DeletingIWords(StatesGroup):
    value_num = State()
    confirmation = State()


class DeletingMessage(StatesGroup):
    confirmation = State()


class AccountName(StatesGroup):
    name = State()


class AdminPassword(StatesGroup):
    password = State()