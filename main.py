import telebot
import pymysql
import calendar
from telebot import types
from db import DataBase
from config import TOKEN, TOKEN_TEST
import datetime



bot = telebot.TeleBot(TOKEN)
db = DataBase('localhost', 'root', 'Morgretar2023', 'beer')
info = {}
admin = ['810885387']
data = datetime.datetime.now()
delivery_data = 0
order = []
quant = []
addresses = []
address = ""
comment = ""
del_drink = set()
write_downs = False
month = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
         'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
list_days = [str(i) for i in range(1, 13)]
select_month = 0
select_days = 0

def add_type_drink(call):
    buttons = types.InlineKeyboardMarkup()
    btn = []
    z = 1
    for i in db.get_drink(call.data):
        button = types.InlineKeyboardButton(i, callback_data=i)
        btn.append(button)
        z += 1
    buttons.add(*btn)
    bot.send_message(chat_id=call.message.chat.id, text="Выберите сорт", reply_markup=buttons)
    info['type'] = call.data

"""def del_drink(call):
    return call.message"""




@bot.message_handler(commands=["start"])
def start_message(message):
    user_id = message.from_user.id
    if user_id == int(admin[0]):
        bot.send_message(message.chat.id, "Вы верховный администратор бота")
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_drinks = types.KeyboardButton("Заказ")
    button_util = types.KeyboardButton("Списание")
    button_repair = types.KeyboardButton("Ремонт")
    button_help = types.KeyboardButton("Помощь")
    buttons.add(button_drinks, button_util, button_repair, button_help)
    bot.send_message(message.chat.id, "Добро пожаловать! Проследуй в меню, изучи, сделай заказ. Если что-то пойдет не так или потребуется помощь то ты всегда можешь написать Помощь", reply_markup=buttons)


@bot.message_handler(content_types=['text'])
def get_name_drinks(message):
    global order
    global info
    global quant
    global addresses
    global comment
    global write_downs
    global del_drink
    global delivery_data
    global data
    global select_month
    global select_days

    #user_id = message.from_user.id
    if message.text == "Заказ":
        buttons = types.InlineKeyboardMarkup()
        for i in db.get_address():
            button = types.InlineKeyboardButton(i, callback_data=i)
            buttons.add(button)
        write_downs = False
        bot.send_message(message.chat.id, "На какой адрес повезем?", reply_markup=buttons)
    elif message.text == "Заказы":
        for i in db.get_orders():
            bot.send_message(message.chat.id, f"Вывожу строку {i}")
    elif message.text == "Списание":
        buttons = types.InlineKeyboardMarkup()
        for i in db.get_type_drink():
            button = types.InlineKeyboardButton(i, callback_data=i)
            buttons.add(button)
        write_downs = True
        bot.send_message(chat_id=message.chat.id, text="Выберите категорию напитков для списания", reply_markup=buttons)
    elif message.text == "Ремонт":
        bot.send_message(message.chat.id, "Скинь фото/фотки и обязательно укажи описание!")
    elif message.text == "Помощь":
        bot.send_message(message.chat.id, "В самом конце тут будут описаны команды, особенности и способ управления ботом")
    elif message.text == "Да":
        buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_drinks = types.KeyboardButton("Добавить")
        button_comment = types.KeyboardButton("Комментарий")
        button_go = types.KeyboardButton("Подтвердить")
        buttons.add(button_drinks, button_comment, button_go)

        bot.send_message(message.chat.id, "Если требуется добавить что-либо чего нет в списке, или оставить комментарий - жми Комментарий, либо Добавить", reply_markup=buttons)
    elif message.text == "Комментарий":
        buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_drinks = types.KeyboardButton("Заказ")
        button_go = types.KeyboardButton("Отправить на доставку")
        buttons.add(button_drinks, button_go)
        bot.send_message(message.chat.id, "Напиши коммент и просто отправь его...", reply_markup=buttons)
        bot.register_next_step_handler(message, test)
    elif message.text == "Добавить":
        buttons = types.InlineKeyboardMarkup()
        for i in db.get_type_drink():
            button = types.InlineKeyboardButton(i, callback_data=i)
            buttons.add(button)
        bot.send_message(message.chat.id, text="Выберите категорию напитков", reply_markup=buttons)
    elif message.text == "Удалить":
        buttons = types.InlineKeyboardMarkup()
        for i in order:
            button = types.InlineKeyboardButton("Удалить " + i, callback_data="Удалить " + i)
            buttons.add(button)
            del_drink.add("Удалить " + i)
        bot.send_message(message.chat.id, "Выбери что удаляем, либо добавляем", reply_markup=buttons)
    elif message.text == "Подтвердить":
        b = ""
        a = 0
        for (i, q) in zip(order, quant):
            a += 1
            b += f"{a}) {i} в количестве: {q} \n"
        buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_replace = types.KeyboardButton("Удалить")
        button_add = types.KeyboardButton("Добавить")
        button_data = types.KeyboardButton("Дата доставки")
        button_comment = types.KeyboardButton("Комментарий")
        button_go = types.KeyboardButton("Отправить на доставку")
        buttons.add(button_replace, button_add, button_data, button_comment, button_go)
        bot.send_message(message.chat.id, text="Заказ принят, скоро его начнут собирать")
        bot.send_message(message.chat.id, f"<b>Вы заказали</b> \n\n{b} на адрес {address} \n\n <b>Комментарий</b> \n\n {comment} \n\n Всё верно?",
                             parse_mode='HTML', reply_markup=buttons)
    elif message.text == "Дата доставки":
        buttons = types.InlineKeyboardMarkup(row_width=4)
        btn = []
        for i in month:
            button = types.InlineKeyboardButton(i, callback_data=i)
            btn.append(button)
        buttons.add(*btn)
        bot.send_message(message.chat.id, "Выберите месяц", reply_markup=buttons)
    elif message.text == "Отправить на доставку":
        if select_days == 0 and select_month == 0:
            delivery_data = data + datetime.timedelta(days=+1)
        else:
            delivery_data = f"{select_days} {select_month} {data.year}"
            delivery_data = datetime.datetime.strptime(delivery_data, '%d %m %Y')
        b = ""
        c = 0
        a = 0
        for (i, q) in zip(order, quant):
            a += 1
            b += f"{a}) {i} в количестве: {q} \n"
            db.insert_order(address, i, q)
            db.minus_drink(i, q)
            c += 1
        buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_drinks = types.KeyboardButton("Заказ")
        button_util = types.KeyboardButton("Списание")
        button_repair = types.KeyboardButton("Ремонт")
        button_help = types.KeyboardButton("Помощь")
        buttons.add(button_drinks, button_util, button_repair, button_help)
        bot.send_message(message.chat.id, text=f"Заказ принят, скоро его начнут собирать, ожидаемая дата доставки: {delivery_data.strftime('%d.%m')} до 19:00")
        bot.send_message(admin[0], f"<b>Заказали</b> \n\n{b} на адрес {address} \n\n <b>Комментарий</b> \n\n {comment} \n\n Доставка на {delivery_data.strftime('%d.%m')}", parse_mode='HTML', reply_markup=buttons)
        order = []
        quant = []
        addresses = []
        select_month = 0
        select_days = 0
        data = datetime.datetime.now()
        delivery_data = data + datetime.timedelta(days=+1)




@bot.callback_query_handler(func=lambda call:True)
def get_drink(call):
    global address
    global write_downs
    global del_drink
    global select_month
    global select_days
    if call.data in db.get_address():
        address = call.data
        buttons = types.InlineKeyboardMarkup()
        for i in db.get_type_drink():
            button = types.InlineKeyboardButton(i, callback_data=i)
            buttons.add(button)
        if write_downs:
            bot.send_message(chat_id=call.message.chat.id, text="Выберите напиток для списания", reply_markup=buttons)
        elif not write_downs:
            bot.send_message(chat_id=call.message.chat.id, text="Выберите категорию напитков", reply_markup=buttons)
    elif call.data == "Пиво":
        add_type_drink(call)
    elif call.data == "Сидр":
        add_type_drink(call)
    elif call.data == "Лимонады":
        add_type_drink(call)
    elif call.data == "Расходники":
        add_type_drink(call)
    elif call.data in del_drink:
        drink = call.data[8:]
        key = 0
        print(drink)
        for i in order:
            if i == drink:
                del order[key]
                del quant[key]
                del_drink = set()
                break
            key += 1
    elif call.data in month:
        select_month = 0
        for i in month:
            select_month += 1
            if i == call.data:
                break
        buttons = types.InlineKeyboardMarkup(row_width=7)
        a = calendar.monthcalendar(2023, select_month)
        print(a)
        for days in a:
            btn = []
            print("")
            for day in days:
                if day == 0:
                    day = " "
                button = types.InlineKeyboardButton(day, callback_data=day)
                btn.append(button)
            buttons.add(*btn)
        bot.send_message(chat_id=call.message.chat.id, text="Выберите день", reply_markup=buttons)
    elif call.data in list_days:
        select_days = call.data
        buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_drinks = types.KeyboardButton("Добавить")
        button_comment = types.KeyboardButton("Комментарий")
        button_go = types.KeyboardButton("Подтвердить")
        buttons.add(button_drinks, button_comment, button_go)

        bot.send_message(chat_id=call.message.chat.id, text="Если требуется добавить что-либо чего нет в списке, или оставить комментарий - жми Комментарий, либо Добавить",
                         reply_markup=buttons)
    elif call.data in db.get_drink(info['type']):
        bot.send_message(chat_id=call.message.chat.id, text=f"Введите количество")
        info['drink'] = call.data
        if write_downs:
            bot.register_next_step_handler(call.message, get_write_downs)
        elif not write_downs:
            bot.register_next_step_handler(call.message, get_quantity)

def get_date(message):
    global delivery_data
    delivery_data = message.text
    bot.send_message(message.chat.id, "Дата принята")
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_add = types.KeyboardButton("Добавить")
    button_comment = types.KeyboardButton("Комментарий")
    button_go = types.KeyboardButton("Отправить на доставку")
    buttons.add(button_add, button_comment, button_go)

def get_quantity(message):
    global order
    global quant
    info['quantity'] = message.text
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_drinks = types.KeyboardButton("Добавить")
    button_comment = types.KeyboardButton("Комментарий")
    button_go = types.KeyboardButton("Подтвердить")
    buttons.add(button_drinks, button_comment, button_go)
    bot.send_message(chat_id=message.chat.id,
                     text=f"Заказано {info['drink']} в количестве {info['quantity']}",
                     reply_markup=buttons)
    order.append(f"{info['drink']}")
    quant.append(f"{info['quantity']}")

def get_write_downs(message):
    global order
    global quant
    info['quantity'] = message.text
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_drinks = types.KeyboardButton("Заказ")
    button_util = types.KeyboardButton("Списание")
    button_repair = types.KeyboardButton("Ремонт")
    button_help = types.KeyboardButton("Помощь")
    buttons.add(button_drinks, button_util, button_repair, button_help)
    bot.send_message(chat_id=message.chat.id,
                     text=f"Списываю {info['drink']} в количестве {info['quantity']} с адреса {address}, готово!",
                     reply_markup=buttons)


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    #msg = bot.send_message(message.chat.id, "Оставьте комментарий к фото")
    bot.send_photo(admin[0], message.photo[0].file_id)
    bot.send_message(admin[0], message.caption)
    bot.send_message(message.chat.id, "Добавили поломку в работу")
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_drinks = types.KeyboardButton("Заказ")
    button_util = types.KeyboardButton("Списание")
    button_repair = types.KeyboardButton("Ремонт")
    button_help = types.KeyboardButton("Помощь")
    buttons.add(button_drinks, button_util, button_repair, button_help)
    bot.send_message(message.chat.id,
                     "Проследуй в меню, изучи, сделай заказ. Если что-то пойдет не так или потребуется помощь то ты всегда можешь написать Помощь",
                     reply_markup=buttons)

def test(message):
    global comment
    comment = message.text
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_go = types.KeyboardButton("Отправить на доставку")
    buttons.add(button_go)
    bot.send_message(message.chat.id, "Жмякни на отправку",
                     reply_markup=buttons)


"""def register_repair(message):
    repair_message = bot.send_message(message.chat.id, "Добавили поломку в работу")
    bot.register_next_step_handler(msg, start_message)"""


bot.infinity_polling(none_stop=True)

'''if __name__ == '__main__':
    print_hi('PyCharm') '''
