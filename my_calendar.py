import calendar
import datetime
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
import telebot
import pymysql
import calendar
from telebot import types
from db import DataBase
from config import TOKEN, TOKEN_TEST
import datetime



bot = telebot.TeleBot(TOKEN)

from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
@bot.message_handler(commands=['calendar'])
def get_month(message):
    pass


@bot.callback_query_handler(func=lambda call:True)
def set_date(call):
    pass


"""@bot.message_handler(commands=['start'])
def start(message):
    a = calendar.monthrange(2023, 4)
    bot.send_message(message.chat.id, a)"""

bot.infinity_polling()