import os

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
