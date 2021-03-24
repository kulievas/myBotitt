import telebot
bot = telebot.TeleBot('1795222844:AAET9vjVQPWr4QeZtP1IEkZXTMxoMzVZNlU')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f'Я бот. Приятно познакомиться, {message.from_user.first_name}')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет!')
    else:
        bot.send_message(message.from_user.id, 'Я не понимаю что это значит.')

bot.polling(none_stop=True)
