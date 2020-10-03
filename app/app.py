import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from mongodb import DB
from bson.objectid import ObjectId
import os

TOKEN = '1196629824:AAFuIQ-lpuoIBea6FGUXJc0jxY7aqlC5h2I' #os.getenv('TG_API_KEY')
db = DB('mongo')
bot = telebot.TeleBot(TOKEN)
dialog_state = ""
current_id = None
text = ""

def gen_mark(mode = "", father = None, admin = True):
    mark = InlineKeyboardMarkup()
    mark.row_width = 2 #len(buttons)
    butt = []
    data = DB()

    if mode:
        butt = data.get_children_category_id(ObjectId(mode))
        print(data.get_children_category_id(ObjectId(mode)))
    else:
        butt = data.get_root_categories_id()

    if not(father is None) :
        mark.row(InlineKeyboardButton("Назад", callback_data = father))

    for b in butt:
        mark.row(InlineKeyboardButton(data.get_category_name(b), callback_data = b))

    #Есть админка
    if(admin):
        mark.row(InlineKeyboardButton("Изменить", callback_data = "Edit"))
    return mark

#режим редактирования

def edit_mark(state = ""):
    mark = InlineKeyboardMarkup()
    mark.row_width = 2
    if(state == "start"):
         mark.row(InlineKeyboardButton("Редактировать", callback_data = "ed"), 
            InlineKeyboardButton("Добавить", callback_data = "add"),
            InlineKeyboardButton("Удалить", callback_data = "del"),
            InlineKeyboardButton("Отмена", callback_data = "back"))

#    if state == "ed":
#        edit_b(id)
    if state == "add":
        mark.row(InlineKeyboardButton("Категорию", callback_data = "cat"), 
            InlineKeyboardButton("Пакет", callback_data = "pack"))
#    if state == "pack":

#   if state == "cat":

#    if state == "del":
#        del_b()
#    else return
    
    return mark

#def edit_b():
#def del_b():


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, я бот', reply_markup=gen_mark())
 
@bot.message_handler(func=lambda message: dialog_state == "name")
def get_name(message):
    global text
    text = message.text
    global dialog_state
    dialog_state = "desk"
    
    bot.send_message(message.chat.id, "Введи описание")

@bot.message_handler(func=lambda message: dialog_state == "desk")
def get_desk(message):
    data = DB()
    desk = message.text
    global dialog_state
    dialog_state = ""
    global text
    global current_id
    bot.send_message(message.chat.id, "Отлично")
    ch = data.add_category(name = text, description = desk, parent_id = current_id)
    current_id = ch
    strr = data.get_category_name(ch) + '\n' + data.get_category_description(ch)
    bot.send_message(message.chat.id, strr, reply_markup=gen_mark(mode))
    text = ""
#    start_message(message)
 
@bot.callback_query_handler(func=lambda message: True)
def callback_query(call):
    mode = call.data
    data = DB()
    global dialog_state
    global current_id
    if mode == "Edit":
        bot.edit_message_text("Добавить, изменить, удалить?)", call.message.chat.id, call.message.message_id, reply_markup=edit_mark("start"))
    elif mode == "ed":
        bot.edit_message_text("Изменить", call.message.chat.id, call.message.message_id, reply_markup=edit_mark("ed"))


    elif mode == "add":
        bot.edit_message_text("Добавить категорию или пакет?", call.message.chat.id, call.message.message_id, reply_markup=edit_mark("add"))
   
    elif mode == "cat":
        bot.edit_message_text("Добавление категории...", call.message.chat.id, call.message.message_id)
        dialog_state = "name"
        bot.send_message(call.message.chat.id, "Введи название категории")

  
    elif mode == "pack":
        bot.edit_message_text("Добавление пакета...", call.message.chat.id, call.message.message_id)
        dialog_state = "name"
        bot.send_message(call.message.chat.id, "Введи название пакета")



    elif mode == "del":
        bot.edit_message_text("Удалить", call.message.chat.id, call.message.message_id, reply_markup=edit_mark("del"))
    elif mode == "back":
        bot.edit_message_text("Вернуться назад)", call.message.chat.id, call.message.message_id, reply_markup=gen_mark(mode ="root"))


    else:
        strr = data.get_category_name(ObjectId(mode))+ "\n" + data.get_category_description(ObjectId(mode))
        current_id = mode
        bot.edit_message_text(strr, call.message.chat.id, call.message.message_id, reply_markup=gen_mark(mode))

bot.polling()