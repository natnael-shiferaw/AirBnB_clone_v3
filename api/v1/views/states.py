#!/usr/bin/python3
"""
Defines views for State objects to handle
RESTful API actions.
"""

from api.v1.views import app_views
from flask import abort, jsonify, request

from models import storage
from models.state import State

# Route to retrieve all the State objects
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def retrieve_all_states():
    """
    Retrieve a list of all State objects.

    Returns:
        A JSON response containing a list of all State objects.
    """
    states = storage.all(State).values()

    list_of_states = [state.to_dict() for state in states]
    return jsonify(list_of_states)

# Route for retrieving a specific State object by ID
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def retrieve_state_by_id(state_id):
    """
    Retrieve a specific State object by ID.

    Args:
        state_id (str): The ID of the State object to retrieve.

    Returns:
        A JSON response containing the State object if found,
        otherwise returns a 404 error.
    """

    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)

# Route for deleting a specific State object by ID
@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state_by_id(state_id):
    """
    Delete a State object by ID.

    Args:
        state_id (str): The ID of the State object to delete.

    Returns:
        An empty JSON response with a status code of 200 if
        the State object is deleted successfully, otherwise
        returns a 404 error.
    """

    state = storage.get(State, state_id)
    if state:

        storage.delete(state)
        storage.save()

        return jsonify({}), 200
    else:

        abort(404)

# Route to create a new State object
@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_new_state():
    """
    Delete a State object by ID.

    Args:
        state_id (str): The ID of the State object to delete.

    Returns:
        An empty JSON response with a status code of 200
        if the State object is deleted successfully,
        otherwise returns a 404 error.
    """
    if not request.get_json():
        abort(400, 'Not a JSON')

    kwargs = request.get_json()
    if 'name' not in kwargs:

        abort(400, 'Missing name')

    state = State(**kwargs)
    state.save()

    return jsonify(state.to_dict()), 201

# Route for updating an existing State object by ID
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state_by_id(state_id):
    """
    Update a State object by ID.

    Args:
        state_id (str): The ID of the State object to update.

    Returns:
        A JSON response containing the updated State object with
        a status code of 200 if successful, otherwise
        returns a 404 error if the State object is not found
        or a 400 error if the request data is not valid JSON.
    """

    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            abort(400, 'Not a JSON')

        data = request.get_json()
        cant_be_updated = ['id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in cant_be_updated:
                setattr(state, key, value)

        state.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)

# Error Handlers:
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

    response = {'error': 'Not found'}
    return jsonify(response), 404

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

    response = {'error': 'Bad Request'}
    return jsonify(response), 400
