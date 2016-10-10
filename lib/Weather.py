# -*- coding: UTF-8 -*-
""" Weather Module
"""

from lib import DEBUG
from lib.Config import Config
from lib.DateTime import DateTime
from lib.String import String
from lib.Web import Web

import json


class Weather(object):
    """ Weather Class
    """

    BASE_URL = "http://api.openweathermap.org/data/2.5/"
    UNITS = "imperial"
    MODE_WEATHER = 'weather'
    MODE_FORECAST = 'forecast'
    TEST_WEATHER_FILE = "./tests/weather.json"
    TEST_FORECAST_FILE = "./tests/forecast.json"

    @staticmethod
    def get_url(zip_code, mode):
        """ Get the API URL
            :param zip_code: The zip code
            :param mode: The mode
            :return: string
        """

        api_key = Config.get_config(Config.FIELD_API_KEY_WEATHER)

        url = Weather.BASE_URL + mode + \
            "?zip=" + str(zip_code) + ",us&" + \
            "&appid=" + api_key + "&" + \
            "units=" + Weather.UNITS

        return url

    @staticmethod
    def get_icon(code):
        """ Get the corresponding CSS icon

            API
            Day icon 	Night icon 	Description         Mapped to
            01d.png 	01n.png 	clear sky
            02d.png 	02n.png 	few clouds
            03d.png 	03n.png 	scattered clouds
            04d.png 	04n.png 	broken clouds
            09d.png 	09n.png 	shower rain
            10d.png 	10n.png 	rain
            11d.png 	11n.png 	thunderstorm
            13d.png 	13n.png 	snow
            50d.png 	50n.png 	mist

        :param code: The code from the API Call
        :return: string
        """

        icon_map = {
            '01d': 'flaticon-clear-sun',
            '01n': 'flaticon-crescent-moon-2',

            '02d': 'flaticon-cloudy-day',
            '02n': 'flaticon-crescent-moon-hiding-behind-a-cloud',

            '03d': 'flaticon-cloud',
            '03n': 'flaticon-cloud',

            '04d': 'flaticon-cloudy-sky',
            '04n': 'flaticon-cloudy-sky',

            '09d': 'flaticon-rain-cloud',
            '09n': 'flaticon-rain-cloud',

            '10d': 'flaticon-sun-and-rain',
            '10n': 'flaticon-rainy-cloud-at-night',

            '11n': 'flaticon-storm-cloud',
            '11d': 'flaticon-storm-cloud',

            '13n': 'flaticon-hail-cloud',
            '13d': 'flaticon-hail-cloud',

            '50n': 'flaticon-striped-cloud',
            '50d': 'flaticon-striped-cloud'
        }

        if code in icon_map:
            return icon_map[code]

        return ""

    @staticmethod
    def get_wind_direction(code):
        """ Get the wind direction
            :param code: The API Code
            :return: String
        """

        code = float(code)

        if code > 348.75 or code < 11.25:
            result = "N"
        elif code < 33.75:
            result = "NNE"
        elif code < 56.25:
            result = "NE"
        elif code < 78.75:
            result = "ENE"
        elif code < 101.25:
            result = "E"
        elif code < 123.75:
            result = "ESE"
        elif code < 146.25:
            result = "SE"
        elif code < 168.75:
            result = "SSE"
        elif code < 191.25:
            result = "S"
        elif code < 213.75:
            result = "SSW"
        elif code < 236.25:
            result = "SW"
        elif code < 258.75:
            result = "WSW"
        elif code < 281.25:
            result = "W"
        elif code < 303.75:
            result = "WNW"
        elif code < 326.25:
            result = "NW"
        else:
            result = "NNW"
        return result

    @staticmethod
    def fix_weather_data(json_data, mode=None):
        """ Fix the json data for the weather data
            :param json_data: The json data
            :param mode: None, Weather or Forecast
            :return: json data
        """

        if mode is None:
            json_data['sys']['sunrise'] = DateTime.get_hours_minutes(
                json_data['sys']['sunrise']
            )
            json_data['sys']['sunset'] = DateTime.get_hours_minutes(
                json_data['sys']['sunset']
            )

        json_data['weather'][0]['description'] = String.ucwords(
            json_data['weather'][0]['description']
        )
        json_data['weather'][0]['icon'] = Weather.get_icon(
            json_data['weather'][0]['icon']
        )
        json_data['wind']['deg'] = Weather.get_wind_direction(
            json_data['wind']['deg']
        )
        json_data['main']['temp'] = round(json_data['main']['temp'], 0)
        json_data['main']['humidity'] = round(json_data['main']['humidity'], 0)
        json_data['main']['temp_min'] = round(json_data['main']['temp_min'], 0)
        json_data['main']['temp_max'] = round(json_data['main']['temp_max'], 0)

        return json_data

    @staticmethod
    def fix_forecast_data(json_data):
        """ Fix the json data for forecast
            :param json_data: The json data
            :return: json data
        """

        forecast = {}

        for item in json_data['list']:
            Weather.fix_weather_data(item, Weather.MODE_FORECAST)
            key = str(DateTime.get_day_index(item['dt']))

            if key not in forecast:
                forecast[key] = {}
                forecast[key]['day'] = ''
                forecast[key]['icon'] = ''
                forecast[key]['temp_min'] = 999
                forecast[key]['temp_max'] = -999

            time = DateTime.get_hours_minutes(item['dt'], True)

            if time == '11:00':
                forecast[key]['icon'] = item['weather'][0]['icon']

            forecast[key]['day'] = DateTime.get_day(item['dt'])
            forecast[key]['temp_min'] = min(
                forecast[key]['temp_min'],
                item['main']['temp_min']
            )
            forecast[key]['temp_max'] = max(
                forecast[key]['temp_max'],
                item['main']['temp_max']
            )

        return forecast

    @staticmethod
    def get_current_weather(zip_code):
        """ Get the current weather
            :param zip_code: The zip code
            :return: json dict
        """

        if not DEBUG:
            Web.download(
                Weather.get_url(zip_code, Weather.MODE_WEATHER),
                Weather.TEST_WEATHER_FILE
            )

        with open(Weather.TEST_WEATHER_FILE) as filename:
            json_string = filename.read()

        json_data = Weather.fix_weather_data(json.loads(json_string))

        return json.dumps(json_data, sort_keys=True, indent=4)

    @staticmethod
    def get_forecast_weather(city_id):
        """ Get the forecast for the city
            :param city_id: The city Id
            :return: string
        """

        if not DEBUG:
            Web.download(
                Weather.get_url(city_id, Weather.MODE_FORECAST),
                Weather.TEST_FORECAST_FILE
            )

        with open(Weather.TEST_FORECAST_FILE) as filename:
            json_string = filename.read()

        json_data = Weather.fix_forecast_data(json.loads(json_string))

        return json.dumps(json_data, sort_keys=True, indent=4)
