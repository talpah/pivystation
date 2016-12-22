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
    _loaded_stream = None
    selected_stream = 0
    stream_list = []
    is_playing = False

    def __init__(self, **kwargs):
        super(RadioWidget, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.config = self.app.config
        self.stream_list = [s for s in self.config.get('radio', 'streams').split("\n") if s]
        self.build_label()
        self.play_status = 'Radio: Oprit'
        self.volume_value = 'Volum 100%'

        self.app.key_handler.bind('f4', self.prev_stream)
        self.app.key_handler.bind('f5', self.playpause)
        self.app.key_handler.bind('f6', self.next_stream)
        self.app.key_handler.bind('numpaddivide', self.playpause)
        self.app.key_handler.bind('numpadmul', self.next_stream)
        self.app.key_handler.bind('numpadadd', self.vol_up)
        self.app.key_handler.bind('numpadsubstract', self.vol_down)

        self.app.myradio = self
        self.build_label()

        if self.config.get('radio', 'play_on_start').lower() in ['true', 'yes', 'y', '1']:
            self.play()

    def build_label(self):
        label_full = ''
        max_length = 5
        cnt = 0
        for stream in self.stream_list:
            stream = stream.split('#')
            if len(stream) > 2:
                label = stream[1]
            elif len(stream) > 1 and len(stream[1]) > 3:
                label = stream[1]
            else:
                label = stream[0].split('/')[2]
            if cnt == self.selected_stream:
                label = '[color=C71585]{}[/color]'.format(label)
            label_full += '{}\n'.format(label)
            cnt += 1
        self.radio_label = label_full

    @property
    def current_stream(self):
        return self.stream_list[self.selected_stream]

    def select_stream(self, url):
        self.build_label()
        self._loaded_stream = MySoundLoader.load(url)
        if self._loaded_stream:
            self._loaded_stream.volume = self.current_volume

    def set_stream(self, id):
        if id < 0 or id >= len(self.stream_list):
            return False
        if self._loaded_stream:
            self._loaded_stream.stop()
        self.selected_stream = id
        self.select_stream(self.current_stream)
        self.play()

    def next_stream(self, *args):
        if self._loaded_stream:
            self._loaded_stream.stop()
        self.selected_stream += 1
        if self.selected_stream >= len(self.stream_list):
            self.selected_stream = 0
        self.select_stream(self.current_stream)
        self.play()

    def prev_stream(self, *args):
        if self._loaded_stream:
            self._loaded_stream.stop()
        self.selected_stream -= 1
        if self.selected_stream < 0:
            self.selected_stream = len(self.stream_list) - 1
        self.select_stream(self.current_stream)
        self.play()

    def playpause(self, *args):
        if self.is_playing:
            self.stop()
        else:
            self.play()

    def play(self, *args):
        if not self._loaded_stream:
            self.select_stream(self.current_stream)
        try:
            self._loaded_stream.play()
            Logger.info("Radio: playing %s" % self.stream_list[0])
            self.is_playing = True
            self.play_status = 'Radio: Pornit'
        except Exception as e:
            self.play_status = 'Radio: Eroare'
            Logger.error('Radio: Failed to play stream: {}'.format(e.message))

    def stop(self, *args):
        Logger.info("Radio: stopping.")
        self.is_playing = False
        self.play_status = 'Radio: Oprit'
        self._loaded_stream.stop()

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
        if self._loaded_stream:
            self._loaded_stream.volume = volume
        self.volume_value = 'Volum {}%'.format(int(round(self.current_volume * 100)))
