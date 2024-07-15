import telebot
from gpt import *
from util import *
import requests

with open(r'G:\Study\Py projects\Keys\tg_chat_key.txt', 'r') as file:
    bot = telebot.TeleBot(file.read())


class Dialog:
    def __init__(self):
        self.mode = 'start'  # статус, в котором находится диалог пользователя с ботом


dialog = Dialog()
chatgpt = ChatGptService(token='gpt:EG44JHCgWRZcE28XEIsgJFkblB3TKFPdeHKs9DxUsueSBurd')

# обработчики команд пользователей

@bot.message_handler(commands=['start', 'help'])
def start(message):  # функция приветствия
    dialog.mode = 'start'
    # отправляю человеку стартовое приветствие
    with open(r'resources\messages\main.txt', 'r', encoding='utf-8') as start_message:
        photo = open(r'resources\images\tinder_main.png', 'rb')
        bot.send_photo(message.chat.id, photo, caption=start_message.read().replace('*', ''))


@bot.message_handler(commands=['gpt'])
def gpt(message):  # функция перехода в режим общения с ботом
    dialog.mode = 'gpt'
    photo = open(r'resources\images\gpt.jpg', 'rb')
    with open(r'resources\messages\gpt.txt', 'r', encoding='utf-8') as gpt_text:
        bot.send_photo(message.chat.id, photo, caption=gpt_text.read().replace('*', ''))


@bot.message_handler(commands=['date'])
def date(message):
    dialog.mode = 'date'
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

# конец обработчиков команд пользователя

# обработчики нажатия кнопок
@bot.callback_query_handler(func=lambda call: True)
def choose_girl(call):
    match call.data:
        case "date_mash":
            name = 'Маш Милаш'
            image = open(r'resources\images\photo_mash.webp', 'rb')
        case 'date_ida':
            name = "Ида Галич"
            image = open(r'resources\images\photo_ida.webp', 'rb')
        case 'date_olsen':
            name = 'Элизабет Олсен'
            image = open(r'resources\images\photo_olsen.jpg', 'rb')
        case 'date_ana':
            name = 'Ана Де Армас'
            image = open(r'resources\images\photo_ana.jpeg', 'rb')
        case 'date_scarlet':
            name = 'Скарлет Йохансон'
            image = open(r'resources\images\photo_scarlet.jpg', 'rb')
    bot.answer_callback_query(call.id, text='Отличный выбор!')
    text = f'Твой выбор: {name}'
    bot.send_photo(call.message.chat.id, image, caption=text)
    date_dialog(call.message)

# конец обработчиков нажатия кнопок


# простые функции
def date_dialog(message):



def gpt_dialog(message):  # функция непосредственно общения с ботом
    text_from_human = message.text
    answer = chatgpt.send_question('Напиши четкий и короткий ответ', text_from_human)
    bot.send_message(message.chat.id, answer)
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




bot.infinity_polling()

