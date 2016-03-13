from libs.remote import app
from libs.remote.helpers import templated


@app.route('/')
@templated()
def index():
    return {'hello': 'world'}
