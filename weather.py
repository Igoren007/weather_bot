from requests import get
import json
from datetime import datetime

API_TOKEN = 'fbe9d08222fbe4a986f4926ac4c316d0'
city = 'Rome,it'


def weather_now(city):

    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}&lang={}'.format(city, API_TOKEN,'ru')
    data = json.loads(get(url).text)
    sky = data['weather'][0]['description']
    temt_now = data['main']['temp']
    pressure = data['main']['pressure']*0.75
    wind_speed = data['wind']['speed']
    weather = {
        'sky': sky,
        'temp_now': temt_now,
        'pressure': pressure,
        'wind_speed': wind_speed
    }
    return weather


def weather_for_week():

    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={47.9957}&lon={37.7903}&exclude=current,hourly,minutely,alerts&appid={API_TOKEN}&units=metric&lang={'ru'}"
    data = json.loads(get(url).text)
    week_forecast = []
    for i in range(0, 7):
        data_item = data['daily'][i]
        daily_forecast = {
            'date': data_item['dt'],
            'temp_day': data_item['temp']['day'],
            'temp_night': data_item['temp']['night'],
            'wind_speed': data_item['wind_speed'],
            'wind_deg': data_item['wind_deg'],
            'sky': data_item['weather'][0]['description'],
            'pressure': data_item['pressure']*0.75,
        }
        week_forecast.append(daily_forecast)
    return week_forecast


def weather_tomorrow():

    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={47.9957}&lon={37.7903}&exclude=current,hourly,minutely,alerts&appid={API_TOKEN}&units=metric&lang={'ru'}"
    data = json.loads(get(url).text)
    tomorrow_forecast = {
        'temp_day': data['daily'][1]['temp']['day'],
        'temp_night': data['daily'][1]['temp']['night'],
        'wind_speed': data['daily'][1]['wind_speed'],
        'wind_deg': data['daily'][1]['wind_deg'],
        'sky': data['daily'][1]['weather'][0]['description'],
        'pressure': data['daily'][1]['pressure'] * 0.75,
    }
    return tomorrow_forecast



if __name__ == '__main__':
    weather_now(city)
    weather_for_week()
    weather_tomorrow()

