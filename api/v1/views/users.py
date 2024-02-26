#!/usr/bin/python3
"""
Creates an endpoint for User objects managing all
default RESTful API actions.
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from models import storage

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def retrieve_all_users():
    """
    Gets/Retrieves the list of all User objects.
    """
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def retrieve_user(user_id):
    """
    Gets/Retrieves a User object.
    """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)

@app_views.route('/users/<user_id>', methods=['DELETE'])
def remove_user(user_id):
    """
    Removes/Deletes a User object.
    """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def add_user():
    """
    Adds/Creates a User object.
    """
    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')

    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def modify_user(user_id):
    """
    Modifies/Updates a User object.
    """
    user = storage.get(User, user_id)
    if user:
        if not request.get_json():
            abort(400, 'Not a JSON')

        data = request.get_json()
        cant_be_updated = ['id', 'email', 'created_at', 'updated_at']
        for k, v in data.items():
            if k not in cant_be_updated:
                setattr(user, k, v)

        user.save()
        return jsonify(user.to_dict()), 200
    else:
        abort(404)

@app_views.errorhandler(404)
def handle_not_found_error(error):
    """
    Returns 404: Not Found.
    """
    response = {'error': 'Not found'}
    return jsonify(response), 404

@app_views.errorhandler(400)
def handle_bad_request_error(error):
    """
    Return Bad Request message for illegal requests to the API.
    """
    response = {'error': 'Bad Request'}
    return jsonify(response), 400
