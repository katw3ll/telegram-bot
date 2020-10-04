import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from mongodb import DB
import os

TOKEN = '1196629824:AAFuIQ-lpuoIBea6FGUXJc0jxY7aqlC5h2I' #os.getenv('TG_API_KEY')
db = DB('mongo')
bot = telebot.TeleBot(TOKEN)

class Dialog:
    State = ""
    Name = ""
    Desk = ""
    Mod = 0 #0 edit 1 category 2 package 
    Choose = None
    def __init__(self):
        pass

admin_dialog = Dialog()

def gen_mark(mode = "", admin = True):
    mark = InlineKeyboardMarkup()
    mark.row_width = 2
    butt = []

    if mode:
        butt = db.get_children_category_id(mode)
        if admin: admin_dialog.Choose = mode
        print(db.get_children_category_id(mode))
    else:
        butt = db.get_root_categories_id()
        if admin: admin_dialog.Choose = None

    if(mode and db.get_parent_category_id(mode)):
        mark.row(InlineKeyboardButton("Назад", callback_data = db.get_parent_category_id(mode)))

    elif(mode and db.get_parent_category_id(mode) is None):
        mark.row(InlineKeyboardButton("Назад", callback_data = "root"))

    for b in butt:
        mark.row(InlineKeyboardButton(db.get_category_name(b), callback_data = b))

    #Есть админка
    if(admin):
        mark.row(InlineKeyboardButton("Изменить", callback_data = "Edit"))
    return mark

#режим редактирования
def edit_mark(state = ""):
    mark = InlineKeyboardMarkup()
    mark.row_width = 2
    if(state == "start"):
        mark.row(InlineKeyboardButton("Редактировать", callback_data = "ed")
        
        if db.is_category(admin_dialog.Choose):
            InlineKeyboardButton("Добавить", callback_data = "add")

        if admin_dialog.Choose :
            mark.row(InlineKeyboardButton("Удалить", callback_data = "del"))

        mark.row(InlineKeyboardButton("Отмена", callback_data = "back"))        

    if state == "add":
        mark.row(InlineKeyboardButton("Категорию", callback_data = "cat"), 
            InlineKeyboardButton("Пакет", callback_data = "pack"))
    
    return mark



@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Главное меню", reply_markup=gen_mark())


@bot.message_handler(func=lambda message: True)
def get_text(message):
    if(admin_dialog.State == "name"):
        admin_dialog.Name = message.text
        admin_dialog.State = "desk"
        bot.send_message(message.chat.id, "Введи описание")
    elif(admin_dialog.State == "desk"):
        admin_dialog.Desk = message.text
        ch = None
        if admin_dialog.Mod:
            ch = db.add_category(name = admin_dialog.Name, description = admin_dialog.Desk, parent_id = admin_dialog.Choose, is_category = (admin_dialog.Mod == 1))
        else:
            ch = db.update_category(name = admin_dialog.Name, description = admin_dialog.Desk, _id = admin_dialog.Choose)
        
        strr = db.get_category_name(ch) + '\n' + db.get_category_description(ch)
        bot.send_message(message.chat.id, "Отлично")
        bot.send_message(message.chat.id, strr, reply_markup=gen_mark(ch))
        admin_dialog.State = ""
 
@bot.callback_query_handler(func=lambda message: True)
def callback_query(call):
    mode = call.data
    print(mode)
    if mode == "Edit":
        bot.edit_message_text("Добавить, изменить, удалить?)", call.message.chat.id, call.message.message_id, reply_markup=edit_mark("start"))
    
    elif mode == "ed":
        bot.edit_message_text("Редактирование...", call.message.chat.id, call.message.message_id)
        admin_dialog.State = "name"
        admin_dialog.Mod = 0
        bot.send_message(call.message.chat.id, "Введи новое название")

    elif mode == "add":
        bot.edit_message_text("Добавить категорию или пакет?", call.message.chat.id, call.message.message_id, reply_markup=edit_mark("add"))
   
    elif mode == "cat":
        bot.edit_message_text("Добавление категории...", call.message.chat.id, call.message.message_id)
        admin_dialog.State = "name"
        admin_dialog.Mod = 1
        bot.send_message(call.message.chat.id, "Введи название категории")

    elif mode == "pack":
        bot.edit_message_text("Добавление пакета...", call.message.chat.id, call.message.message_id)
        admin_dialog.State = "name"
        admin_dialog.Mod = 2
        bot.send_message(call.message.chat.id, "Введи название пакета")

    elif mode == "del":
        par = db.get_parent_category_id(admin_dialog.Choose)
        if not(par is None): strr = db.get_category_name(par)+ "\n" + db.get_category_description(par)
        db.delete_category(admin_dialog.Choose)
        bot.edit_message_text(strr, call.message.chat.id, call.message.message_id, reply_markup=gen_mark(par))
        
    elif mode == "back":
        admin_dialog.State = None
        bot.edit_message_text("Вернуться назад)", call.message.chat.id, call.message.message_id, reply_markup=gen_mark(admin_dialog.Choose))

    elif str(mode) == "root" or not mode:
        bot.edit_message_text("Главное меню", call.message.chat.id, call.message.message_id, reply_markup=gen_mark())
                 
    else:
        strr = db.get_category_name(mode)+ "\n" + db.get_category_description(mode)
        bot.edit_message_text(strr, call.message.chat.id, call.message.message_id, reply_markup=gen_mark(mode))

bot.polling()