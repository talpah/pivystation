# coding=utf-8
import os
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty, ListProperty, Clock

from libs import PROJECT_PATH
from libs.timer import Timer
from libs.widgets.LabelB import LabelB


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

        for key in Timer.all_keys:
            self.app.key_handler.bind(key, self.timer_provider.key)
            self.app.key_handler.bind(key, self.update_timer)

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
