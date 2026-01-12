from __future__ import annotations
from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    # favoritos
    favorite_planets: Mapped[List["FavoritePlanet"]] = relationship(back_populates="user")
    favorite_vehicles: Mapped[List["FavoriteVehicle"]] = relationship(back_populates="user")
    favorite_droids: Mapped[List["FavoriteDroid"]] = relationship(back_populates="user")
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
        }


class Vehicle(db.Model):
    __tablename__ = "vehicles"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    model: Mapped[str] = mapped_column(String(200), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    # Favoritos
    favorited_by: Mapped[List["FavoriteVehicle"]] = relationship(back_populates="vehicle")

    def serialize(self):
        return {
            "id": self.id,
            "model": self.model,
            "user_id": self.user_id
        }


class Planet(db.Model):
    __tablename__ = "planets"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    population: Mapped[int] = mapped_column(Integer, nullable=True)
    size: Mapped[str] = mapped_column(String(100), nullable=False)

    # favorios
    favorited_by: Mapped[List["FavoritePlanet"]] = relationship(back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "size": self.size
        }


class Droid(db.Model):
    __tablename__ = "droids"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    model: Mapped[str] = mapped_column(String(200), nullable=False)
    creator: Mapped[str] = mapped_column(String(200), nullable=False)

    #Favoritos
    favorited_by: Mapped[List["FavoriteDroid"]] = relationship(back_populates="droid")

    def serialize(self):
        return {
            "id": self.id,
            "model": self.model,
            "creator": self.creator
        }


#tablas muchos a varios

class FavoriteVehicle(db.Model):
    __tablename__ = "favorite_vehicles"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"))

    # Relaciones
    user: Mapped["User"] = relationship(back_populates="favorite_vehicles")
    vehicle: Mapped["Vehicle"] = relationship(back_populates="favorited_by")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "vehicle_id": self.vehicle_id
        }


class FavoritePlanet(db.Model):
    __tablename__ = "favorite_planets"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    planets_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))

    #Relaciones
    user: Mapped["User"] = relationship(back_populates="favorite_planets")
    planet: Mapped["Planet"] = relationship(back_populates="favorited_by")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planets_id": self.planets_id
        }


class FavoriteDroid(db.Model):
    __tablename__ = "favorite_droids"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    droid_id: Mapped[int] = mapped_column(ForeignKey("droids.id"))

    # relaciones
    user: Mapped["User"] = relationship(back_populates="favorite_droids")
    droid: Mapped["Droid"] = relationship(back_populates="favorited_by")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "droid_id": self.droid_id
        }