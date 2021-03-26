import telebot
import sqlite3
import schedule
from threading import Thread
from time import sleep
from datetime import datetime
import random

bot = telebot.TeleBot('1763661693:AAEgC41QY5FnTE6Ph6LSmQmhkqYsNjLLUIw')

start_lessons_times_1minute = ["08:14", "09:14", "10:19", "11:19", "12:19", "13:19", "14:19"]
start_lessons_times_5minutes = ["08:10", "09:10", "10:15", "11:15", "12:15", "13:15", "14:15"]
start_lessons_times_in_time = ["08:15", "09:15", "10:20", "11:20", "12:20", "13:20", "14:20"]
start_lessons_times_end = ["09:00", "10:00", "11:05", "12:05", "13:05", "14:05", "15:05"]


def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)


def class_input(message):
    print('Start class_input')
    text = message.text
    try:
        sqlite_connection = sqlite3.connect('db.db')
        cursor = sqlite_connection.cursor()
        print("База данных создана и успешно подключена к SQLite")

        sqlite_select_query = f"UPDATE users SET class = '{text}' WHERE id = {message.from_user.id}"
        cursor.execute(sqlite_select_query)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
    bot.send_message(message.chat.id, f"Ок, {text}")
    bot.send_message(message.from_user.id,
                     f'Когда вы хотите получать уведомления?\n1. За минуту до начала урока\n'
                     f'2. За 5 минут до начала урока\n3. Во время начала урока\n4. По окончанию урока'
                     f'\n(введите цифру от 1 до 4 ; эту настройку всегда можно поменять командой /time)')
    bot.register_next_step_handler(message, notifications_type_input)


@bot.message_handler(commands=['/time'])  # комманда /time будет менять время уведомлений юзера
def notifications_type_input(message):
    print('Start notifications_type_input')
    text = message.text
    try:
        sqlite_connection = sqlite3.connect('db.db')
        cursor = sqlite_connection.cursor()
        print("База данных создана и успешно подключена к SQLite")

        sqlite_select_query = f"UPDATE users SET notifications_type = {int(text)} WHERE id = {message.from_user.id}"
        cursor.execute(sqlite_select_query)
        sqlite_connection.commit()
        cursor.close()
        bot.send_message(message.chat.id, f"Настройка сохранена")

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    print('Start send_welcome')
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


def random_notification(user_class, notifications_type):
    if notifications_type != 4:
        notification_number = random.randint(1, 5)
        if notification_number == 1:
            return f'Скоро у Вас урок у {user_class}!'
        if notification_number == 2:
            return f'Сейчас начнётся урок у {user_class}'
        if notification_number == 3:
            return f'Скоро Вам предстоит встретиться с Вашим {user_class})'
        if notification_number == 4:
            return f'Вот-вот к Вам придёт {user_class}'
        if notification_number == 5:
            return f'Ваш {user_class} уже мчится к вам!'
    return f'Урок закончился)'


def send_notifications():
    try:
        sqlite_connection = sqlite3.connect('db.db')
        cursor = sqlite_connection.cursor()
        print("База данных создана и успешно подключена к SQLite")

        sqlite_select_query = f"SELECT * FROM users"
        cursor.execute(sqlite_select_query)
        record = cursor.fetchall()
        print("Результат SQLite: ", record)
        current_notifications_type = 1
        time_now = datetime.now().strftime("%H:%M")
        if time_now in start_lessons_times_1minute:
            current_notifications_type = 1
        elif time_now in start_lessons_times_5minutes:
            current_notifications_type = 2
        elif time_now in start_lessons_times_in_time:
            current_notifications_type = 3
        elif time_now in start_lessons_times_end:
            current_notifications_type = 4
        for user in record:
            user_id = user[0]
            user_class = user[1]
            user_notifications_type = user[2]
            if user_notifications_type == current_notifications_type:
                bot.send_message(user_id, random_notification(user_class, current_notifications_type))

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


for lesson_time in (
        start_lessons_times_1minute + start_lessons_times_5minutes +
        start_lessons_times_in_time + start_lessons_times_end):
    schedule.every().monday.at(lesson_time).do(send_notifications)
    schedule.every().tuesday.at(lesson_time).do(send_notifications)
    schedule.every().wednesday.at(lesson_time).do(send_notifications)
    schedule.every().thursday.at(lesson_time).do(send_notifications)
    schedule.every().friday.at(lesson_time).do(send_notifications)

Thread(target=schedule_checker).start()
bot.polling(none_stop=True)
