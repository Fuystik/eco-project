import telebot
from telebot import types

API_TOKEN = 'токен'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет, я телеграм-бот!")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Обработка фотографии
    bot.send_message(message.chat.id, "Спасибо за изображение!")


#создание клавиатуры
@bot.message_handler(commands=['keyboard'])
def handle_keyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("Нажми меня")
    markup.add(item)

    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)

#обработка данных клавиатуры
@bot.message_handler(func=lambda message: message.text == "Нажми меня")
def handle_key(message):
    bot.send_message(message.chat.id, "Кирюша лучший бро)")

bot.polling()
