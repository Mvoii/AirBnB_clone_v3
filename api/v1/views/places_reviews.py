#!/usr/bin/python3
"""Create a view for Rewview"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """Get all reviews in place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """gets a review by id"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.reoute('/reviews/<review_id>', methods=['DELETE'],
                   strict_slashes=False)
def delete_review(review_id):
    """Deletes a review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    storage.delete(review_id)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a review of a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    new_review = request.get_json()
    if new_review is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in new_review:
        abort(400, 'Missing user_id')
    user = storage.get("User", new_review["user_id"])
    if user is None:
        abort(404)
    review = Review(**new_review)
    setattr(review, 'place_id', place_id)
    storage.new(review)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updaet a review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    new_review = request.get_json()
    if new_review is None:
        abort(400, 'Not a JSON')
    for key, value in new_review.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
