# coding=utf-8
import imp
from datetime import datetime

import os
from pprint import pformat

from DictObject import DictObject
from babel.dates import format_timedelta
from kivy.app import App
from kivy.properties import StringProperty, Clock, Logger
from kivy.uix.boxlayout import BoxLayout

from libs import PROJECT_PATH, MinuteScheduler


class _WP(object):
    WEATHERPROVIDER = None


class WeatherWidget(BoxLayout):
    can_remote = True

    location_label = StringProperty()
    temperature_label = StringProperty()
    temperatureminmax_label = StringProperty()
    weathericon_source = StringProperty()
    weatherupdated_label = StringProperty()
    weather_provider = None

    def __init__(self, **kwargs):
        super(WeatherWidget, self).__init__(**kwargs)

        self.app = App.get_running_app()
        dict_config = dict(self.app.config.items('weather'))
        self.weather_config = DictObject(dict_config)
        if _WP.WEATHERPROVIDER is None:
            weather_module = imp.load_source(self.weather_config.provider,
                                             os.path.join(PROJECT_PATH, 'libs', "weather",
                                                          "%s.py" % self.weather_config.provider))

            _WP.WEATHERPROVIDER = weather_module.Weather(self.weather_config)
        self.weather_provider = _WP.WEATHERPROVIDER
        self.update_weather()
        MinuteScheduler.add_callback(self.update_weather)

    def update_weather(self, *args):
        place = self.weather_config.default_place
        weather_data = self.weather_provider.now(place)
        self.weathericon_source = u"libs/weather/icons/{}.png".format(weather_data['icon'])
        self.location_label = u"{}: {}".format(weather_data['place'], weather_data['conditions'])
        self.temperature_label = u"{:.2g} ° C".format(weather_data['temperature'])
        self.temperatureminmax_label = u"{:.2g} / {:.2g}".format(weather_data['temperature_min'],
                                                                 weather_data['temperature_max'])
        last_updated = format_timedelta(self.weather_provider.update_stamps[place] - datetime.now(),
                                        granularity='minute',
                                        locale='ro_RO.utf-8',
                                        add_direction=True)
        self.weatherupdated_label = u"Actualizat {}".format(last_updated)


class ForecastWidget(BoxLayout):
    can_remote = False

    today_temperature_max_label = StringProperty()
    today_conditions_label = StringProperty()
    today_weathericon_source = StringProperty()
    tomorrow_temperature_max_label = StringProperty()
    tomorrow_conditions_label = StringProperty()
    tomorrow_weathericon_source = StringProperty()
    weather_provider = None

    def __init__(self, **kwargs):
        super(ForecastWidget, self).__init__(**kwargs)

        self.app = App.get_running_app()
        dict_config = dict(self.app.config.items('weather'))
        self.weather_config = DictObject(dict_config)
        if _WP.WEATHERPROVIDER is None:
            weather_module = imp.load_source(self.weather_config.provider,
                                             os.path.join(PROJECT_PATH, 'libs', "weather",
                                                          "%s.py" % self.weather_config.provider))

            _WP.WEATHERPROVIDER = weather_module.Weather(self.weather_config)
        self.weather_provider = _WP.WEATHERPROVIDER
        self.update_weather()

    def update_weather(self, *args):
        place = self.weather_config.default_place
        today_data = self.weather_provider.today(place)
        tomorrow_data = self.weather_provider.tomorrow(place)
        self.today_weathericon_source = u"libs/weather/icons/{}.png".format(today_data['icon'])
        self.today_temperature_max_label = u"{:.2g} ° C".format(today_data['temperature_max'])
        self.today_conditions_label = today_data['conditions']
        self.tomorrow_weathericon_source = u"libs/weather/icons/{}.png".format(tomorrow_data['icon'])
        self.tomorrow_temperature_max_label = u"{:.2g} ° C".format(tomorrow_data['temperature_max'])
        self.tomorrow_conditions_label = tomorrow_data['conditions']


class WeatherLiteWidget(BoxLayout):
    can_remote = True

    shortstatus = StringProperty()
    weather_provider = None

    def __init__(self, **kwargs):
        super(WeatherLiteWidget, self).__init__(**kwargs)

        self.app = App.get_running_app()
        dict_config = dict(self.app.config.items('weather'))
        self.weather_config = DictObject(dict_config)
        if _WP.WEATHERPROVIDER is None:
            weather_module = imp.load_source(self.weather_config.provider,
                                             os.path.join(PROJECT_PATH, 'libs', "weather",
                                                          "%s.py" % self.weather_config.provider))

            _WP.WEATHERPROVIDER = weather_module.Weather(self.weather_config)
        self.weather_provider = _WP.WEATHERPROVIDER
        self.update_weather()
        MinuteScheduler.add_callback(self.update_weather)

    def update_weather(self, *args):
        place = self.weather_config.default_place
        weather_data = self.weather_provider.now(place)
        self.shortstatus = u"{} - {:.2g} ° C - {}".format(weather_data['place'],
                                                          weather_data['temperature'],
                                                          weather_data['conditions'])
