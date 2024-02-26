#!/usr/bin/python3
"""
Creates an endpoint for Place objects managing all
default RESTful API actions.
"""

from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage

@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def retrieve_places_by_city(city_id):
    """
    Gets the list of all Place objects of a City.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def retrieve_place(place_id):
    """
    Function that retrieves a Place object.
    """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)

@app_views.route('/places/<place_id>', methods=['DELETE'])
def remove_place(place_id):
    """
    Function that deletes a Place object.
    """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)

@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def add_place(city_id):
    """
    Function that creates a Place object.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def modify_place(place_id):
    """
    Function that modifies/updates a Place object.
    """
    place = storage.get(Place, place_id)
    if place:
        if not request.get_json():
            abort(400, 'Not a JSON')

        data = request.get_json()
        cant_be_updated = ['id', 'user_id', 'city_id', 'created_at',
                           'updated_at']
        for key, value in data.items():
            if key not in cant_be_updated:
                setattr(place, key, value)

        place.save()
        return jsonify(place.to_dict()), 200
    else:
        abort(404)

@app_views.errorhandler(404)
def handle_not_found_error(error):
    """
    Returns a 404 status code: 'Not Found' message.
    """
    response = {'error': 'Not found'}
    return jsonify(response), 404

@app_views.errorhandler(400)
def handle_bad_request_error(error):
    """
    Return a Bad Request message for unauthorized
    requests to the API.
    """
    response = {'error': 'Bad Request'}
    return jsonify(response), 400

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """
    Retrieves Place objects based on the specified
    JSON search criteria.
    """
    if request.get_json() is None:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        places_list = []
        for p in places:
            places_list.append(p.to_dict())
        return jsonify(places_list)

    places_list = []

    if states:
        objs_of_states = [storage.get(State, s_id) for s_id in states]
        for state in objs_of_states:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            places_list.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in places_list:
                        places_list.append(place)

    if amenities:
        if not places_list:
            places_list = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]

        places_list = [place for place in places_list
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for p in places_list:
        place_dict = p.to_dict()
        place_dict.pop('amenities', None)
        places.append(place_dict)

    return jsonify(places)
