from datetime import datetime

import pyowm
from kivy import Logger
from pyowm.exceptions.api_call_error import APICallError


class Weather(object):
    api_object = None
    weather_data = {}
    forecast_data = {}
    update_stamps = {}
    update_interval = 1800  # seconds

    def __init__(self, config):
        self.config = config
        self.api_object = pyowm.OWM(config.api_key, language=config.language)

    def refresh(self, place):
        last_updated = now = datetime.now()
        place_cache = self.weather_data.get(place, {})
        if place in self.update_stamps:
            last_updated = self.update_stamps[place]
        if not place_cache or (now - last_updated).total_seconds() >= self.update_interval:
            try:
                self.weather_data[place] = self.api_object.weather_at_place(place).get_weather()
                self.forecast_data[place] = self.api_object.daily_forecast(place).get_weather_at(now)
                self.update_stamps[place] = datetime.now()
            except APICallError as e:
                self.update_stamps[place] = datetime.now()
                Logger.error('WEATHER: Failed to get data: {}'.format(e))
                return False
        return True

    def now(self, place):
        if not self.refresh(place):
            return {
                'place': place,
                'conditions': 'EROARE',
                'icon': '01d',
                'wind': '-',
                'humidity': '',  # 87
                'temperature': 0,
                'temperature_min': 0,
                'temperature_max': 0
            }
        wind = self.weather_data[place].get_wind()  # {'speed': 4.6, 'deg': 330}
        temperature = self.weather_data[place].get_temperature(self.config.temperature_unit)
        temperature_today = self.forecast_data[place].get_temperature(self.config.temperature_unit)
        # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
        conditions = self.weather_data[place].get_detailed_status()
        icon = self.weather_data[place].get_weather_icon_name()

        response = {
            'place': place,
            'conditions': conditions,
            'icon': icon,
            'wind': self._convert_speed_from_mps(wind['speed'], self.config.wind_speed_unit),
            'humidity': self.weather_data[place].get_humidity(),  # 87
            'temperature': temperature['temp'],
            'temperature_min': temperature_today['min'],
            'temperature_max': temperature_today['max']
        }
        return response

    def tomorrow(self):
        pass

    def today(self):
        pass

    def _convert_speed_from_mps(self, speed, unit):
        if unit == 'kph':
            return 3.6 * speed
        return speed
