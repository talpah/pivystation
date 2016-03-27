import os

from kivy.clock import Clock

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def remotable_widget_map(parent_object):
    widgets = {}
    w = {}
    for child in parent_object.children:
        if hasattr(child, 'remote_name'):
            w[child.remote_name] = child
        widgets = w.copy()
        widgets.update(remotable_widget_map(child))
    return widgets


class Scheduler(object):
    CALLBACKS = []

    @staticmethod
    def callback(*args):
        for cb in Scheduler.CALLBACKS:
            cb()

    @staticmethod
    def add_callback(cb):
        Scheduler.CALLBACKS.append(cb)


class MinuteScheduler(Scheduler):
    CALLBACKS = []


CLOCK = Clock.schedule_interval(Scheduler.callback, 1)
MINUTECLOCK = Clock.schedule_interval(MinuteScheduler.callback, 60)
