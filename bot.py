# import telebot
# from gpt import *
# from util import *
# with open(r'G:\Study\Py projects\Keys\tg_chat_key.txt', 'r') as file:
#     bot = telebot.TeleBot(file.read())
#
# @bot.message_handler(commands=['start'])
# def hello(message):
#     bot.send_message(message.chat.id, 'Привет')
#
# bot.infinity_polling()

from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler
from gpt import *
from util import *
with open(r'G:\Study\Py projects\Keys\tg_chat_key.txt', 'r') as file:
    TOKEN = file.read()

async def start(update, context):
    text = load_message('main')
    await send_photo(update, context, 'main')
    await send_photo(update, context, text)

async def hello(update, context):
    await send_text(update, context, '*Привет*')
    await send_text(update, context, "_Как дела_")
    await send_text(update, context, 'вы написали' + update.message.text)

    await send_photo(update, context, 'avatar_main')
    await send_text_buttons(update, context, "Запустить процесс?", {
        "start": "Запустить",
        'stop': "Остановить"
    })

async def hell0_button(update, context):
    query = update.callback_query.data
    if query == 'start':
        await send_text(update, context, "процесс запущен")
    else:
        await send_text(update, context, "Процесс остановлен")


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(hell0_button))
app.run_polling()

