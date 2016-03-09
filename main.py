#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import
from __future__ import print_function

import imp
import time
from collections import deque
from datetime import datetime

import locale
import os
from DictObject import DictObject
from babel.dates import format_timedelta
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.properties import StringProperty, ListProperty, Clock, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

from libs.LabelB import LabelB
from libs.timer import Timer

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))

locale.setlocale(locale.LC_ALL, 'ro_RO.utf8')


class KeyHandler(object):
    _callbacks = {}

    def __init__(self, target):
        self._keyboard = Window.request_keyboard(self.keyboard_closed, target)
        self._keyboard.bind(on_key_down=self.on_keyboard_down)

    def keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_keyboard_down)
        self._keyboard = None

    def bind(self, key, callback):
        if key not in self._callbacks:
            self._callbacks[key] = []
        self._callbacks[key].append(callback)

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        key = keycode[1]  # Textual representation of key
        if key in self._callbacks:
            for cb in self._callbacks[key]:
                cb(key)
            return True
        return False


class NewsWidget(Label):
    news_items = StringProperty()
    news_rotation_paused = False
    news_rotation_manual_update = datetime.now()

    def __init__(self, **kwargs):
        super(NewsWidget, self).__init__(**kwargs)
        self.app = App.get_running_app()
        app_config = self.app.config
        provider = app_config.get('news', 'provider')
        news_module = imp.load_source(provider,
                                      os.path.join(PROJECT_PATH, 'libs', "news", "%s.py" % provider))
        self.news_provider = news_module.News()
        Clock.schedule_interval(self.update_news, 600)
        Clock.schedule_interval(self.rotate_news, app_config.getint('news', 'cycle_interval'))
        self.update_news()
        self.key_handler = self.app.key_handler
        self.key_handler.bind('down', lambda *args: self.rotate_news(direction='next', manual=True))
        self.key_handler.bind('up', lambda *args: self.rotate_news(direction='prev', manual=True))

    def update_news(self, *args):
        self.news_provider.update()
        self.rotate_news()

    def rotate_news(self, *args, **kwargs):
        if self.news_rotation_paused and 'manual' not in kwargs:
            if (datetime.now() - self.news_rotation_manual_update).total_seconds() > 30:
                self.news_rotation_paused = False
            else:
                return
        if 'direction' not in kwargs or kwargs.get('direction') == 'next':
            self.news_items = self.news_provider.get_next_article()
        else:
            self.news_items = self.news_provider.get_prev_article()
        if 'manual' in kwargs:
            self.news_rotation_manual_update = datetime.now()
            self.news_rotation_paused = True


class ClockWidget(BoxLayout):
    orientation = 'vertical'

    date_text = StringProperty()
    clock_text = StringProperty()

    def __init__(self, **kwargs):
        super(ClockWidget, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_clock, 1)

        self.update_clock()

    def update_clock(self, *args):
        self.clock_text = time.strftime("%H:%M:%S")
        self.update_date()

    def update_date(self, *args):
        self.date_text = time.strftime("%A, %d %B %Y")


class TimerWidget(LabelB):
    timer_text = StringProperty()
    timer_color = ListProperty()
    timer_bgcolor = ListProperty()
    alarm_odd = False

    def __init__(self, **kwargs):
        super(TimerWidget, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.timer_provider = Timer()
        self.alarmsound = SoundLoader.load(os.path.join(PROJECT_PATH, 'libs', 'timer', 'beep.wav'))

        for key in Timer.number_keys:
            self.app.key_handler.bind(key, self.timer_provider.key)
        for key in Timer.terminator_keys:
            self.app.key_handler.bind(key, self.timer_provider.done)
        for key in Timer.reset_keys:
            self.app.key_handler.bind(key, self.timer_provider.reset)

        Clock.schedule_interval(self.update_timer, 0.5)
        Clock.schedule_interval(self.timer_provider.countdown, 1)

    def update_timer(self, *args):
        self.timer_text = str(self.timer_provider)
        if self.timer_provider.is_alarmed:
            if self.alarm_odd:
                self.timer_color = [1, 0, 0, 1]
                self.timer_bgcolor = [0, 0, 0, 1]
            else:
                self.timer_color = [0, 0, 0, 1]
                self.timer_bgcolor = [1, 0, 0, 1]
            self.alarm_odd = not self.alarm_odd
            self.alarmsound.play()
        else:
            self.timer_color = [0.529, 0.808, 0.922, 1]
            self.timer_bgcolor = [0, 0, 0, 1]


class WeatherWidget(BoxLayout):
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
        weather_module = imp.load_source(self.weather_config.provider,
                                         os.path.join(PROJECT_PATH, 'libs', "weather",
                                                      "%s.py" % self.weather_config.provider))

        self.weather_provider = weather_module.Weather(self.weather_config)
        self.update_weather()
        Clock.schedule_interval(self.update_weather, 60)

    def update_weather(self, *args):
        place = self.weather_config.default_place
        weather_data = self.weather_provider.now(place)
        self.weathericon_source = u"libs/weather/icons/{}.png".format(weather_data['icon'])
        self.location_label = u"{} - {}".format(weather_data['place'], weather_data['conditions'])
        self.temperature_label = u"{:.2g} ° C".format(weather_data['temperature'])
        self.temperatureminmax_label = u"{:.2g} / {:.2g}".format(weather_data['temperature_min'],
                                                                 weather_data['temperature_max'])
        last_updated = format_timedelta(self.weather_provider.update_stamps[place] - datetime.now(),
                                        granularity='minute',
                                        locale='ro_RO.utf-8',
                                        add_direction=True)
        self.weatherupdated_label = u"Actualizat {}".format(last_updated)


class MainScreen(Screen):
    key_handler = ObjectProperty()

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.key_handler = kwargs['key_handler']


class ForecastScreen(Screen):
    pass


class MainApp(App):
    screens = deque()
    screen_manager = ScreenManager()
    key_handler = None

    def _key_right(self, *args):
        self.screens.rotate(1)
        self.screen_manager.transition.direction = 'left'
        self.screen_manager.current = self.screens[0]

    def _key_left(self, *args):
        self.screens.rotate(-1)
        self.screen_manager.transition.direction = 'right'
        self.screen_manager.current = self.screens[0]

    def build_config(self, config):
        config.setdefaults('news', {'cycle_interval': 15, 'provider': 'mediafax'})
        config.setdefaults('weather', {'temperature_unit_display': 'C', 'language': 'ro', 'temperature_unit': 'celsius',
                                       'provider': 'openweathermap', 'api_key': '1a6b3c983f34975e1634037a882c365a',
                                       'wind_speed_unit': 'kph', 'default_place': 'Bucuresti',
                                       'wind_speed_unit_display': 'km/h'})

    def build(self):
        screens = [
            ('main', MainScreen),
            ('forecast', ForecastScreen)
        ]
        keys = [
            ('q', self.stop),
            ('right', self._key_right),
            ('left', self._key_left)
        ]
        self.key_handler = KeyHandler(self.screen_manager)

        for screen in screens:
            self.screen_manager.add_widget(screen[1](name=screen[0], key_handler=self.key_handler))
            self.screens.append(screen[0])

        for key in keys:
            self.key_handler.bind(key[0], key[1])

        return self.screen_manager


if __name__ == '__main__':
    MainApp().run()
