#!/usr/bin/python3
"""
Creates an instance of Flask, register the blueprint app_views
to Flask instance app.
"""

from api.v1.views import app_views
from flask_cors import CORS
from flask import Flask, jsonify
from models import storage
from os import getenv

app = Flask(__name__)

CORS(app, resources={r'/api/v1/*': {'origins': '0.0.0.0'}})

app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_session(exception):
    """Removes the current SQLAlchemy Session."""
    storage.close()


# Error handlers
@app.errorhandler(404)
def error_msg(error):
    """
    Returns:
    An error message `Not Found`.
    """
    response = {'error': 'Not found'}
    return jsonify(response), 404


if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)
