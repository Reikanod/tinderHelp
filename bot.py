import telebot
from gpt import *
from util import *
with open(r'G:\Study\Py projects\Keys\tg_chat_key.txt', 'r') as file:
    bot = telebot.TeleBot(file.read())

class Dialog():
    def __init__(self):
        self.mode = 'start' # статус, в котором находится диалог пользователя с ботом
dialog = Dialog()
chatgpt = ChatGptService(token='gpt:EG44JHCgWRZcE28XEIsgJFkblB3TKFPdeHKs9DxUsueSBurd')


@bot.message_handler(commands=['start', 'help'])
def start(message): # функция приветствия
    dialog.mode = 'start'
    # отправляю человеку стартовое приветствие
    with open(r'resources\messages\main.txt', 'r', encoding='utf-8') as start_message:
        photo = open(r'resources\images\main.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, caption=start_message.read().replace('*', ''))

@bot.message_handler(commands=['gpt'])
def gpt(message): # функция перехода в режим общения с ботом
    dialog.mode = 'gpt'
    photo = open(r'resources\images\gpt.jpg', 'rb')
    with open(r'resources\messages\gpt.txt', 'r', encoding='utf-8') as gpt_text:
        bot.send_photo(message.chat.id, photo, caption=gpt_text.read().replace('*', ''))


@bot.message_handler()
def gpt_dialog(message):
    text_from_human = message.text
    answer = chatgpt.send_question('Напиши четкий и короткий ответ', text_from_human)
    bot.send_message(message.chat.id, answer)



@bot.message_handler(content_types=['text'])
def main(message): # функция для перемещения по машине состояний
    match dialog.mode:
        case 'start': start()
        case 'gpt': pass
    bot.send_message(message.chat.id, "Сообщение")












bot.infinity_polling()

# from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler
# from gpt import *
# from util import *
# import requests
# with open(r'G:\Study\Py projects\Keys\tg_chat_key.txt', 'r') as file:
#     TOKEN = file.read()
#
# async def gpt(update, context):
#     dialog.mode = 'gpt'
#     text = load_message("gpt")
#     await send_photo(update, context, "gpt")
#     await send_text(update, context, text)
#
# async def date(update, context):
#     dialog.mode = 'date'
#     text = load_message("date")
#     await send_photo(update, context, "date")
#     await send_text_buttons(update, context, text, {
#         'date_grande': 'Ариана Гранде',
#         'date_robbie': 'Марго Робби',
#         'date_mash': 'Маш Милаш',
#         'date_rayan': 'Райан Гослинг',
#         'date_tom': 'Том Харди'
#     })
#
# async def date_dialog(update, context):
#     pass
#
# async def date_button(update, context):
#     query = update.callback_query.data
#     await update.callback_query.answer()
#
#
#     mash_img = 'https://oyda.ru/wp-content/uploads/2023/12/mash-milash-maksim-1.webp'
#     await app.sendPhoto()
#     await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
#     await send_text(update, context, mash_img)
#
#
# async def start(update, context):
#     dialog.mode = 'main'
#     text = load_message('main')
#     await send_photo(update, context, 'main')
#     await send_text(update, context, text)
#
#     await show_main_menu(update, context, {
#         "start": 'Главное меню бота',
#         "profile": 'генерация Tinder-профля 😎',
#         "opener": 'сообщение для знакомства 🥰',
#         "message": 'переписка от вашего имени 😈',
#         "date": 'переписка со звездами 🔥',
#         "gpt": 'задать вопрос чату GPT 🧠',
#     })
#
# async def gpt_dialog(update, context):
#     text = update.message.text
#     answer = await chatgpt.send_question('напиши четкий и короткий ответ на следующий вопрос', text)
#     await send_text(update, context, 'вы общаетесь с чат гпт')
#     await send_text(update, context, answer)
#
# async def hello(update, context):
#     if dialog.mode == 'gpt':
#         await gpt_dialog(update, context)
#     else:
#         await send_text(update, context, '*Привет*')
#         await send_text(update, context, "_Как дела_")
#         await send_text(update, context, 'вы написали' + update.message.text)
#
#         await send_photo(update, context, 'avatar_main')
#         await send_text_buttons(update, context, "Запустить процесс?", {
#             "start": "Запустить",
#             'stop': "Остановить"
#         })
#
# async def hello_button(update, context):
#     query = update.callback_query.data
#     if query == 'start':
#         await send_text(update, context, "процесс запущен")
#     else:
#         await send_text(update, context, "Процесс остановлен")
#
#
# dialog = Dialog()
# dialog.mode = None
#
# chatgpt = ChatGptService(token='gpt:EG44JHCgWRZcE28XEIsgJFkblB3TKFPdeHKs9DxUsueSBurd')
#
# app = ApplicationBuilder().token(TOKEN).build()
# app.add_handler(CommandHandler('start', start))
# app.add_handler(CommandHandler('gpt', gpt))
# app.add_handler(CommandHandler('date', date))
#
# app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
#
# app.add_handler(CallbackQueryHandler(date_button, pattern='^date_.*'))
# app.add_handler(CallbackQueryHandler(hello_button))
#
# app.run_polling()

