#!/usr/bin/python3
"""
Creates an endpoint for Amenity objects that manages
all default RESTful API actions.
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.amenity import Amenity
from models import storage

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def retrieve_all():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])

@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def retrieve():
    """Retrieves an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def remove():
    """Deletes an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def add():
    """Creates an Amenity object"""
    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')

    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def modify():
    """Updates an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        if not request.get_json():
            abort(400, 'Not a JSON')

        data = request.get_json()
        cant_be_updated = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in cant_be_updated:
                setattr(amenity, key, value)

        amenity.save()
        return jsonify(amenity.to_dict()), 200
    else:
        abort(404)

@app_views.errorhandler(404)
def handle_not_found_error(error):
    """Returns 404: Not Found"""
    response = {'error': 'Not found'}
    return jsonify(response), 404

@app_views.errorhandler(400)
def handle_bad_request_error(error):
    """Return Bad Request message for illegal requests to the API."""
    response = {'error': 'Bad Request'}
    return jsonify(response), 400
