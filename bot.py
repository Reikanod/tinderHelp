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

async def gpt(update, context):
    dialog.mode = 'gpt'
    text = load_message("gpt")
    await send_photo(update, context, "gpt")
    await send_text(update, context, text)

async def start(update, context):
    dialog.mode = 'main'
    text = load_message('main')
    await send_photo(update, context, 'main')
    await send_photo(update, context, text)

async def gpt_dialog(update, context):
    text = update.message.text
    answer = await chatgpt.send_question('напиши четкий и короткий ответ на следующий вопрос', text)
    await send_text(update, context, 'вы общаетесь с чат гпт')

async def hello(update, context):
    if dialog.mode == 'gpt':
        await gpt_dialog(update, context)
    else:
        await send_text(update, context, '*Привет*')
        await send_text(update, context, "_Как дела_")
        await send_text(update, context, 'вы написали' + update.message.text)

        await send_photo(update, context, 'avatar_main')
        await send_text_buttons(update, context, "Запустить процесс?", {
            "start": "Запустить",
            'stop': "Остановить"
        })

async def hello_button(update, context):
    query = update.callback_query.data
    if query == 'start':
        await send_text(update, context, "процесс запущен")
    else:
        await send_text(update, context, "Процесс остановлен")


dialog = Dialog()
dialog.mode = None

chatgpt = ChatGptService(token='EG44JHCgWRZcE28XEIsgJFkblB3TKFPdeHKs9DxUsueSBurd')

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('gpt', gpt))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(hello_button))
app.run_polling()

