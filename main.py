import telebot
import os
from dotenv import load_dotenv
from googletable import add_spend, add_income
from datetime import date

load_dotenv()

token_bot = os.getenv('TOKEN')
token= os.getenv('SHEED_ID')

addres_table = f"https://docs.google.com/spreadsheets/d/{token}"

bot = telebot.TeleBot(token=token_bot, parse_mode=None)

@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    bot.reply_to(message, "    Финансовый бот wety    \nДоступны комманды :\n/add - Добавить растраты или доходы\n/excel - Прислать ссылку на google таблицу\n/clear - Очистить таблицу")


@bot.message_handler(commands=['add'])
def choose(message):
    chat_id = message.chat.id
    name = message.from_user.username
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_save = telebot.types.InlineKeyboardButton(text="Расходы", callback_data="spend")
    button_change = telebot.types.InlineKeyboardButton(text="Доходы", callback_data="income")
    keyboard.add(button_save, button_change)

    bot.send_message(chat_id, f"{name}, выберете какую категорию вы хотите добавить: ", reply_markup=keyboard)


@bot.message_handler(commands=['excel'])
def choose(message):
    chat_id = message.chat.id
    name = message.from_user.username
    bot.send_message(chat_id, f"{name}, Вот ваша ссылка на доску excel: \n{addres_table}")



@bot.callback_query_handler(func=lambda call: call.data == "spend")
def choose_spend(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_save = telebot.types.InlineKeyboardButton(text="Наличные", callback_data="spend_cash")
    button_change = telebot.types.InlineKeyboardButton(text="Банк", callback_data="spend_bank")
    keyboard.add(button_save, button_change)
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Выберите способ оплаты:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "income")
def choose_income(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_save = telebot.types.InlineKeyboardButton(text="Наличные", callback_data="income_cash")
    button_change = telebot.types.InlineKeyboardButton(text="Банк", callback_data="income_bank")
    keyboard.add(button_save, button_change)
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Выберите способ получения денег:", reply_markup=keyboard)




@bot.callback_query_handler(func=lambda call: call.data == "spend_cash")
def save_spend_cash(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    msg = bot.send_message(chat_id, f"Введите 💶сумму💶 и раздел в который добавить трату\nПример: 1000, продукты🍔")
    bot.register_next_step_handler(msg, add_spend_cash)


@bot.callback_query_handler(func=lambda call: call.data == "spend_bank")
def save_spend_bank(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    msg = bot.send_message(chat_id, f"Введите 💶сумму💶 и раздел в который добавить трату\nПример: 1000, продукты🍔")
    bot.register_next_step_handler(msg, add_spend_bank)


@bot.callback_query_handler(func=lambda call: call.data == "income_bank")
def save_income_bank(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    msg = bot.send_message(chat_id, f"Введите сумму и раздел в который добавить доход\nПример: 50000, зарплата💶")
    bot.register_next_step_handler(msg, add_income_bank)


@bot.callback_query_handler(func=lambda call: call.data == "income_cash")
def save_income_cash(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    msg = bot.send_message(chat_id, f"Введите сумму и раздел в который добавить доход\nПример: 50000, зарплата💶")
    bot.register_next_step_handler(msg, add_income_cash)

"""

ФУНКЦИИ ДОБАВЛЕНИЯ В ГУГЛ ТАБЛИЦУ

"""

def add_spend_cash(message):
    text = message.text
    list_spend = list(text.replace(" ", "").split(","))
    time12 = str(date.today())
    if len(list_spend) == 2:
        add_spend("Наличная оплата", list_spend[0], list_spend[1], time12, "May")
    elif len(list_spend) == 1:
        add_spend("Наличная оплата", list_spend[0], "()()()()()", time12, "May")
    else:
        chat_id = message.chat.id
        bot.send_message(chat_id, f"Херово сделал, переделывай")
        return
    chat_id = message.chat.id
    bot.send_message(chat_id, f"Успешно добавлено!")

def add_spend_bank(message):
    text = message.text
    list_spend = list(text.replace(" ", "").split(","))
    time12 = str(date.today())
    if len(list_spend) == 2:
        add_spend("Банковская карта", list_spend[0], list_spend[1], time12, "May")
    elif len(list_spend) == 1:
        add_spend("Банковская карта", list_spend[0], "()()()()()", time12, "May")
    else:
        chat_id = message.chat.id
        bot.send_message(chat_id, f"Херово сделал, переделывай")
        return
    chat_id = message.chat.id
    bot.send_message(chat_id, f"Успешно добавлено!")



def add_income_cash(message):
    text = message.text
    list_spend = list(text.replace(" ", "").split(","))
    time12 = str(date.today())
    if len(list_spend) == 2:
        add_income("Наличная оплата", list_spend[0], list_spend[1], time12, "May")
    elif len(list_spend) == 1:
        add_income("Наличная оплата", list_spend[0], "()()()()()", time12, "May")
    else:
        chat_id = message.chat.id
        bot.send_message(chat_id, f"Херово сделал, переделывай")
        return
    chat_id = message.chat.id
    bot.send_message(chat_id, f"Успешно добавлено!")

def add_income_bank(message):
    text = message.text
    list_spend = list(text.replace(" ", "").split(","))
    time12 = str(date.today())
    if len(list_spend) == 2:
        add_income("Банковская карта", list_spend[0], list_spend[1], time12, "May")
    elif len(list_spend) == 1:
        add_income("Банковская карта", list_spend[0], "()()()()()", time12, "May")
    else:
        chat_id = message.chat.id
        bot.send_message(chat_id, f"Херово сделал, переделывай")
        return
    chat_id = message.chat.id
    bot.send_message(chat_id, f"Успешно добавлено!")




bot.infinity_polling()