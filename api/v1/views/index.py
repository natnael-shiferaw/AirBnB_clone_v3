#!/usr/bin/python3
"""
Creates a route `/status` on the object app_views
that returns a JSON: "status": "OK"
"""


from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def api_status():
    """Returns:
    A JSON response for RESTful API health."""
    response = {'status': 'OK'}
    return jsonify(response)


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """
    This function retrieves the number of objects
    for each class.
    """
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(stats)
