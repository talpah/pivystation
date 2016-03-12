from collections import deque

from kivy import Logger
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

from libs.Sound import MySoundLoader


class RadioWidget(BoxLayout):
    radio_label = StringProperty()
    play_status = StringProperty()
    volume_value = StringProperty('100%')
    current_stream = None
    stream_list = []
    is_playing = False

    def __init__(self, **kwargs):
        super(RadioWidget, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.config = self.app.config
        streams = self.config.get('radio', 'streams')
        self.stream_list = deque([s for s in streams.split("\n") if s])
        self.radio_label = ''
        self.play_status = 'Oprit'
        self.volume_value = 'Volum   %s'

        self.app.key_handler.bind('f2', self.playpause)
        self.app.key_handler.bind('f3', self.next_stream)

    def select_stream(self, url):
        self.current_stream = MySoundLoader.load(url)

    def next_stream(self, *args):
        if self.current_stream:
            self.current_stream.stop()
        self.stream_list.rotate(1)
        self.select_stream(self.stream_list[0])
        self.play()

    def playpause(self, *args):
        if self.is_playing:
            self.stop()
        else:
            self.play()

    def play(self, *args):
        if not self.current_stream:
            self.select_stream(self.stream_list[0])
        self.radio_label = self.stream_list[0]
        Logger.info("Radio playing %s" % self.stream_list[0])
        self.is_playing = True
        self.play_status = 'Pornit'
        self.current_stream.play()

    def stop(self, *args):
        Logger.info("Radio stopping.")
        self.radio_label = self.stream_list[0]
        self.is_playing = False
        self.play_status = 'Oprit'
        self.current_stream.stop()
