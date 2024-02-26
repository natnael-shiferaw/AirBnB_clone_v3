#!/usr/bin/python3
"""Handles RESTful API actions for Review objects."""

from models.place import Place
from models.review import Review
from models.user import User
from models import storage

from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def retrieve_reviews_for_place(place_id):
    """
    Retrieves the list of all reviews associated with a specific place.

    Args:
        place_id (str): The ID of the place to retrieve reviews for.

    Returns:
        JSON: A JSON response containing the list of review objects
        associated with the specified place.

    Raises:
        404: If the specified place does not exist.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_review(review_id):
    """
    Retrieves a specific review by its ID.

    Args:
        review_id (str): The ID of the review to retrieve.

    Returns:
        JSON: A JSON response containing the review object if found,
        or a 404 error if not found.
    """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def remove_review(review_id):
    """
    Deletes a review by its ID.

    Args:
        review_id (str): The ID of the review to delete.

    Returns:
        JSON: An empty JSON response with a 200 status code if
        the review is deleted successfully, or a 404 error if
        the review is not found.
    """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def add_review(place_id):
    """
    Creates a new review associated with a place.

    Args:
        place_id (str): The ID of the place to associate the review with.

    Returns:
        JSON: A JSON response containing the newly created review object
        with a 201 status code if successful, or a 404 error if the place
        is not found.

    Raises:
        400: If the request data is not in JSON format, or if required
        fields are missing.
        404: If the specified place or user does not exist.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'text' not in data:
        abort(400, 'Missing text')

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def modify_review(review_id):
    """
    Modifies/Updates an existing review by its ID.

    Args:
        review_id (str): The ID of the review to update.

    Returns:
        JSON: A JSON response containing the updated review object
        with a 200 status code if successful, or a 404 error if
        the review is not found.

    Raises:
        400: If the request data is not in JSON format.
    """
    review = storage.get(Review, review_id)
    if review:
        if not request.get_json():
            abort(400, 'Not a JSON')

        data = request.get_json()
        cant_be_updated = ['id', 'user_id', 'place_id', 'created_at',
                           'updated_at']
        for k, v in data.items():
            if k not in cant_be_updated:
                setattr(review, k, v)

        review.save()
        return jsonify(review.to_dict()), 200
    else:
        abort(404)


@app_views.errorhandler(404)
def handle_not_found_error(error):
    """
    Returns a 404 error response in JSON format.
    """
    response = {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def handle_bad_request_error(error):
    """
    Returns a 400 error response in JSON format.
    """
    response = {'error': 'Bad Request'}
    return jsonify(response), 400
