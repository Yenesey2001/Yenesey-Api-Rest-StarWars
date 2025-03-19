from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Boolean, Integer

db = SQLAlchemy()

character_vehicles = db.Table(
    "character_vehicles",
    db.Column("character_id", ForeignKey("characters.id"), primary_key=True),
    db.Column("vehicle_id", ForeignKey("vehicles.id"), primary_key=True)
)


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    firstname: Mapped[str] = mapped_column(String(20), nullable=False)
    lastname: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)

    favourites = relationship("Favourites", back_populates="user")

    def serialize_user(self):
        return ({
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
        }
        )


class Character(db.Model):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    height: Mapped[int] = mapped_column(Integer)
    mass: Mapped[int] = mapped_column(Integer)
    eye_color: Mapped[str] = mapped_column(String(10), nullable=False)
    hair_color: Mapped[str] = mapped_column(String(10), nullable=False)
    skin_color: Mapped[str] = mapped_column(String(10), nullable=False)
    birth_year: Mapped[str] = mapped_column(String(10))

    homeworld_id: Mapped[int] = mapped_column(
        ForeignKey("planets.id"), nullable=True)
    homeworld = relationship("Planet", back_populates="residents")

    vehicles = relationship(
        "Vehicle", secondary=character_vehicles, back_populates="pilots")

    def serialize(self):
        return ({
            "id": self.id,
            "gender": self.gender,
            "height": self.height,
            "mass": self.mass,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "birth_year": self.birth_year,
        }
        )


class Planet(db.Model):
    __tablename__ = "planets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    population: Mapped[int] = mapped_column(Integer)
    climate: Mapped[str] = mapped_column(String(20), nullable=False)
    terrain: Mapped[str] = mapped_column(String(20), nullable=False)
    diameter: Mapped[int] = mapped_column(Integer)

    residents = relationship("Character", back_populates="homeworld")

    def serialize_planet(self):
        return ({
            "id": self.id,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "diameter": self.diameter
        }
        )


class Vehicle(db.Model):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    model: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False)  # Aumentado
    manufacturer: Mapped[str] = mapped_column(
        String(100), nullable=False)  # Aumentado
    vehicle_class: Mapped[str] = mapped_column(
        String(100), nullable=False)  # Aumentado
    cost_in_credits: Mapped[int] = mapped_column(Integer)
    length: Mapped[int] = mapped_column(Integer)
    crew: Mapped[int] = mapped_column(Integer)
    passengers: Mapped[int] = mapped_column(Integer)
    cargo_capacity: Mapped[int] = mapped_column(Integer)
    max_atmosphering_speed: Mapped[int] = mapped_column(Integer)
    consumables: Mapped[str] = mapped_column(
        String(50))  # Aumentado por seguridad

    pilots = relationship(
        "Character", secondary=character_vehicles, back_populates="vehicles")

    def serialize_vehicle(self):
        return ({
            "id": self.id,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "vehicle_class": self.vehicle_class,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,
            "cargo_capacity": self.cargo_capacity,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "consumables": self.consumables,
        }
        )


class Favourites(db.Model):
    __tablename__ = "favourites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(
        ForeignKey("planets.id"), nullable=True)
    character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.id"), nullable=True)
    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id"), nullable=True)

    user = relationship("User", back_populates="favourites")
    planet = relationship("Planet")
    character = relationship("Character")
    vehicle = relationship("Vehicle")

    def serialize_favourites(self):

        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id if self.planet_id else None,
            "character_id": self.character_id if self.character_id else None,
            "vehicle_id": self.vehicle_id if self.vehicle_id else None,
        }
