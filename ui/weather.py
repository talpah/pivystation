# coding=utf-8
import imp
from datetime import datetime

import os
from DictObject import DictObject
from babel.dates import format_timedelta
from kivy.app import App
from kivy.properties import StringProperty, Clock
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

    location_label = StringProperty()
    temperature_max_label = StringProperty()
    temperature_min_label = StringProperty()
    weathericon_source = StringProperty()
    weatherupdated_label = StringProperty()
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
        weather_data = self.weather_provider.today(place)
        self.weathericon_source = u"libs/weather/icons/{}.png".format(weather_data['icon'])
        self.location_label = u"{} astăzi: {}".format(weather_data['place'], weather_data['conditions'])
        self.temperature_max_label = u"{:.2g} ° C".format(weather_data['temperature_max'])
        self.temperature_min_label = u"{:.2g} ° C".format(weather_data['temperature_min'])


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
