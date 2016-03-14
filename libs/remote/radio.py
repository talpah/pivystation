# coding=utf-8
from kivy.app import App

from libs.remote import app
from libs.remote.helpers import templated


@app.route('/radio')
@templated()
def radio():
    kivy_app = App.get_running_app()
    radio_widget = kivy_app.screen_manager
    print radio_widget.children
    radio_object = {}
    return {'radio': radio_object}
