import telebot
from gpt import *
from util import *
import requests
import json

with open(r'G:\Study\Py projects\Keys\tg_chat_key.txt', 'r') as file:
    bot = telebot.TeleBot(file.read())


class Dialog:
    def __init__(self):
        self.mode = 'start'  # статус, в котором находится диалог пользователя с ботом


dialog = Dialog()
chatgpt = ChatGptService(token='gpt:EG44JHCgWRZcE28XEIsgJFkblB3TKFPdeHKs9DxUsueSBurd')
dialog.count = 0
dialog.user = {}

# обработчики команд пользователей

@bot.message_handler(commands=['start', 'help'])
def start(message):  # функция приветствия
    dialog.mode = 'start'
    # отправляю человеку стартовое приветствие
    with open(r'resources\messages\main.txt', 'r', encoding='utf-8') as start_message:
        photo = open(r'resources\images\tinder_main.png', 'rb')
        bot.send_photo(message.chat.id, photo, caption=start_message.read().replace('*', ''))
    c1 = telebot.types.BotCommand(command='start', description='Главное меню бота')
    c2 = telebot.types.BotCommand(command='profile', description='Создать профиль для Tinder')
    c3 = telebot.types.BotCommand(command='opener', description='Сгенерировать открывающее сообщение')
    c4 = telebot.types.BotCommand(command='helper', description='Помощь с ответами девушке')
    c5 = telebot.types.BotCommand(command='date', description='Потренироваться на звездах')
    c6 = telebot.types.BotCommand(command='gpt', description='Задать вопрос ChatGPT')
    bot.set_my_commands([c1, c2, c3, c4, c5, c6])
    bot.set_chat_menu_button(message.chat.id, telebot.types.MenuButtonCommands())
    menu = bot.get_chat_menu_button(message.chat.id)


@bot.message_handler(commands=['gpt'])
def gpt(message):  # функция перехода в режим общения с ботом
    dialog.mode = 'gpt'
    photo = open(r'resources\images\gpt.jpg', 'rb')
    with open(r'resources\messages\gpt.txt', 'r', encoding='utf-8') as gpt_text:
        bot.send_photo(message.chat.id, photo, caption=gpt_text.read().replace('*', ''))


@bot.message_handler(commands=['date'])
def date(message):
    photo = open(r'resources\images\date.jpg', 'rb')
    with open(r'resources\messages\date.txt', 'r', encoding='utf-8') as file:
        date_text = file.read().replace('*', '')

    inline_keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    mash_button = telebot.types.InlineKeyboardButton(text='Маш Милаш', callback_data='date_mash')
    ida_button = telebot.types.InlineKeyboardButton(text='Ида Галич', callback_data='date_ida')
    olsen_button = telebot.types.InlineKeyboardButton(text='Элизабет Олсен', callback_data="date_olsen")
    scarlet_button = telebot.types.InlineKeyboardButton(text='Скарлет Йохансон', callback_data="date_scarlet")
    ana_button = telebot.types.InlineKeyboardButton(text="Ана Де Армас", callback_data='date_ana')
    inline_keyboard.add(mash_button, ida_button, olsen_button, scarlet_button, ana_button)
    bot.send_photo(message.chat.id, photo, date_text, reply_markup=inline_keyboard)

@bot.message_handler(commands=['helper'])
def helper(message):
    dialog.mode = 'helper'
    photo = open(r'resources\images\helper.png', 'rb')
    text = open(r'resources\messages\helper.txt', 'r', encoding='2utf-8').read()
    promt = open(r'resources\prompts\helper.txt', 'r', encoding='utf-8').read()
    bot.send_photo(message.chat.id, photo, caption=text)
    chatgpt.set_prompt(promt)


# конец обработчиков команд пользователя

# обработчики нажатия кнопок
@bot.callback_query_handler(func=lambda call: True)
def choose_girl(call):
    dialog.mode = 'date'
    match call.data:
        case "date_mash":
            name = 'Маш Милаш'
            image = open(r'resources\images\photo_mash.webp', 'rb')
            promt = open(r'resources\prompts\date_mash.txt', 'r', encoding='utf-8').read()
        case 'date_ida':
            name = "Ида Галич"
            image = open(r'resources\images\photo_ida.webp', 'rb')
            promt = open(r'resources\prompts\date_ida.txt', 'r', encoding='utf-8').read()
        case 'date_olsen':
            name = 'Элизабет Олсен'
            image = open(r'resources\images\photo_olsen.jpg', 'rb')
            promt = open(r'resources\prompts\date_olsen.txt', 'r', encoding='utf-8').read()
        case 'date_ana':
            name = 'Ана Де Армас'
            image = open(r'resources\images\photo_ana.jpeg', 'rb')
            promt = open(r'resources\prompts\date_ana.txt', 'r', encoding='utf-8').read()
        case 'date_scarlet':
            name = 'Скарлет Йохансон'
            image = open(r'resources\images\photo_scarlet.jpg', 'rb')
            promt = open(r'resources\prompts\date_scarlet.txt', 'r', encoding='utf-8').read()

    bot.answer_callback_query(call.id, text='Отличный выбор!')
    text = f'Твой выбор: {name}\nПиши свое первое сообщение:'
    bot.send_photo(call.message.chat.id, image, caption=text)
    chatgpt.set_prompt(promt)


@bot.message_handler(commands=['profile'])
def profile(message):
    dialog.mode = 'profile'
    text = open(r'resources\messages\profile.txt', 'r', encoding='utf-8').read()
    photo = open(r'resources\images\profile.webp', 'rb')
    bot.send_photo(message.chat.id, photo, caption=text)

    dialog.user.clear()
    dialog.count = 0
    bot.send_message(message.chat.id, "Сколько вам лет?")


@bot.message_handler(commands=['opener'])
def opener(message):
    dialog.mode = 'opener'
    text = open(r'resources\messages\opener.txt', 'r', encoding='utf-8').read()
    photo = open(r'resources\images\opener.jpg', 'rb')
    bot.send_photo(message.chat.id, photo, caption=text)

    dialog.user.clear()
    dialog.count = 0
    bot.send_message(message.chat.id, "Как зовут девушку?")


# конец обработчиков нажатия кнопок

# простые функции
def helper_dialog(message):
    text = message.text
    bot_message = bot.send_message(message.chat.id, 'ChatGPT отвечает...')
    answer = chatgpt.add_message(text)
    bot.edit_message_text(answer, chat_id=message.chat.id, message_id=bot_message.id)


def date_dialog(message):
    text = message.text
    my_message = bot.send_message(message.chat.id, "Пишет сообщение...")
    answer = chatgpt.add_message(text)
    bot.edit_message_text(answer, chat_id=message.chat.id, message_id=my_message.id)


def gpt_dialog(message):  # функция непосредственно общения с ботом
    text_from_human = message.text
    answer = chatgpt.send_question('Напиши четкий и короткий ответ', text_from_human)
    bot.send_message(message.chat.id, answer)


def profile_dialog(message):
    text = message.text
    match dialog.count:
        case 0:
            dialog.user['age'] = text
            dialog.count += 1
            bot.send_message(message.chat.id, "Кем вы работаете?")
        case 1:
            dialog.user['profession'] = text
            dialog.count += 1
            bot.send_message(message.chat.id, "Назовите свое хобби, если оно есть")
        case 2:
            dialog.user['hobby'] = text
            dialog.count += 1
            bot.send_message(message.chat.id, "Что вам не нравится в людях?")
        case 3:
            dialog.user['dislike'] = text
            dialog.count += 1
            bot.send_message(message.chat.id, "Что вам нравится в людях?")
        case 4:
            dialog.user['like'] = text
            dialog.count += 1
            bot.send_message(message.chat.id, "Какая ваша цель знакомства?")
        case 5:
            dialog.user['goal'] = text
            dialog.count += 1
            promt = open(r'resources\prompts\profile.txt', 'r', encoding='utf-8').read()
            map = {
                'age': 'Возраст',
                'profession': 'Профессия, работа',
                'hobby': 'Хобби, любимое занятие',
                'dislike': 'Не нравится в людях',
                'like': 'Нравится в людях',
                'goal': 'Цель, ради которой сижу в Тиндере'
            }
            user_info = ''
            for key, val in map.items():
                if key in dialog.user:
                    user_info += f'{val}: {dialog.user[key]}.\n'

            my_message = bot.send_message(message.chat.id, "ChatGPT пишет ответ...")
            answer = chatgpt.send_question(promt, user_info)
            bot.edit_message_text(text=answer, chat_id=message.chat.id, message_id=my_message.id)


        case _:
            bot.send_message(message.chat.id, "Возникла ошибка, перезапустите диалог по команде /profile")

def opener_dialog(message):
    text = message.text

    match dialog.count:
        case 0:
            dialog.girl['name'] = text
            dialog.count += 1
            bot.send_message(message.chat.id, 'Сколько ей лет?')
        case 1:
            dialog.girl['age'] = text
            dialog.count += 1
            bot.send_message(message.chat.id, 'Оцени ее внешность от 1 до 5 баллов')
        case 2:
            dialog.girl['look'] = text
            dialog.count += 1


# конец простых функций


# обработчик любого текста пользователя и определение, куда этот текст будет направлен
@bot.message_handler(content_types=['text'])
def main(message):  # функция для перемещения по машине состояний
    match dialog.mode:
        case 'start':
            start(message)
        case 'gpt':
            gpt_dialog(message)
        case 'date':
            date_dialog(message)
        case 'helper':
            helper_dialog(message)
        case 'profile':
            profile_dialog(message)
        case 'opener':
            opener_dialog(message)





bot.infinity_polling()

