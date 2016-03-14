# coding=utf-8
import imp
from datetime import datetime

import os
from kivy.app import App
from kivy.properties import StringProperty, Clock
from kivy.uix.label import Label

from libs import PROJECT_PATH


class NewsWidget(Label):
    can_remote = True

    news_items = StringProperty()
    news_rotation_paused = False
    news_rotation_manual_update = datetime.now()

    def __init__(self, **kwargs):
        super(NewsWidget, self).__init__(**kwargs)
        self.app = App.get_running_app()
        app_config = self.app.config
        provider = app_config.get('news', 'provider')
        news_module = imp.load_source(provider,
                                      os.path.join(PROJECT_PATH, 'libs', "news", "%s.py" % provider))
        self.news_provider = news_module.News()
        Clock.schedule_interval(self.update_news, 600)
        Clock.schedule_interval(self.rotate_news, app_config.getint('news', 'cycle_interval'))
        self.update_news()
        self.key_handler = self.app.key_handler
        self.key_handler.bind('down', lambda *args: self.rotate_news(direction='next', manual=True))
        self.key_handler.bind('up', lambda *args: self.rotate_news(direction='prev', manual=True))

    def update_news(self, *args):
        self.news_provider.update()
        self.rotate_news()

    def rotate_news(self, *args, **kwargs):
        if self.news_rotation_paused and 'manual' not in kwargs:
            if (datetime.now() - self.news_rotation_manual_update).total_seconds() > 30:
                self.news_rotation_paused = False
            else:
                return
        if 'direction' not in kwargs or kwargs.get('direction') == 'next':
            self.news_items = self.news_provider.get_next_article()
        else:
            self.news_items = self.news_provider.get_prev_article()
        if 'manual' in kwargs:
            self.news_rotation_manual_update = datetime.now()
            self.news_rotation_paused = True
