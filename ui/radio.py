from collections import deque

from kivy import Logger
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

from libs.sound import MySoundLoader


class RadioWidget(BoxLayout):
    can_remote = True
    radio_label = StringProperty()
    play_status = StringProperty()
    volume_value = StringProperty()
    current_volume = 1.0
    current_stream = None
    stream_list = []
    is_playing = False

    def __init__(self, **kwargs):
        super(RadioWidget, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.config = self.app.config
        streams = [s for s in self.config.get('radio', 'streams').split("\n") if s]
        self.stream_list = deque(streams)
        self.radio_label = ''
        self.play_status = 'Oprit'
        self.volume_value = 'Volum 100%'

        self.app.key_handler.bind('numpaddivide', self.playpause)
        self.app.key_handler.bind('numpadmul', self.next_stream)
        self.app.key_handler.bind('numpadadd', self.vol_up)
        self.app.key_handler.bind('numpadsubstract', self.vol_down)

        if self.config.get('radio', 'play_on_start').lower() in ['true', 'yes', 'y', '1']:
            self.play()

    def select_stream(self, url):
        self.current_stream = MySoundLoader.load(url)
        if self.current_stream:
            self.current_stream.volume = self.current_volume

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
        stream = self.stream_list[0].split('#')
        if len(stream)>2:
            label = stream[1]
        elif len(stream)>1 and len(stream[1])>3:
            label = stream[1]
        else:
            label = stream[0].split('/')[2]
        self.radio_label = label
        try:
            self.current_stream.play()
            Logger.info("Radio: playing %s" % self.stream_list[0])
            self.is_playing = True
            self.play_status = 'Pornit'
        except Exception as e:
            self.play_status = 'Eroare'
            Logger.error('Radio: Failed to play stream: {}'.format(e.message))

    def stop(self, *args):
        Logger.info("Radio: stopping.")
        self.radio_label = ''
        self.is_playing = False
        self.play_status = 'Oprit'
        self.current_stream.stop()

    def vol_up(self, *args):
        vol = self.current_volume + 0.02
        if vol > 1.0:
            vol = 1.0
        self.set_volume(vol)

    def vol_down(self, *args):
        vol = self.current_volume - 0.02
        if vol < 0.0:
            vol = 0.0
        self.set_volume(vol)

    def set_volume(self, volume):
        self.current_volume = volume
        if self.current_stream:
            self.current_stream.volume = volume
        self.volume_value = 'Volum {}%'.format(int(round(self.current_volume * 100)))
