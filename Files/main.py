import json
import logging
import time
import telethon
import yaml
import re

from config import API
from config import admin_password
from config import api_hash, api_id
from config import Channels
from config import Words
from config import i_Words
from config import Messages
from config import Deleting
from config import DeletingWords
from config import DeletingIWords
from config import DeletingMessage
from config import AccountName
from config import AdminPassword
from config import titles_main
from config import titles_channels
from config import titles_confirmation
from config import titles_words
from config import titles_i_words
from config import titles_message
from config import ChannelsButtons
from config import MenuButtons
from config import ConfirmationButtons
from config import BackToMenuButtons
from config import WordsButtons
from config import I_WordsButton
from config import MessageButtons

from data import get_all_values
from data import insert_values
from data import del_values
from data import insert_many_values

from client import start_client


from aiogram import Dispatcher, executor, types
from aiogram.bot import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from datetime import datetime
from fnmatch import fnmatch as fn

from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.messages import GetHistoryRequest
from telethon import events


# Кнопки
markup_main_menu = ReplyKeyboardMarkup(row_width=2)
markup_main_menu.add(
    MenuButtons.tg_channels,
    MenuButtons.words,
    MenuButtons.i_words,
    MenuButtons.message_text,
    MenuButtons.running,
    MenuButtons.doc
)
markup_channels_menu = ReplyKeyboardMarkup(row_width=1)
markup_channels_menu.add(
    ChannelsButtons.add_channel,
    ChannelsButtons.del_channel,
    ChannelsButtons.back_to_menu
)
markup_confirmation_menu = ReplyKeyboardMarkup(row_width=1)
markup_confirmation_menu.add(
    ConfirmationButtons.confirm,
    ConfirmationButtons.back_to_menu
)
markup_back_to_menu = ReplyKeyboardMarkup(row_width=1)
markup_back_to_menu.add(
    BackToMenuButtons.back_to_menu
)
markup_words_menu = ReplyKeyboardMarkup(row_width=2)
markup_words_menu.add(
    WordsButtons.add_new_words,
    WordsButtons.del_words,
    WordsButtons.back_to_menu
)
markup_i_words_menu = ReplyKeyboardMarkup(row_width=2)
markup_i_words_menu.add(
    I_WordsButton.add_new_i_word,
    I_WordsButton.del_i_word,
    I_WordsButton.back_to_menu
)
markup_message_menu = ReplyKeyboardMarkup(row_width=2)
markup_message_menu.add(
    MessageButtons.remake_message,
    MessageButtons.del_message,
    MessageButtons.back_to_menu
)
# Переменные и запуск базовых процессов
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler()

users_messages = {}
users_info = {}
channels_d = [None]

user_is_admin = [False]
client = start_client(
    name='YaGlee',
    api_id=api_id,
    api_hash=api_hash
)
client.start()



async def handler(dp=dp):
    @client.on(events.NewMessage())
    async def check(event):
        #print("Check passed")
        users_ids = get_all_values('messages_history', 'user_id')
        users_ids = table_list(users_ids)
        if users_ids:
            users_ids = [int(i[:-1]) for i in users_ids]
        answered = get_all_values('auto_answered', 'user_id')
        answered = table_list(answered)
        if answered:
            for i in range(len(answered)):
                answered[i] = answered[i][:-1]
                if answered[i] == '':
                    answered.pop(i)
            else:
                answered = [int(i) for i in answered]
            #answered = [int(i[:-1]) for i in answered]
        sender = await event.get_sender()
        if sender.id in users_ids:
            if sender.id not in answered:
                # print("Auto message answered")
                # print(answered, users_ids)
                await client.send_message(sender.id, "Aloha")
                insert_values('auto_answered', str(sender.id), 'user_id')


async def main_cycle(dp=dp):
    channels = get_all_values('telegram_channels', 'url')
    channels = table_list(channels)
    time_range = list(range(9, 16))
        # scheduler.add_job(handler, 'interval', seconds=0.2, args=(dp,))
    if int(datetime.now().hour) in time_range:
        #print("Bot is sleeping")
        #time.sleep(600)
        pass
    else:
        for channel in channels:
            channels_d[0] = channel
            await main(channel[:-1],
                    client)
            time.sleep(60)
                

        # print(users_ids)
        # print(sender.id)
    # In this case, the result is a ``Match`` object
    # since the `str` pattern was converted into
    # the ``re.compile(pattern).match`` function.


def table_list_string(data):
    string = ""
    for i in range(len(data)):
        string += str(i + 1) + ". " + str(data[i])[:-1] + '\n'
    string = string.replace("'", '')
    string = string.replace("(", "").replace(")", "")
    return string


def table_list(data):
    string = ""
    for i in range(len(data)):
        data[i] = str(data[i]).strip().split("\\n")
        data[i] = str(["\n".join(data[i])])
        data[i] = str(data[i]).replace("(", "").replace(")", "").replace("'", "")[1:-1]
        data[i] = yaml.safe_load(data[i])
    
    return data


def message_text_string(data):
    for i in range(len(data)):
        data[i] = str(data[i]).replace("'", "").replace("(", "").replace(")", "").replace('\\n', '\n')
    return data

@dp.message_handler(regexp=titles_words[2])
@dp.message_handler(regexp=titles_channels[2])
async def back_to_menu(message: types.Message):
    await message.answer("Вы вернулись обратно в меню",
                         reply_markup=markup_main_menu)


@dp.message_handler(regexp=titles_main[5])
async def doc(message: types.Message):
    await message.answer(
        "Документацию вы можете прочитать по ссылке: \n"
        "https://docs.google.com/document/d/1t1GUg6RjH0Duy9ThdjdT4wh6fNUn-U43WDOlKRH_nss/edit?usp=sharing"
    )


# Приветственное сообщение
@dp.message_handler(commands=['start'])
async def main_menu(message: types.Message):
    #scheduler.add_job(..., 'interval', seconds=15, args=(dp,))
    await message.answer("Введите пароль от панели управления")
    await AdminPassword.next()


@dp.message_handler(state=AdminPassword.password)
async def checking_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['p'] = message.text
        if data['p'] == admin_password:
            await state.finish()
            await message.answer("Это телеграм бот для парсинга и рассылки сообщений "
                                 "по ключевым словам.", reply_markup=markup_main_menu)
            user_is_admin[0] = True
        else:
            await message.answer("Пароль не верный")
            await state.reset_state()
            await main_menu(message)


# Телеграм каналы
@dp.message_handler(regexp=titles_main[0])
async def channels_menu(message: types.Message):
    channels = get_all_values('telegram_channels', 'url')
    channels = table_list(channels)
    if not channels:
        await message.answer("У вас еще не добавлено ни одного телеграм канала\n"
                             "Нажмите на кнопку <b>'Добавить телеграм канал'</b>.",
                             parse_mode='html',
                             reply_markup=markup_channels_menu)
    else:
        await message.answer(f"Список телеграм каналов:\n"
                             f"{table_list_string(channels)}",
                             reply_markup=markup_channels_menu)


@dp.message_handler(regexp=titles_channels[0])
async def add_channel(message: types.Message):
    await message.answer("Введите ссылку на телеграм канал формата https://t.me/имя_канала")
    await Channels.next()


@dp.message_handler(state=Channels.channel_url)
async def process_channels(message: types.Message, state: FSMContext):
    pattern = "https://t.me/*"
    channels = get_all_values('telegram_channels', 'url')
    channels = table_list(channels)
    async with state.proxy() as data:
        try:
            data['channel_name'] = message.text
            if message.text == '/stop':
                await channels_menu(message)
                await state.finish()
            elif not fn(message.text, pattern):
                await message.answer("Ссылка введена некорректно")
                await state.finish()
                await add_channel(message)
            elif f"{data['channel_name']}" in channels:
                await message.answer("Ссылка уже есть в списке\n"
                                     "Введите ссылку заново или напишите команду /stop")
            else:
                insert_values('telegram_channels', str(data['channel_name']), 'url')
                await message.answer("Ссылка добавлена, введите следующую\n"
                                     "Если вы хотите завершить процесс добавления "
                                     "ссылок напишите команду нажмите на кнопку 'Обратно в меню'",
                                     reply_markup=markup_channels_menu)
                await state.reset_state()
        except ValueError:
            await message.answer("Ссылка введена некорректно")
            await state.finish()
            await add_channel(message)


@dp.message_handler(regexp=titles_channels[1])
async def ask_num_of_channel(message: types.Message):
    channels = get_all_values('telegram_channels', 'url')
    channels = table_list(channels)
    markup_nums = ReplyKeyboardMarkup(row_width=4)
    for i in range(len(channels)):
        markup_nums.add(
            KeyboardButton(text=str(i+1))
        )
    markup_nums.add(
        KeyboardButton(text='Обратно в меню')
    )
    await message.answer("Выберите номер ссылки для удаления",
                         reply_markup=markup_nums)
    await Deleting.next()


@dp.message_handler(state=Deleting.value_num)
async def ask_confirmation(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['value_num'] = message.text
        if data['value_num'] == 'Обратно в меню':
            await message.answer("Удаление отменено")
            await state.finish()
            await channels_menu(message)
        else:
            await message.answer("Подтвердите удаление",
                                 reply_markup=markup_confirmation_menu)
            await Deleting.next()


@dp.message_handler(state=Deleting.confirmation)
async def deleting_channel(message: types.Message, state: FSMContext):
    channels = get_all_values('telegram_channels', 'url')
    channels = table_list(channels)
    async with state.proxy() as data:
        data['confirmation'] = message.text
        if data['confirmation'] == titles_confirmation[0]:
            del_values('telegram_channels', channels[int(data['value_num'])-1], 'url')
            await message.answer("Ссылка успешно удалена")
            await state.finish()
            await channels_menu(message)
        elif data['confirmation'] == titles_confirmation[1]:
            await message.answer("Удаление отменено")
            await state.finish()
            await channels_menu(message)


# Команда /stop
@dp.message_handler(state=Messages.message, regexp='/stop')
@dp.message_handler(state=Channels.channel_url, regexp='/stop')
async def stop_process(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Заполнение окончено")


# Текст рекламного сообщения
@dp.message_handler(regexp=titles_main[3])
async def message_text_menu(message: types.Message):
    messages = get_all_values('message_text', 'text')
    messages = table_list(messages)
    if not messages:
        await message.answer("Рекламное сообщение еще не добавлено\n"
                             "Нажмите на кнопку 'Ввести новое сообщение' и создайте его",
                             reply_markup=markup_message_menu)
    else:
        messages_s = table_list_string(messages)
        await message.answer(f"Текущее рекламное сообщение\n\n"
                             f"{messages_s}",
                             reply_markup=markup_message_menu)


@dp.message_handler(regexp=titles_message[0])
async def ask_new_message_text(message: types.Message):
    await message.answer("Введите текст нового рекламного сообщения")
    await Messages.next()


@dp.message_handler(state=Messages.message)
async def process_new_message_text(message: types.Message, state: FSMContext):
    messages = get_all_values('message_text', 'text')
    messages = message_text_string(messages)
    async with state.proxy() as data:
        data['message'] = message.text
        if data['message'] == '/stop':
            await state.finish()
            await message_text_menu(message)
        else:
            if len(messages) != 0:
                messages[0] = messages[0][:-1]
                del_values('message_text', messages[0], 'text')
                insert_values('message_text', data['message'], 'text')
                await message.answer(data['message'])
                await message.answer("Сообщение успешно добавлено",
                                     reply_markup=markup_message_menu)
                await state.finish()
            else:
                insert_values('message_text', data['message'], 'text')
                await message.answer(data['message'])
                await message.answer("Сообщение успешно добавлено",
                                     reply_markup=markup_message_menu)
                await state.finish()


@dp.message_handler(regexp=titles_message[1])
async def del_message(message: types.Message):
    await message.answer("Подтвердите удаление текущего рекламного сообщения",
                         reply_markup=markup_confirmation_menu)
    await DeletingMessage.next()


@dp.message_handler(state=DeletingMessage.confirmation)
async def del_message_confirmation(message: types.Message, state: FSMContext):
    messages = get_all_values('message_text', 'text')
    messages = table_list(messages)
    async with state.proxy() as data:
        data['confirmation'] = message.text
        if data['confirmation'] == titles_confirmation[0] and messages:
            await message.answer("Сообщение успешно удалено!")
            del_values('message_text', messages[0], 'text')
            await state.finish()
            await back_to_menu(message)
        elif data['confirmation'] == titles_confirmation[1]:
            await message.answer("Удаление отменено")
            await state.finish()
            await back_to_menu(message)


# Ключевые слова
@dp.message_handler(regexp=titles_main[1])
async def words_menu(message: types.Message):
    words = get_all_values('q_words', 'text')
    words = table_list(words)
    if not words:
        await message.answer("У вас еще не добавлено ни одного ключевого слова\n"
                             "Нажмите на кнопку <b>'Задать ключевые слова'</b>.",
                             parse_mode='html',
                             reply_markup=markup_words_menu)
    else:
        await message.answer(f"Ключевые слова:\n"
                             f"{table_list_string(words)}",
                             reply_markup=markup_words_menu)


@dp.message_handler(regexp=titles_words[0])
async def new_q_words(message: types.Message):
    await message.answer("Напишите новые ключевые слова.\n\n"
                         "Примеры:\n"
                         "> Купить дом\n"
                         "> Аренда квартиры\n"
                         "> Дом\n")
    await Words.next()


@dp.message_handler(state=Words.word)
async def process_word(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == '/stop':
            await state.finish()
            await words_menu(message)
        else:
            data['word'] = message.text
            insert_values('q_words', data['word'].lower(), 'text')
            await message.answer('Напишите следующее ключевое слово\n'
                                 'Для завершения заполнения напишите команду /stop')


@dp.message_handler(regexp=titles_main[2])
async def i_words_menu(message: types.Message):
    i_words = get_all_values('i_words', 'text')
    i_words = table_list(i_words)
    if not i_words:
        await message.answer("Слов исключений еще нету.\n"
                             "Добавьте их по кнопке <b>\"Задать слова исключения\"</b>",
                             reply_markup=markup_i_words_menu,
                             parse_mode='html')
    else:
        await message.answer("Слова исключения:")
        await message.answer(table_list_string(i_words),
                             reply_markup=markup_i_words_menu)


@dp.message_handler(regexp=titles_i_words[0])
async def process_add_i_words(message: types.Message):
    await message.answer("Введите слово исключение")
    await i_Words.next()


@dp.message_handler(state=i_Words.i_word)
async def add_new_i_word(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['i_word'] = message.text
        if data['i_word'] == '/stop':
            await state.finish()
            await i_words_menu(message)
        else:
            insert_values('i_words', data['i_word'].lower(), 'text')
            await message.answer('Напишите следующее слово исключение\n'
                                 'Для завершения заполнения напишите команду /stop')


@dp.message_handler(regexp=titles_i_words[1])
async def process_del_i_word(message: types.Message):
    i_words = get_all_values('i_words', 'text')
    i_words = table_list(i_words)
    markup_num = ReplyKeyboardMarkup(row_width=1)
    for i in range(len(i_words)):
        markup_num.add(
            KeyboardButton(
                text=str(i+1)
            )
        )
    markup_num.add(
        KeyboardButton(
            text="Отмена"
        )
    )
    await message.answer("Выберите номер ключевого слова, которое вы хотите удалить",
                         reply_markup=markup_num)
    await DeletingIWords.next()


@dp.message_handler(state=DeletingIWords.value_num)
async def ask_del_i_confirmation(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['i_value'] = message.text
        if data['i_value'] == 'Отмена':
            await state.finish()
            await back_to_menu(message)
        else:
            await message.answer("Подтвердите удаление",
                                 reply_markup=markup_confirmation_menu)
            await DeletingIWords.next()


@dp.message_handler(state=DeletingIWords.confirmation)
async def process_deleting_i_word(message: types.Message, state: FSMContext):
    i_words = get_all_values('i_words', 'text')
    i_words = table_list(i_words)
    async with state.proxy() as data:
        data['confirmation'] = message.text
        if data['confirmation'] == titles_confirmation[0]:
            del_values(
                'i_words',
                i_words[int(data['i_value'])-1],
                'text'
            )
            await state.finish()
            await message.answer("Слово успешно удалено",
                                 reply_markup=markup_main_menu)
        elif data['confirmation'] == titles_confirmation[1]:
            await message.answer("Удаление отменено")
            await back_to_menu(message)


@dp.message_handler(regexp=titles_words[1])
async def del_words(message: types.Message):
    words = get_all_values('q_words', 'text')
    words = table_list(words)
    markup_nums = ReplyKeyboardMarkup(row_width=3)
    for i in range(len(words)):
        markup_nums.add(
            KeyboardButton(text=str(i+1))
        )
    markup_nums.add(
        KeyboardButton(text="Вернуться в меню")
    )
    await message.answer("Выберите номер удаляемого слова",
                         reply_markup=markup_nums)
    await DeletingWords.next()


@dp.message_handler(state=DeletingWords.value_num)
async def del_confirmation(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['value_num'] = message.text
    await message.answer("Подтвердите удаление",
                         reply_markup=markup_confirmation_menu)
    await DeletingWords.next()


@dp.message_handler(state=DeletingWords.confirmation)
async def del_process(message: types.Message, state: FSMContext):
    words = get_all_values('q_words', 'text')
    words = table_list(words)
    async with state.proxy() as data:
        data['conf'] = message.text
        if data['conf'] == titles_confirmation[0]:
            del_values('q_words', words[int(data['value_num'])-1], 'text')
            await message.answer("Ключевое слово успешно удалена")
            await state.finish()
            await words_menu(message)
        elif data['conf'] == titles_confirmation[1]:
            await message.answer("Удаление отменено")
            await state.finish()
            await words_menu(message)


@dp.message_handler(regexp=titles_main[4])
async def start_running(message: types.Message):
    words = get_all_values('q_words', 'text')
    words = table_list(words)
    messages = get_all_values('message_text', 'text')
    messages = table_list(messages)
    channels = get_all_values('telegram_channels', 'url')
    channels = table_list(channels)
    if not words:
        await message.answer("У вас еще не указаны ключевые слова "
                             "с которыми боту предстоит работать\n"
                             "Укажите их в меню-ключевые слова")
    elif not messages:
        await message.answer("У вас еще не указано рекламное сообщение"
                             "с которым бот будет работать\n"
                             "Укажите их в меню-текст рекламного сообщения")
    elif not channels:
        await message.answer("У вас еще не указаны телеграм каналы"
                             "которые будет анализировать бот\n"
                             "Укажите их в меню-телеграм каналы")
    else:
        await message.answer("Введите короткое имя аккаунта, без значка @ "
                             "с которого будет проводиться рассылка.")
        await AccountName.next()


@dp.message_handler(state=AccountName.name)
async def process_account_name(message: types.Message, state: FSMContext):
    channels = get_all_values('telegram_channels', 'url')
    channels = table_list(channels)
    async with state.proxy() as data:
        data['name'] = message.text
        # client.disconnect()
        # client = start_client(
        #     data['name'],
        #     api_id,
        #     api_hash
        # )
        # await client.start()
        # await client.connect()
    await message.answer("Укажите данные на сервере в консоли. Подробнее смотрите в документации.")
    await message.answer("После этого бот начнет свою работу.")
    await message.answer("Если до этого вы запускали бота с указанного аккаунта, "
                         "то ничего вводить повторно не нужно будет")
    await message.answer("Если вы все сделали верно, бот начнет присылать логи отправленных сообщений")
    scheduler.add_job(main_cycle, 'interval', seconds=0.2, args=(dp,))
        # else:
        #     await message.answer("Бот завершил свою работу")
        #     await state.finish()
        #     await client.disconnect()
        #     await back_to_menu(message)


async def dump_all_participants(channel, client):
    offset_user = 0
    limit_user = 100

    all_participants = []
    filter_user = ChannelParticipantsSearch('')

    while True:
        participants = await client(GetParticipantsRequest(channel,
                                                           filter_user, offset_user, limit_user, hash=0))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset_user += len(participants.users)

    all_users_details = []

    for participant in all_participants:
        all_users_details.append({f"id": participant.id,
                                  "user": participant.username,
                                  "phone": participant.phone})

    for i in range(len(all_users_details)):
        users_info[all_users_details[i]['id']] = f"https://t.me/{all_users_details[i]['user']} " \
                                                 f"({all_users_details[i]['phone']})"


# Parse messages func
async def dump_all_messages(channel, client):
    offset_msg = 0
    limit_msg = 100

    all_messages = []
    total_count_limit = 0

    class DateTimeEncoder(json.JSONEncoder):

        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()
            if isinstance(o, bytes):
                return list(o)
            return json.JSONEncoder.default(self, o)

    while True:
        history = await client(GetHistoryRequest(
            peer=channel,
            offset_id=offset_msg,
            offset_date=None, add_offset=0,
            limit=limit_msg, max_id=0, min_id=0,
            hash=0))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            for i in range(len(message.to_dict())):
                date = message.to_dict()['date'].replace(tzinfo=None)
                # print(abs((date - datetime.now()).days) < 7)
                if abs((date - datetime.now()).days) < 7:
                    all_messages.append(message.to_dict())
                else:
                    break
        offset_msg = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break

    words = get_all_values('q_words', 'text')
    words = table_list(words)
    i_words = get_all_values('i_words', 'text')
    i_words = table_list(i_words)
    for i in range(len(all_messages)):
        date = str(all_messages[i]['date'])[:10]
        date = datetime(int(date[:4]),
                        int(date[5:7]),
                        int(date[8:]))
        date_delta = date - datetime.now()
        date_delta = int(date_delta.days)
        # print(all_messages[i])
        if date_delta > -7:
            try:
                for x in words:
                    try:
                        for i_word in i_words:
                            i_word_s = f"*{i_word.replace(' ', '*')}*"
                            if fn(all_messages[i]['message'].lower(), i_word_s):
                                break
                        else:
                            if fn(all_messages[i]['message'], "*"+x.replace(" ", "*")+"*"):
                                users_messages[all_messages[i]['from_id']['user_id']] = all_messages[i]['message']
                    except KeyError:
                        break
            except TypeError or KeyError:
                break
        else:
            break


async def main(url, client):
    channel = await client.get_entity(url)
    await dump_all_messages(channel,
                            client)
    await dump_all_participants(
        channel,
        client
    )
    await spam_messages(client, users_info)


async def spam_messages(client: telethon.client.telegramclient.TelegramClient, users):
    users_ids = get_all_values('messages_history', 'user_id')
    users_ids = table_list(users_ids)
    users_dates = get_all_values('messages_history', 'date')
    users_dates = table_list(users_dates)
    message = get_all_values('message_text', 'text')
    message = table_list(message)
    message_dates = {}
    for i in range(len(users_dates)):
        date = datetime.strptime(
            users_dates[i][:19],
            '%Y-%m-%d %H:%M:%S'
        )
        message_dates[users_ids[i]] = date
    # print(users_dates)
    # print(users_ids)
    for user in users.keys():
        # try:
        if message_dates:
            if str(user) in message_dates.keys():
                if int((message_dates[str(user)] - datetime.now()).days) < -7:
                    del_values('messages_history', user, 'user_id')
            if user in users_messages.keys():
                if str(user) in users_ids:
                    continue
                else:
                    if user in users_messages.keys():
                        await client.send_message(
                            user,
                            message[0]
                        )
                        insert_many_values(
                            'messages_history',
                            [
                                (
                                    datetime.now(),
                                    user
                                )
                            ]
                        )
                        await logging(
                            datetime.now(),
                            channels_d[0],
                            users_info[user],
                            users_messages[user],
                            message[0]
                        )
            else:
                continue
        # except KeyError:
        #     continue


async def logging(date,
                  channel,
                  ID,
                  message,
                  spam_text):
    # 5398962531
    log = f"""
Дата:\n
{date}\n
Ссылка на группу:\n
{channel}\n
Клиент:\n
{ID}\n
Найденное сообщение:\n
{message}\n
Отправленное сообщение:\n
{spam_text}\n
"""
    await bot.send_message(
        5398962531,
        log
    )


if __name__ == '__main__':
    scheduler.start()
    scheduler.add_job(handler, 'interval', seconds=0.2, args=(dp,))
    executor.start_polling(dp, skip_updates=True)