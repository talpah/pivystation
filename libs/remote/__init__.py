import os
from flask import Flask

from libs import PROJECT_PATH

static_folder = 'static'
template_folder = 'templates'
if PROJECT_PATH is not None:
    static_folder = os.path.join(PROJECT_PATH, 'ui', 'remote', 'static')
    template_folder = os.path.join(PROJECT_PATH, 'ui', 'remote', 'templates')
app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)
# cache = SimpleCache()

# Import controllers
# noinspection PyUnresolvedReferences
import libs.remote.index
import libs.remote.shutdown


def start_server(settings, logger):
    try:
        logger.info('Remote: Starting on {host}:{port}'.format(**settings))
        app.run(**settings)
    except Exception, e:
        logger.warning('Remote: Start failed:  %s' % str(e))