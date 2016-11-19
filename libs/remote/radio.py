# coding=utf-8
from kivy.app import App
from flask import redirect

from libs.remote import app
from libs.remote.helpers import templated

status_map = {
    True: 'playing',
    False: 'stopped'
}


@app.route('/radio')
@templated()
def radio():
    kivy_app = App.get_running_app()
    stream_list = [stream.split('#') for stream in kivy_app.myradio.stream_list]
    radio_object = {
        "state": kivy_app.myradio.is_playing,
        "status": status_map[kivy_app.myradio.is_playing],
        "stream_list": stream_list,
        "selected_stream": kivy_app.myradio.selected_stream,
        "current_stream": kivy_app.myradio.current_stream.split('#')}
    # app.logger.error(str(kivy_app.root.__dict__))
    return {'radio': radio_object}

@app.route('/radio/next')
def radio_next():
    kivy_app = App.get_running_app()
    kivy_app.myradio.next_stream()
    return redirect('/radio')

@app.route('/radio/prev')
def radio_prev():
    kivy_app = App.get_running_app()
    kivy_app.myradio.prev_stream()
    return redirect('/radio')

@app.route('/radio/toggle')
def radio_toggle():
    kivy_app = App.get_running_app()
    kivy_app.myradio.playpause()
    return redirect('/radio')
