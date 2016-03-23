#!runner
# coding=utf-8
from __future__ import absolute_import
from __future__ import print_function

import requests
from collections import deque
from random import randint
from threading import Thread

import locale
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty, Logger, ReferenceListProperty, NumericProperty, Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.vector import Vector

from libs import remotable_widget_map
from libs.remote import start_server

# noinspection PyUnresolvedReferences
from ui import *

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
        # print(key)
        if key in self._callbacks:
            for cb in self._callbacks[key]:
                cb(key)
        return False


class MainScreen(Screen):
    key_handler = ObjectProperty()

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.key_handler = kwargs['key_handler']


class FlyingWidget(BoxLayout):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class SaverScreen(Screen):
    saver = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SaverScreen, self).__init__(**kwargs)
        self.saver.init_flying()
        Clock.schedule_interval(self.saver.update, 1.0 / 30.0)


class SaverWidget(Widget):
    flying = ObjectProperty(None)

    def init_flying(self):
        self.flying.right = 800
        self.flying.velocity = Vector(4, 0).rotate(randint(0, 360))

    def update(self, dt):
        self.flying.move()
        # bounce off top and bottom
        if (self.flying.y < 0) or (self.flying.top > self.height):
            self.flying.velocity_y *= -1

        # bounce off left and right
        if (self.flying.x < 0) or (self.flying.right > self.width):
            self.flying.velocity_x *= -1


class MainApp(App):
    screens = deque()
    screen_manager = ScreenManager()
    key_handler = None
    remote_settings = {}

    def _key_right(self, *args):
        self.screens.rotate(1)
        self.screen_manager.transition.direction = 'left'
        self.screen_manager.current = self.screens[0]

    def _key_left(self, *args):
        self.screens.rotate(-1)
        self.screen_manager.transition.direction = 'right'
        self.screen_manager.current = self.screens[0]

    def build_config(self, config):
        config.setdefaults('remote', {'host': '0.0.0.0', 'port': 5000, 'debug': False})
        config.setdefaults('news', {'cycle_interval': 15, 'provider': 'mediafax'})
        config.setdefaults('radio', {'play_on_start': 'no',
                                     'streams': "\nhttp://astreaming.europafm.ro:8000/europafm_aacp48k#aac"
                                                "\nhttp://edge126.rdsnet.ro:84/profm/dancefm.mp3"})
        config.setdefaults('weather', {'temperature_unit_display': 'C', 'language': 'ro', 'temperature_unit': 'celsius',
                                       'provider': 'openweathermap', 'api_key': '1a6b3c983f34975e1634037a882c365a',
                                       'wind_speed_unit': 'kph', 'default_place': 'Bucuresti',
                                       'wind_speed_unit_display': 'km/h'})

    def build(self):
        screens = [
            ('main', MainScreen),
            ('saver', SaverScreen)
        ]
        keys = [
            ('q', self.stop),
            ('right', self._key_right),
            ('left', self._key_left)
        ]
        self.key_handler = KeyHandler(self.screen_manager)

        for screen in screens:
            screen_object = screen[1](name=screen[0], key_handler=self.key_handler)
            self.screen_manager.add_widget(screen_object)
            self.screens.append(screen[0])

        for key in keys:
            self.key_handler.bind(key[0], key[1])

        self.remote_settings = {
            'host': self.config.get('remote', 'host'),
            'port': self.config.getint('remote', 'port'),
            'debug': self.config.getboolean('remote', 'debug'),
        }

        print(remotable_widget_map(self.screen_manager))

        Thread(target=start_server, args=(self.remote_settings, Logger)).start()

        return self.screen_manager

    def on_stop(self):
        try:
            Logger.info('Remote: Shutting down')
            requests.get('http://{host}:{port}/shutdown'.format(**self.remote_settings))
        except Exception as e:
            Logger.warning('Remote: Shutdown failed:  %s' % e.message)


if __name__ == '__main__':
    MainApp().run()
