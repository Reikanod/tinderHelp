import telebot
from gpt import *
from util import *

# тут будем писать наш код :)

with open(r'G:\Study\Py projects\Keys\tg_chat_key.txt', 'r') as file:
    app = telebot.TeleBot(file.read()).build()
app.run_polling()



