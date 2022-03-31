import json
import random
import db_holder

import pandas as pd
import requests
import telebot

bot = telebot.TeleBot('token')


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        'Greetings! I can show you Weather Bot.\n' +
        'To get info about the author /author.\n' +
        'To get cities list /facts.\n' +
        'To get forcast about a city type its name like: Moscow.\n'
    )


@bot.message_handler(commands=["facts"])
def start(message):
    factsList = db_holder.returnData()
    comp_string = factsList[random.randint(0, len(factsList))]
    new_string = ''.join([i for i in comp_string if not i.isdigit()])
    bot.send_message(message.chat.id, new_string)


@bot.message_handler(commands=["author"])
def authorCommand(message):
    bot.send_message(message.chat.id, '\U0001F609')
    bot.send_message(parse_mode='HTML', chat_id=message.chat.id, text='<b>The author of this Bot is Horoshko '
                                                                      'Olena-Ivanna</b> \n ')


@bot.message_handler(content_types=["text"])
def handle_text(message):
    celsiusBreak = "\u00b0C\n"

    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=token".format(
                city_name=message.text))
        if response.status_code == 200:
            d = json.loads(response.text)

            img = d["weather"][0]["icon"]
            main = d["weather"][0]["main"]
            temp = "Температура: " + str(kelvinToCelsius(d["main"]["temp"])) + celsiusBreak
            feelsLike = "Ощущается как: " + str(kelvinToCelsius(d["main"]["feels_like"])) + celsiusBreak
            lowest = "Нижняя точка: " + str(kelvinToCelsius(d["main"]["temp_min"])) + celsiusBreak
            highest = "Верхняя точка: " + str(kelvinToCelsius(d["main"]["temp_max"])) + celsiusBreak
            sunrise = "Восход" + str(getTime(d["sys"]["sunrise"])) + "\n"
            sunset = "Закат" + str(getTime(d["sys"]["sunset"])) + "\n"

            bot.send_photo(message.chat.id, f"http://openweathermap.org/img/w/{img}.png")
            currentStatus = "<b>" + main + "</b>" + "\n" + \
                            temp + \
                            feelsLike + lowest + highest + \
                            sunrise + sunset

            bot.send_message(parse_mode='HTML', chat_id=message.chat.id, text=currentStatus)
        else:
            handleException(message)
    except requests.exceptions.Timeout:
        handleException(message)
    except requests.exceptions.TooManyRedirects:
        handleException(message)
    except requests.exceptions.RequestException as e:
        handleException(message)






def handleException(message):
    bot.send_photo(message.chat.id,
                   "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSjjoJ0G5uM6SvT9IaTjEo-qIsSKH4tQy8hvFn2KJ40UAXIjP6OQwnXpstX3gv4Se9YYfM&usqp=CAU")
    bot.send_message(message.chat.id, "Попробуйте ещё раз")


def kelvinToCelsius(kelvin):
    return round(kelvin - 273.15, 2)


def getTime(milliseconds):
    return pd.to_datetime(milliseconds, unit='ms').to_pydatetime()


bot.polling(none_stop=True, interval=0)
