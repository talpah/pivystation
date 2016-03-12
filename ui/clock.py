# coding=utf-8
import time

from kivy.properties import StringProperty, Clock
from kivy.uix.boxlayout import BoxLayout


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