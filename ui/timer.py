# coding=utf-8
from __future__ import print_function
import os
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty, ListProperty, Clock

from libs import PROJECT_PATH, Scheduler
from libs.timer import Timer
from libs.widgets.LabelB import LabelB


class TimerWidget(LabelB):
    can_remote = True
    alarmsound = SoundLoader.load(os.path.join(PROJECT_PATH, 'libs', 'timer', 'alarm.mp3'))
    alarmsound.loop = True
    timer_text = StringProperty()
    timer_color = ListProperty()
    timer_bgcolor = ListProperty()
    alarm_odd = False
    timer_updater = None

    def __init__(self, **kwargs):
        super(TimerWidget, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.timer_provider = Timer()
        self.alarmsound.play()

        for key in Timer.all_keys:
            self.app.key_handler.bind(key, self.timer_provider.key)
            self.app.key_handler.bind(key, self.update_timer)
        self.update_timer()
        Scheduler.add_callback(self.timer_provider.countdown)
        Scheduler.add_callback(self.update_timer)

    def update_timer(self, *args):
        if self.timer_provider.is_active or self.timer_provider.is_editing:
            pass
        else:
            if self.timer_updater:
                self.timer_updater.cancel()
                self.timer_updater = None
        self.timer_text = str(self.timer_provider)
        if self.timer_provider.is_alarmed:
            if self.alarm_odd:
                self.timer_color = [1, 0, 0, 1]
                self.timer_bgcolor = [0, 0, 0, 1]
            else:
                self.timer_color = [0, 0, 0, 1]
                self.timer_bgcolor = [1, 0, 0, 1]
            self.alarm_odd = not self.alarm_odd
            if self.alarmsound.state != 'play':
                self.alarmsound.play()
        else:
            self.alarmsound.stop()
            self.timer_color = [0.529, 0.808, 0.922, 1]
            self.timer_bgcolor = [0, 0, 0, 1]
