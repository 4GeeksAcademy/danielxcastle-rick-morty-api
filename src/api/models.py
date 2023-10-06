from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from api.utils import APIException

db = SQLAlchemy()


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f"<User {self.email}>"

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }


class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(120), nullable=False)
    species = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<Character {self.name}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "species": self.species,
            "gender": self.gender,
        }


class Locations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<Location {self.name}>"

    def serialize(self):
        return {"id": self.id, "name": self.name, "type": self.type}


class Episodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    air_date = db.Column(db.String(120), nullable=False)
    episode = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<Episode {self.name}>"

    def serialize(self):
        return {"id": self.id, "air_date": self.air_date, "episode": self.episode}



class FavoriteLocations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, ForeignKey("locations.id"))
    user_id = db.Column(db.Integer, ForeignKey("user.id"))
    user = db.relationship("User", backref="favorite_locations")
    location = db.relationship("Locations", backref="marked_as_favorite")

    def __init__(self, user_id, location_id):
        self.location_id = location_id
        self.user_id = user_id
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            raise APIException(f"{error}", 500)

    def __repr__(self):
        return f"<Favorite Locations {self.id}>"

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.serialize(),
            "location": self.location.serialize()
        }
    

class FavoriteCharacters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, ForeignKey("characters.id"))
    user_id = db.Column(db.Integer, ForeignKey("user.id"))
    user = db.relationship("User", backref="favorite_characters")
    character = db.relationship("Characters", backref="marked_as_favorite")

    def __init__(self, user_id, character_id):
        self.character_id = character_id
        self.user_id = user_id
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            raise APIException(f"{error}", 500)

    def __repr__(self):
        return f"<Favorite Characters {self.id}>"

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.serialize(),
            "character": self.character.serialize()

        }
    
class FavoriteEpisodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    episode_id = db.Column(db.Integer, ForeignKey("episodes.id"))
    user_id = db.Column(db.Integer, ForeignKey("user.id"))
    user = db.relationship("User", backref="favorite_episodes")
    episode = db.relationship("Episodes", backref="marked_as_favorite")

    def __init__(self, user_id, episode_id):
        self.episode_id = episode_id
        self.user_id = user_id
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            raise APIException(f"{error}", 500)

    def __repr__(self):
        return f"<Favorite Episodes {self.id}>"

    def serialize(self):
        return {
            "id": self.id,
            "episode": self.episode.serialize()

        }

