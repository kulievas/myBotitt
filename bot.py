import telebot
import sqlite3
import schedule
from threading import Thread
from time import sleep

bot = telebot.TeleBot('1763661693:AAEgC41QY5FnTE6Ph6LSmQmhkqYsNjLLUIw')


def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)


def class_input(message):
    text = message.text
    if text == "11":
        try:
            sqlite_connection = sqlite3.connect('db.db')
            cursor = sqlite_connection.cursor()
            print("База данных создана и успешно подключена к SQLite")

            sqlite_select_query = f"UPDATE users SET class = '{text}' WHERE id = {message.from_user.id}"
            cursor.execute(sqlite_select_query)
            record = cursor.fetchall()
            print("Версия базы данных SQLite: ", record)
            sqlite_connection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)
        finally:
            if (sqlite_connection):
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")
        bot.send_message(message.chat.id, f"ок, {11}")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f'Я бот. Приятно познакомиться, {message.from_user.first_name}')
    try:
        sqlite_connection = sqlite3.connect('db.db')
        cursor = sqlite_connection.cursor()
        print("База данных создана и успешно подключена к SQLite")

        sqlite_select_query = f"INSERT INTO users (id, class) VALUES ({message.from_user.id}, '')"
        cursor.execute(sqlite_select_query)
        record = cursor.fetchall()
        print("Версия базы данных SQLite: ", record)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
            bot.send_message(message.from_user.id, f'Введите Ваш класс:')
            bot.register_next_step_handler(message, class_input)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет!')
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')

def send_notifications():
    try:
        sqlite_connection = sqlite3.connect('db.db')
        cursor = sqlite_connection.cursor()
        print("База данных создана и успешно подключена к SQLite")
