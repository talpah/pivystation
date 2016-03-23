from collections import deque
from datetime import datetime, timedelta

import feedparser
import locale
from babel.dates import format_timedelta
from kivy import Logger


class News(object):
    def __init__(self):
        self.feed_url = 'http://www.mediafax.ro/rss/'
        self.news = {'items': []}
        self.articles = deque()

    def update(self):
        self.news = feedparser.parse(self.feed_url)

        article_list = []

        xlocale = locale.getlocale(locale.LC_TIME)
        locale.setlocale(locale.LC_TIME, 'en_US.utf-8')

        if not self.news['items']:
            Logger.error('NEWS: Seems there\'s no news')
            return # Return here so we keep old news (if any)

        for x in self.news['items']:
            description = unicode(x['description']).strip()
            description = description.split('<', 1)[0].strip()
            title = unicode(x['title']).strip()
            if description == '.':
                title = u'[color=#FFDD63]{}[/color]'.format(title)
                description = ''
            article_date = (datetime.strptime(x['published'], "%a, %d %b %Y %H:%M:%S %Z") + timedelta(hours=2))
            article_relative_date = format_timedelta(article_date - datetime.now(),
                                                     granularity='minute',
                                                     locale='ro_RO.utf-8',
                                                     add_direction=True)
            article_list.append(u'{}\n[color=#777777]{}[/color]\n\n{}'.format(title,
                                                                              article_relative_date,
                                                                              description))
        locale.setlocale(locale.LC_TIME, xlocale)
        self.articles = deque(article_list)

    def get_next_article(self):
        self.shift_descriptions('next')
        try:
            return self.articles[0]
        except IndexError:
            return ''

    def get_prev_article(self):
        self.shift_descriptions('prev')
        try:
            return self.articles[0]
        except:
            return ''

    def shift_descriptions(self, direction='next'):
        if direction == 'next':
            self.articles.rotate(-1)
        else:
            self.articles.rotate(1)
