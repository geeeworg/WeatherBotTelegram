#pip install pyTelegramBotAPI
#botname @GDweater_bot

import telebot
from telebot import types
import requests
import json

def number_to_emoji(number):
    return ' '.join([f'{d}\uFE0F\u20E3' for d in str(number)])

bot = telebot.TeleBot('7060898035:AAFhBE-rroyCZgEcTdxVB2C1MVTNkTPj6lM')
API_KEY = 'dda82ef907f6cae64dad2657ddc51a7f'
mode = "metric"
corf='°C'
condit = {
    "clear sky": "☀️",
    "few clouds": "🌤",
    "scattered clouds": "⛅️",
    "broken clouds": "☁️",
    "overcast clouds": "☁️",
    "shower rain": "🌧",
    "rain": "🌦",
    "thunderstorm": "🌩",
    "snow": "🌨",
    "mist": "😶‍🌫️"
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("°C", callback_data='mode1')
    button2 = types.InlineKeyboardButton("°F", callback_data='mode2')
    markup.add(button1, button2)
    bot.send_message(message.chat.id, "Welcome to our bot! Enter city name")
    bot.send_message(message.chat.id, "Please choose a mode:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('m'))
def query_handler(call):
    global mode
    global corf
    if call.data == 'mode1':
        mode = 'metric'
        corf='°C'
        bot.answer_callback_query(call.id, "Mode 1 selected")
    elif call.data == 'mode2':
        mode = 'standard'
        corf='°F'
        bot.answer_callback_query(call.id, "Mode 2 selected")
    bot.send_message(call.message.chat.id, f"Mode {mode} is now active.")
    
@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={mode}')
    if res.status_code == 200:
        data = json.loads(res.text)
        num = round(float(data["main"]["temp"]))
        description = data["weather"][0]["description"]
        
        if num>=0:
            emoji_number = number_to_emoji(num)
            bot.send_message(message.chat.id ,f'{emoji_number}{corf}')
        else:
            bot.send_message(message.chat.id ,f'➖{emoji_number}{corf}')
        if description in condit:
            bot.send_message(message.chat.id, f'{condit[description]}')
        else:
            bot.send_message(message.chat.id, f'Weather: {description.capitalize()}')
    else:
        bot.send_message(message.chat.id, "City not found or API request failed.")


bot.polling(none_stop=True)
