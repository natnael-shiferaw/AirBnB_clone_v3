#!/usr/bin/python3
"""
Create a new endpoint for City objects that manages
all default RESTful API actions.
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.city import City
from models import storage
from models.state import State

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities_for_state(state_id):
    """
    Retrieve the list of all City objects associated with a State.

    Args:
        state_id (str): The ID of the State.

    Returns:
        A JSON response containing a list of all City objects
        associated with the State. Returns a 404 error
        if the State object is not found.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    """
    Retrieve a specific City object by its ID.

    Args:
        city_id (str): The ID of the City object.

    Returns:
        A JSON response containing the City object if found,
        otherwise returns a 404 error.
    """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)

@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city_by_id(city_id):
    """
    Delete a City object by its ID.

    Args:
        city_id (str): The ID of the City object to delete.

    Returns:
        An empty JSON response with a status code of 200
        if the City object is deleted successfully,
        otherwise returns a 404 error.
    """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city_for_state(state_id):
    """
    Create a new City object under a specific State.

    Args:
        state_id (str): The ID of the State to create the City under.

    Returns:
        A JSON response containing the newly created City
        object with a status code of 201 if successful, otherwise
        returns a 404 error if the State object is not found or
        a 400 error if the request data is not valid JSON or
        if the 'name' key is missing.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')

    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city_by_id(city_id):
    """
    Update an existing City object by its ID.

    Args:
        city_id (str): The ID of the City object to update.

    Returns:
        A JSON response containing the updated City object with
        a status code of 200 if successful, otherwise returns
        a 404 error if the City object is not found or a 400
        error if the request data is not valid JSON.
    """
    city = storage.get(City, city_id)
    if city:
        if not request.get_json():
            abort(400, 'Not a JSON')

        data = request.get_json()
        cant_be_updated = ['id', 'state_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in cant_be_updated:
                setattr(city, key, value)

        city.save()
        return jsonify(city.to_dict()), 200
    else:
        abort(404)

@app_views.errorhandler(404)
def handle_not_found_error(error):
    """
    Handle 404 errors.

    Args:
        error (Exception): The error object.

    Returns:
        A JSON response with a status code of 404
        indicating that the requested resource is not found.
    """
    return jsonify({'error': 'Not found'}), 404

@app_views.errorhandler(400)
def handle_bad_request_error(error):
    """
    Handle 400 errors.

    Args:
        error (Exception): The error object.

    Returns:
        A JSON response with a status code of 400
        indicating a bad request.
    """
    return jsonify({'error': 'Bad Request'}), 400
