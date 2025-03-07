import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
from threading import Thread

# Токен бота
TOKEN = "7636942221:AAGe4vJVbtQB-jCeo1iSFq_CZBRMt9iI0jc"
bot = telebot.TeleBot(TOKEN)

# ID психолога
PSYCHOLOGIST_ID = 974207794  

# Словарь для хранения номеров телефонов пользователей
user_contacts = {}

# Ключевые слова
keywords = [
    'буллинг', 'буллят', 'рэкит', 'бьют', 'избивают', 'пинают', 'матерят', 
    'деньги просят', 'налог', 'угроза', 'побои', 'оскорбления', 'угрожают'
]

# Главное меню
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = KeyboardButton("📢 Сообщить о рэкете")
    item2 = KeyboardButton("💬 Чат с психологом")
    item3 = KeyboardButton("🚨 SOS (экстренная помощь)")
    item4 = KeyboardButton("📞 Отправить номер", request_contact=True)  # Кнопка для номера
    item5 = KeyboardButton("❓ Помощь")
    markup.add(item1, item2, item3, item4, item5)
    return markup

# Старт
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я помогу тебе защититься от рэкета. Выбери действие:", reply_markup=main_menu())

# Обработка номера телефона
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    if message.contact is not None:
        phone_number = message.contact.phone_number
        user_id = message.chat.id
        user_contacts[user_id] = phone_number  # Сохраняем номер пользователя

        bot.reply_to(message, f"Спасибо! Мы получили твой номер: {phone_number}. В ближайшее время с тобой свяжется психолог.")
        bot.send_message(PSYCHOLOGIST_ID, f"📞 Пользователь {user_id} отправил номер телефона: {phone_number}")

# Обработка кнопки "📢 Сообщить о рэкете"
@bot.message_handler(func=lambda message: message.text == "📢 Сообщить о рэкете")
def report_reket(message):
    user_id = message.chat.id
    phone_number = user_contacts.get(user_id, "Не указан")

    bot.reply_to(message, "Опиши ситуацию, и мы постараемся помочь. Ты можешь сообщить о рэкете анонимно.")
    bot.send_message(PSYCHOLOGIST_ID, f"🚨 Жалоба на рэкет от пользователя {user_id}\n📞 Телефон: {phone_number}")

# Обработка кнопки "💬 Чат с психологом"
@bot.message_handler(func=lambda message: message.text == "💬 Чат с психологом")
def chat_psychologist(message):
    user_id = message.chat.id
    phone_number = user_contacts.get(user_id, "Не указан")

    bot.reply_to(message, "Наш психолог скоро свяжется с тобой. Опиши свою проблему, и мы передадим информацию психологу.")
    bot.send_message(PSYCHOLOGIST_ID, f"💬 Новый запрос от пользователя {user_id}\n📞 Телефон: {phone_number}\nТекст: {message.text}")

# Кнопка "SOS"
@bot.message_handler(func=lambda message: message.text == "🚨 SOS (экстренная помощь)")
def sos(message):
    user_id = message.chat.id
    phone_number = user_contacts.get(user_id, "Не указан")

    bot.reply_to(message, "⚠️ Тревожный сигнал отправлен! В ближайшее время с тобой свяжется специалист.")
    bot.send_message(PSYCHOLOGIST_ID, f"⚠️ SOS-сигнал от пользователя {user_id}\n📞 Телефон: {phone_number}")

# Обнаружение угроз
@bot.message_handler(func=lambda message: any(keyword in message.text.lower() for keyword in keywords))
def respond_to_abuse(message):
    user_id = message.chat.id
    phone_number = user_contacts.get(user_id, "Не указан")

    bot.reply_to(message, "Мне очень жаль, что ты переживаешь такие вещи. Помощь доступна, ты не один.")
    bot.send_message(PSYCHOLOGIST_ID, f"⚠️ Жалоба от пользователя {user_id}\n📞 Телефон: {phone_number}\nТекст: {message.text}")

# Обработка кнопки "❓ Помощь"
@bot.message_handler(func=lambda message: message.text == "❓ Помощь")
def help_message(message):
    bot.reply_to(message, "Если ты столкнулся с проблемой рэкета, угрозами или насилием, выбери одну из опций в меню:\n\n"
                          "📢 Сообщить о рэкете\n"
                          "💬 Чат с психологом\n"
                          "🚨 SOS (экстренная помощь)\n\n"
                          "Также ты можешь отправить свой номер телефона, чтобы с
обы с тобой мог связаться специалист.")

# Обработка всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def default_response(message):
    bot.reply_to(message, "Я тебя не совсем понял. Выбери одну из опций в меню.")

# Запуск бота
bot.polling(none_stop=True)

# Flask-сервер для поддержания активности бота
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
from threading import Thread

# Токен бота
TOKEN = "7636942221:AAGe4vJVbtQB-jCeo1iSFq_CZBRMt9iI0jc"
bot = telebot.TeleBot(TOKEN)

# ID психолога
PSYCHOLOGIST_ID = 974207794  

# Словарь для хранения номеров телефонов пользователей
user_contacts = {}

# Ключевые слова
keywords = [
    'буллинг', 'буллят', 'рэкит', 'бьют', 'избивают', 'пинают', 'матерят', 
    'деньги просят', 'налог', 'угроза', 'побои', 'оскорбления', 'угрожают'
]

# Главное меню
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = KeyboardButton("📢 Сообщить о рэкете")
    item2 = KeyboardButton("💬 Чат с психологом")
    item3 = KeyboardButton("🚨 SOS (экстренная помощь)")
    item4 = KeyboardButton("📞 Отправить номер", request_contact=True)  # Кнопка для номера
    item5 = KeyboardButton("❓ Помощь")
    markup.add(item1, item2, item3, item4, item5)
    return markup

# Старт
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я помогу тебе защититься от рэкета. Выбери действие:", reply_markup=main_menu())

# Обработка номера телефона
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    if message.contact is not None:
        phone_number = message.contact.phone_number
        user_id = message.chat.id
        user_contacts[user_id] = phone_number  # Сохраняем номер пользователя

        bot.reply_to(message, f"Спасибо! Мы получили твой номер: {phone_number}. В ближайшее время с тобой свяжется психолог.")
        bot.send_message(PSYCHOLOGIST_ID, f"📞 Пользователь {user_id} отправил номер телефона: {phone_number}")

# Обработка кнопки "📢 Сообщить о рэкете"
@bot.message_handler(func=lambda message: message.text == "📢 Сообщить о рэкете")
def report_reket(message):
    user_id = message.chat.id
    phone_number = user_contacts.get(user_id, "Не указан")

    bot.reply_to(message, "Опиши ситуацию, и мы постараемся помочь. Ты можешь сообщить о рэкете анонимно.")
    bot.send_message(PSYCHOLOGIST_ID, f"🚨 Жалоба на рэкет от пользователя {user_id}\n📞 Телефон: {phone_number}")

# Обработка кнопки "💬 Чат с психологом"
@bot.message_handler(func=lambda message: message.text == "💬 Чат с психологом")
def chat_psychologist(message):
    user_id = message.chat.id
    phone_number = user_contacts.get(user_id, "Не указан")

    bot.reply_to(message, "Наш психолог скоро свяжется с тобой. Опиши свою проблему, и мы передадим информацию психологу.")
    bot.send_message(PSYCHOLOGIST_ID, f"💬 Новый запрос от пользователя {user_id}\n📞 Телефон: {phone_number}\nТекст: {message.text}")

# Кнопка "SOS"
@bot.message_handler(func=lambda message: message.text == "🚨 SOS (экстренная помощь)")
def sos(message):
    user_id = message.chat.id
    phone_number = user_contacts.get(user_id, "Не указан")

    bot.reply_to(message, "⚠️ Тревожный сигнал отправлен! В ближайшее время с тобой свяжется специалист.")
    bot.send_message(PSYCHOLOGIST_ID, f"⚠️ SOS-сигнал от пользователя {user_id}\n📞 Телефон: {phone_number}")

# Обнаружение угроз
@bot.message_handler(func=lambda message: any(keyword in message.text.lower() for keyword in keywords))
def respond_to_abuse(message):
    user_id = message.chat.id
    phone_number = user_contacts.get(user_id, "Не указан")

    bot.reply_to(message, "Мне очень жаль, что ты переживаешь такие вещи. Помощь доступна, ты не один.")
    bot.send_message(PSYCHOLOGIST_ID, f"⚠️ Жалоба от пользователя {user_id}\n📞 Телефон: {phon
e_number}\nТекст: {message.text}")

# Обработка кнопки "❓ Помощь"
@bot.message_handler(func=lambda message: message.text == "❓ Помощь")
def help_message(message):
    bot.reply_to(message, "Если ты столкнулся с проблемой рэкета, угрозами или насилием, выбери одну из опций в меню:\n\n"
                          "📢 Сообщить о рэкете\n"
                          "💬 Чат с психологом\n"
                          "🚨 SOS (экстренная помощь)\n\n"
                          "Также ты можешь отправить свой номер телефона, чтобы с тобой мог связаться специалист.")

# Обработка всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def default_response(message):
    bot.reply_to(message, "Я тебя не совсем понял. Выбери одну из опций в меню.")

# Запуск бота
def bot_polling():
    bot.polling(none_stop=True)

# Flask-сервер для поддержания активности бота
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает!"

def run():
    app.run(host="0.0.0.0", port=8080)

# Функция, которая запускает Flask и поддерживает работу бота
def keep_alive():
    t1 = Thread(target=run)
    t2 = Thread(target=bot_polling)
    t1.start()
    t2.start()

keep_alive()
