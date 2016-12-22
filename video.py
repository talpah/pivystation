from __future__ import print_function
import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.lang import Builder

root = Builder.load_string('''
Video:
    source: 'http://91.232.210.204:8020/rtv.flv?file=rtv.flv&start=0'
''')

class TestApp(App):
    def build(self):
        return root

if __name__ == '__main__':
    TestApp().run()
