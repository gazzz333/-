import telebot
import requests
import json
from translate import Translator

bot = telebot.TeleBot('7523461368:AAFX1U5Jo2AWiyTP1hIgoUWq4FBI8UKKBx0')
API = '60a2f30cb8d1c2feab6faf5b3db8d2c8'
translator = Translator(to_lang="ru")

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Привет напиши город, погоду которого ты бы хотел узнать')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        hum = data["main"]["humidity"]
        des = data["weather"][0]["description"]

        des_ru = translator.translate(des)

        bot.reply_to(message, f'Сейчас: {temp:.0f}°C Влажность: {hum}% Описание: {des_ru}')
    else:
        bot.reply_to(message, 'Указанный город не найден')
        
bot.polling(none_stop=True)