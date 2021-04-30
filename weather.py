from requests import get
import json


def get_token():

    with open("api_token.txt") as f:
        API_TOKEN = f.read().strip()
    return API_TOKEN


def get_coord_by_city_name(name):

    url = f"http://search.maps.sputnik.ru/search/addr?q={name}&addr_limit=1"
    data = json.loads(get(url).text)
    coord = data['result']['address'][0]['features'][0]['geometry']['geometries'][0]['coordinates']
    lat = coord[1]
    lon = coord[0]
    return lat, lon


def weather_now(city):

    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}&lang={}'.format(city, get_token(),'ru')
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


def weather_for_week(city):

    lat, lon = get_coord_by_city_name(city)
    print(lat, lon)
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,hourly,minutely,alerts&appid={get_token()}&units=metric&lang={'ru'}"
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


def weather_tomorrow(city):

    lat, lon = get_coord_by_city_name(city)
    print(lat, lon)
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,hourly,minutely,alerts&appid={get_token()}&units=metric&lang={'ru'}"
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
    get_coord_by_city_name('Киев')


