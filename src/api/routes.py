"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Characters, Locations, Episodes, FavoriteLocations, FavoriteCharacters, FavoriteEpisodes
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
        existing_favorite_location = FavoriteLocations.query.filter_by(user_id=user_id, location_id=location_id).first()
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
        body = request.json
        location_id_to_delete = body.get("location_id")
        if location_id_to_delete is None:
            raise APIException("Missing location_id in request body", 400)
        favorite_location_to_delete = FavoriteLocations.query.filter_by(user_id=user_id, location_id=location_id_to_delete).first()
        if favorite_location_to_delete:
            db.session.delete(favorite_location_to_delete)
            db.session.commit()
            return jsonify("Deleted successfully"), 201



@api.route("/favorite/characters/<int:user_id>", methods=["GET", "POST", "DELETE"])
def handle_favorite_characters(user_id):
    if request.method == "GET":
        favorite_characters = FavoriteCharacters.query.filter_by(user_id=user_id)
        favorite_characters_list = []
        for favorite_character in favorite_characters:
            favorite_characters_list.append(favorite_character.serialize())
        return jsonify(favorite_characters_list), 200
    elif request.method == "POST":
        body = request.json
        character_id = body["character_id"]
        existing_favorite_character = FavoriteCharacters.query.filter_by(user_id=user_id, character_id=character_id)
        if existing_favorite_character is not None:
            raise APIException("Character already in favorites.", 400)
        favorite_character = FavoriteCharacters(
            character_id = body["character_id"],
            user_id = user_id
        )
        if not isinstance(
            favorite_character, FavoriteCharacters
        ):
          return jsonify("Something went wrong"), 500  
        return jsonify(favorite_character.serialize()), 201
    elif request.method == "DELETE":
        body = request.json
        character_id_to_delete = body.get("character_id")
        if character_id_to_delete is None:
            raise APIException("Missing character_id in request body", 400)
        favorite_character_to_delete = FavoriteCharacters.query.filter_by(user_id=user_id, character_id=character_id_to_delete).first()
        if favorite_character_to_delete:
            db.session.delete(favorite_character_to_delete)
            db.session.commit()
            return jsonify("Deleted successfully"), 201
        
@api.route("/favorite/episodes/<int:user_id>", methods=["GET", "POST", "DELETE"])
def handle_favorite_episodes(user_id):
    if request.method == "GET":
        favorite_episodes = FavoriteEpisodes.query.filter_by(user_id=user_id)
        favorite_episodes_list = []
        for favorite_episode in favorite_episodes:
            favorite_episodes_list.append(favorite_episode.serialize())
        return jsonify(favorite_episodes_list), 200
    elif request.method == "POST":
        body = request.json
        episode_id = body["episode_id"]
        existing_favorite_episode = FavoriteEpisodes.query.filter_by(user_id=user_id, episode_id=episode_id)
        if existing_favorite_episode is not None:
            raise APIException("Episode already in favorites.", 400)
        favorite_episode = FavoriteEpisodes(
            episode_id = body["episode_id"],
            user_id = user_id
        )
        if not isinstance(
            favorite_episode, FavoriteEpisodes
        ):
          return jsonify("Something went wrong"), 500  
        return jsonify(favorite_episode.serialize()), 201
    elif request.method == "DELETE":
        body = request.json
        episode_id_to_delete = body.get("episode_id")
        if episode_id_to_delete is None:
            raise APIException("Missing episode_id in request body", 400)
        favorite_episode_to_delete = FavoriteEpisodes.query.filter_by(user_id=user_id, episode_id=episode_id_to_delete).first()
        if favorite_episode_to_delete:
            db.session.delete(favorite_episode_to_delete)
            db.session.commit()
            return jsonify("Deleted successfully"), 201

@api.route("/users/favorites/<int:user_id>", methods=["GET", "POST", "DELETE"])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    
    if user is None:
        return jsonify("User not found"), 404

    favorite_locations = [fav.serialize() for fav in user.favorite_locations]
    favorite_characters = [fav.serialize() for fav in user.favorite_characters]
    favorite_episodes = [fav.serialize() for fav in user.favorite_episodes]
    
    response = {
        "favorite_locations": favorite_locations,
        "favorite_characters": favorite_characters,
        "favorite_episodes": favorite_episodes
    }

    return jsonify(response), 200
