from datetime import datetime
from pprint import pprint

import pyowm


class Weather(object):
    api_object = None
    weather_data = {}
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
            self.weather_data[place] = self.api_object.weather_at_place(place).get_weather()
            self.update_stamps[place] = datetime.now()
            pprint(self.weather_data[place].to_JSON())

    def now(self, place):
        self.refresh(place)
        wind = self.weather_data[place].get_wind()  # {'speed': 4.6, 'deg': 330}
        temperature = self.weather_data[place].get_temperature(self.config.temperature_unit)
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
            'temperature_min': temperature['temp_min'],
            'temperature_max': temperature['temp_max']
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
