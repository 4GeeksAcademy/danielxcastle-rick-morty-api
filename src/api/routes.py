"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Characters, Locations, Episodes, FavoriteLocations, FavoriteCharacters
from api.utils import generate_sitemap, APIException

api = Blueprint("api", __name__)


@api.route("/hello", methods=["POST", "GET"])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route("/users", methods=["GET"])
def handle_users():
    if request.method != "GET":
        raise APIException("method not implemented", 405)
    users = User.query.all()
    user_dictionaries = []
    for user in users:
        user_dictionaries.append(user.serialize())
    return jsonify(user_dictionaries), 200


@api.route("/characters", methods=["GET"])
def handle_characters():
    if request.method != "GET":
        raise APIException("method not implemented", 405)
    characters = Characters.query.all()
    character_dictionaries = []
    for character in characters:
        character_dictionaries.append(character.serialize())
    return jsonify(character_dictionaries), 200


@api.route("/episodes", methods=["GET"])
def handle_episodes():
    if request.method != "GET":
        raise APIException("method not implemented", 405)
    episodes = Episodes.query.all()
    episode_dictionaries = []
    for episode in episodes:
        episode_dictionaries.append(episode.serialize())
    return jsonify(episode_dictionaries), 200


@api.route("/locations", methods=["GET"])
def handle_locations():
    if request.method != "GET":
        raise APIException("method not implemented", 405)
    locations = Locations.query.all()
    location_dictionaries = []
    for location in locations:
        location_dictionaries.append(location.serialize())
    return jsonify(location_dictionaries), 200


@api.route("/favorite/locations/<int:user_id>", methods=["GET", "POST", "DELETE"])
def handle_favorite_locations(user_id):
    if request.method == "GET":
        favorite_locations = FavoriteLocations.query.filter_by(user_id=user_id)
        favorite_locations_list = []
        for favorite_location in favorite_locations:
            favorite_locations_list.append(favorite_location.serialize())
        return jsonify(favorite_locations_list), 200
    elif request.method == "POST":
        body = request.json
        location_id = body["location_id"]
        existing_favorite_location = FavoriteLocations.query.filter_by(user_id=user_id, location_id=location_id)
        if existing_favorite_location is not None:
            raise APIException("Location already in favorites.", 400)
        favorite_location = FavoriteLocations(
            location_id = body["location_id"],
            user_id = user_id
        )
        if not isinstance(
            favorite_location, FavoriteLocations
        ):
          return jsonify("Something went wrong"), 500  
        return jsonify(favorite_location.serialize()), 201
    elif request.method == "DELETE":
        pass

@api.route("/favorite/characters/<int:user_id>", methods=["GET", "POST", "DELETE"])
def handle_favorite_characters(user_id):
    if request.method == "GET":
        favorite_characters = FavoriteCharacters.query.filter_by(user_id=user_id)
        favorite_characters_list = []
        for favorite_location in favorite_characters:
            favorite_characters_list.append(favorite_location.serialize())
        return jsonify(favorite_characters_list), 200
    elif request.method == "POST":
        body = request.json
        character_id = body["character_id"]
        existing_favorite_character = FavoriteLocations.query.filter_by(user_id=user_id, character_id=character_id)
        if existing_favorite_character is not None:
            raise APIException("Location already in favorites.", 400)
        favorite_character = FavoriteCharacters(
            character_id = body["character_id"],
            user_id = user_id
        )
        if not isinstance(
            favorite_location, FavoriteCharacters
        ):
          return jsonify("Something went wrong"), 500  
        return jsonify(favorite_character.serialize()), 201
    elif request.method == "DELETE":
        pass