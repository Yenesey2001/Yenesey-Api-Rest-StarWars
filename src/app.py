"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Vehicle, Favourites, Vehicle, Planet
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# .................. EN EL ARCHIVO INICIALIZAR.PY PODRAS INICIALIZAR LA BD CON 5 PLANETAS, VEHICULOS Y CHARACTERS..............
# ................................. USERS ( POST Y GET ) ........................................


@app.route('/users', methods=['POST'])
def add_user():

    request_body = request.json

    if not request_body:
        return jsonify({"error": "Invalid input"}), 400

    new_user = User(
        firstname=request_body.get("firstname"),
        lastname=request_body.get("lastname"),
        email=request_body.get("email")
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User Created!!"}), 201


@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()

    if not users:
        return jsonify({"msg": "Users not found"}), 404

    response_body = {
        "Users": [user.serialize_user() for user in users]
    }

    return jsonify(response_body), 200


# ................................. CHARACTERS ( GET Y GET(id) ) ........................................

@app.route('/characters', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()

    if not characters:
        return jsonify({"msg": "Characters not found"}), 404

    response_body = {
        "characters": [character.serialize() for character in characters]
    }

    return jsonify(response_body), 200


@app.route('/characters/<int:charac_id>', methods=['GET'])
def get_character(charac_id):  # Nombre de la función corregido

    # Se pasa la variable correctamente
    character = Character.query.get(charac_id)

    if not character:
        return jsonify({"msg": "Character not found"}), 404

    response_body = {
        "character": character.serialize()  # Solo serializamos un objeto
    }

    return jsonify(response_body), 200


# ................................. PLANETS ( GET Y GET(id) ) ........................................

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()

    if not planets:
        return jsonify({"msg": "Planets not found"}), 404

    response_body = {
        "Planets": [planets.serialize_planet() for planets in planets]
    }

    return jsonify(response_body), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):  # Nombre de la función corregido

    # Se pasa la variable correctamente
    planet = Planet.query.get(planet_id)

    if not planet:
        return jsonify({"msg": "Planet not found"}), 404

    response_body = {
        "Planet": planet.serialize_planet()  # Solo serializamos un objeto
    }

    return jsonify(response_body), 200


# ................................. VEHICLES ( GET Y GET(id) ) ........................................

@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():
    vehicles = Vehicle.query.all()

    if not vehicles:
        return jsonify({"msg": "Vehicles not found"}), 404

    response_body = {
        "Vehicles": [vehicle.serialize_vehicle() for vehicle in vehicles]
    }

    return jsonify(response_body), 200


@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):  # Nombre de la función corregido

    # Se pasa la variable correctamente
    vehicle = Vehicle.query.get(vehicle_id)

    if not vehicle:
        return jsonify({"msg": "Vehicle not found"}), 404

    response_body = {
        "Planet": vehicle.serialize_vehicle()  # Solo serializamos un objeto
    }

    return jsonify(response_body), 200


# ................................. FAVOURITES ( POST PLANET, VEHICLES, CHARACTERS ) ........................................

@app.route('/favourite/planet/<int:planet_id>', methods=['POST'])
def add_favourite_planet(planet_id):
    request_body = request.json

    if not request_body or "user_id" not in request_body:
        return jsonify({"error": "Invalid input, user_id is required"}), 400

    user_id = request_body.get("user_id")

    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not planet:
        return jsonify({"error": "Planet not found"}), 404

    existing_favourite = Favourites.query.filter_by(
        user_id=user_id, planet_id=planet_id).first()
    if existing_favourite:
        return jsonify({"error": "Planet is already in favourites"}), 400

    new_fav_planet = Favourites(user_id=user_id, planet_id=planet_id)
    db.session.add(new_fav_planet)
    db.session.commit()

    return jsonify({"msg": "Favourite planet added!"}), 201

# ........................................................................................


@app.route('/favourite/vehicle/<int:vehicle_id>', methods=['POST'])
def add_favourite_vehicle(vehicle_id):
    request_body = request.json

    if not request_body or "user_id" not in request_body:
        return jsonify({"error": "Invalid input, user_id is required"}), 400

    user_id = request_body.get("user_id")

    user = User.query.get(user_id)
    vehicle = Vehicle.query.get(vehicle_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404

    existing_favourite = Favourites.query.filter_by(
        user_id=user_id, vehicle_id=vehicle_id).first()
    if existing_favourite:
        return jsonify({"error": "Vehicle is already in favourites"}), 400

    new_fav_vehicle = Favourites(user_id=user_id, vehicle_id=vehicle_id)
    db.session.add(new_fav_vehicle)
    db.session.commit()

    return jsonify({"msg": "Favourite vehicle added!"}), 201

# ........................................................................................


@app.route('/favourite/character/<int:character_id>', methods=['POST'])
def add_favourite_character(character_id):
    request_body = request.json

    if not request_body or "user_id" not in request_body:
        return jsonify({"error": "Invalid input, user_id is required"}), 400

    user_id = request_body.get("user_id")

    user = User.query.get(user_id)
    character = Character.query.get(character_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not character:
        return jsonify({"error": "Character not found"}), 404

    existing_favourite = Favourites.query.filter_by(
        user_id=user_id, character_id=character_id).first()
    if existing_favourite:
        return jsonify({"error": "Character is already in favourites"}), 400

    new_fav_character = Favourites(user_id=user_id, character_id=character_id)
    db.session.add(new_fav_character)
    db.session.commit()

    return jsonify({"msg": "Favourite Character added!"}), 201

# ................................. FAVOURITES ( GET PLANET, VEHICLES, CHARACTERS ) ........................................


@app.route('/users/favourites/<int:user_id>', methods=['GET'])
def get_user_favourites(user_id):

    favourites = Favourites.query.filter_by(user_id=user_id).all()

    if not favourites:
        return jsonify({
            "planet_ids": [],
            "character_ids": [],
            "vehicle_ids": []
        }), 200

    planet_ids = []
    character_ids = []
    vehicle_ids = []

    for favourite in favourites:
        if favourite.planet_id:
            planet_ids.append(favourite.planet_id)
        if favourite.character_id:
            character_ids.append(favourite.character_id)
        if favourite.vehicle_id:
            vehicle_ids.append(favourite.vehicle_id)

    response_body = {
        "planet_ids": planet_ids,
        "character_ids": character_ids,
        "vehicle_ids": vehicle_ids
    }

    return jsonify(response_body), 200

# ................................. FAVOURITES ( DELETE PLANET, VEHICLES, CHARACTERS ) ........................................


@app.route('/favourite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favourite_planet(planet_id):
    request_body = request.json

    if not request_body or "user_id" not in request_body:
        return jsonify({"error": "Invalid input, user_id is required"}), 400

    user_id = request_body.get("user_id")

    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not planet:
        return jsonify({"error": "Planet not found"}), 404

    existing_favourite = Favourites.query.filter_by(
        user_id=user_id, planet_id=planet_id).first()

    db.session.delete(existing_favourite)
    db.session.commit()

    return jsonify({"msg": "Favourite planet deleted!"}), 201

# ........................................................................................


@app.route('/favourite/character/<int:character_id>', methods=['DELETE'])
def delete_favourite_character(character_id):
    request_body = request.json

    if not request_body or "user_id" not in request_body:
        return jsonify({"error": "Invalid input, user_id is required"}), 400

    user_id = request_body.get("user_id")

    user = User.query.get(user_id)
    character = Character.query.get(character_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not character:
        return jsonify({"error": "Character not found"}), 404

    existing_favourite = Favourites.query.filter_by(
        user_id=user_id, character_id=character_id).first()

    db.session.delete(existing_favourite)
    db.session.commit()

    return jsonify({"msg": "Favourite Character deleted!"}), 201

# ........................................................................................


@app.route('/favourite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_favourite_vehicle(vehicle_id):
    request_body = request.json

    if not request_body or "user_id" not in request_body:
        return jsonify({"error": "Invalid input, user_id is required"}), 400

    user_id = request_body.get("user_id")

    user = User.query.get(user_id)
    vehicle = Vehicle.query.get(vehicle_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404

    existing_favourite = Favourites.query.filter_by(
        user_id=user_id, vehicle_id=vehicle_id).first()

    db.session.delete(existing_favourite)
    db.session.commit()

    return jsonify({"msg": "Favourite vehicle deleted!"}), 201


# .......................................... PUNTOS EXTRA ...........................................
# .......................................... POST (PLANETS, CHARACTER, VEHICLES) ...........................................


@app.route('/planets', methods=['POST'])
def add_planets():

    request_body = request.json

    if not request_body:
        return jsonify({"error": "Invalid input"}), 400

    new_planet = Planet(
        population=request_body.get("population"),
        climate=request_body.get("climate"),
        terrain=request_body.get("terrain"),
        diameter=request_body.get("diameter"),
    )

    db.session.add(new_planet)
    db.session.commit()

    return jsonify({"msg": "Planet Created!!"}), 201

# ........................................................................................


@app.route('/characters', methods=['POST'])
def add_character():

    request_body = request.json

    if not request_body:
        return jsonify({"error": "Invalid input"}), 400

    new_character = Character(
        gender=request_body.get("gender"),
        height=request_body.get("height"),
        mass=request_body.get("mass"),
        eye_color=request_body.get("eye_color"),
        hair_color=request_body.get("hair_color"),
        skin_color=request_body.get("skin_color"),
        birth_year=request_body.get("birth_year"),
    )

    db.session.add(new_character)
    db.session.commit()

    return jsonify({"msg": "Character Created!!"}), 201

# ........................................................................................


@app.route('/vehicles', methods=['POST'])
def add_vehicle():

    request_body = request.json

    if not request_body:
        return jsonify({"error": "Invalid input"}), 400

    new_vehicle = Vehicle(
        model=request_body.get("model"),
        manufacturer=request_body.get("manufacturer"),
        vehicle_class=request_body.get("vehicle_class"),
        cost_in_credits=request_body.get("cost_in_credits"),
        length=request_body.get("length"),
        crew=request_body.get("crew"),
        passengers=request_body.get("passengers"),
        cargo_capacity=request_body.get("cargo_capacity"),
        max_atmosphering_speed=request_body.get("max_atmosphering_speed"),
        consumables=request_body.get("consumables"),
    )

    db.session.add(new_vehicle)
    db.session.commit()

    return jsonify({"msg": "Vehicle Created!!"}), 201

# .......................................... DELETE (PLANETS, CHARACTER, VEHICLES) ...........................................


@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):

    planet = Planet.query.get(planet_id)

    if not planet:
        return jsonify({"error": "Planet not found"}), 404

    existing_planet = Planet.query.filter_by(
        id=planet_id).first()

    db.session.delete(existing_planet)
    db.session.commit()

    return jsonify({"msg": "Planet deleted!"}), 201

# ........................................................................................


@app.route('/characters/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):

    character = Character.query.get(character_id)

    if not character:
        return jsonify({"error": "Character not found"}), 404

    existing_character = Character.query.filter_by(
        id=character_id).first()

    db.session.delete(existing_character)
    db.session.commit()

    return jsonify({"msg": "Character deleted!"}), 201

# ........................................................................................


@app.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):

    vehicle = Vehicle.query.get(vehicle_id)

    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404

    existing_vehicle = Vehicle.query.filter_by(
        id=vehicle_id).first()

    db.session.delete(existing_vehicle)
    db.session.commit()

    return jsonify({"msg": "Vehicle deleted!"}), 201


# .......................................... PUT (PLANETS, CHARACTER, VEHICLES) ...........................................

@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    request_body = request.json

    if not request_body:
        return jsonify({"error": "Invalid input"}), 400

    planet = Planet.query.get(planet_id)

    if not planet:
        return jsonify({"error": "Planet not found"}), 404

    planet.population = request_body.get("population", planet.population)
    planet.climate = request_body.get("climate", planet.climate)
    planet.terrain = request_body.get("terrain", planet.terrain)
    planet.diameter = request_body.get("diameter", planet.diameter)

    db.session.commit()

    return jsonify({"msg": "Planet updated!"}), 200

# ........................................................................................


@app.route('/characters/<int:character_id>', methods=['PUT'])
def update_character(character_id):
    request_body = request.json

    if not request_body:
        return jsonify({"error": "Invalid input"}), 400

    character = Character.query.get(character_id)

    if not character:
        return jsonify({"error": "Character not found"}), 404

    character.gender = request_body.get("gender", character.gender)
    character.height = request_body.get("height", character.height)
    character.mass = request_body.get("mass", character.mass)
    character.eye_color = request_body.get("eye_color", character.eye_color)
    character.hair_color = request_body.get("hair_color", character.hair_color)
    character.skin_color = request_body.get("skin_color", character.skin_color)
    character.birth_year = request_body.get("birth_year", character.birth_year)

    db.session.commit()

    return jsonify({"msg": "Character updated!"}), 200

# ........................................................................................


@app.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    request_body = request.json

    if not request_body:
        return jsonify({"error": "Invalid input"}), 400

    vehicle = Vehicle.query.get(vehicle_id)

    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404

    vehicle.model = request_body.get("model", vehicle.model)
    vehicle.manufacturer = request_body.get(
        "manufacturer", vehicle.manufacturer)
    vehicle.vehicle_class = request_body.get(
        "vehicle_class", vehicle.vehicle_class)
    vehicle.cost_in_credits = request_body.get(
        "cost_in_credits", vehicle.cost_in_credits)
    vehicle.length = request_body.get("length", vehicle.length)
    vehicle.crew = request_body.get("crew", vehicle.crew)
    vehicle.passengers = request_body.get("passengers", vehicle.passengers)
    vehicle.cargo_capacity = request_body.get(
        "cargo_capacity", vehicle.cargo_capacity)
    vehicle.max_atmosphering_speed = request_body.get(
        "max_atmosphering_speed", vehicle.max_atmosphering_speed)
    vehicle.consumables = request_body.get("consumables", vehicle.consumables)

    db.session.commit()

    return jsonify({"msg": "Vehicle updated!"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
