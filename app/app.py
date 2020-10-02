import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from mongodb import DB
import os

TOKEN = os.getenv('TG_API_KEY')

db = DB('mongo')


bot = telebot.TeleBot(TOKEN)
def keyboard_gen():
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.row('1', '2','3')
    return keyboard
 
def gen_mark(cat = 0):
    mark = InlineKeyboardMarkup()
    mark.row_width = 2
    if cat == 1: 
        mark.add(InlineKeyboardButton("0", callback_data = "0"),InlineKeyboardButton("1.1", callback_data = "2"))
    elif cat == 2: 
        mark.add(InlineKeyboardButton("0", callback_data = "0"), InlineKeyboardButton("2.1", callback_data = "3"), InlineKeyboardButton("2.2", callback_data = "4"))
    else : 
        mark.add(InlineKeyboardButton("1", callback_data = "1"), InlineKeyboardButton("2", callback_data = "2"))
    return mark
 
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Хэй', reply_markup=keyboard_gen())
 
 
@bot.message_handler(content_types=['text'])
def message_handler(message):
    bot.send_message(message.chat.id, "1/2?", reply_markup=gen_mark())
 
@bot.callback_query_handler(func=lambda message: True)
def callback_query(call):
    bot.edit_message_text("Ты нажал " + call.data, call.message.chat.id, call.message.message_id, reply_markup=gen_mark(int(call.data)))

bot.polling()