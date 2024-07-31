from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    admin = Column(Boolean, default=False)
    active = Column(Boolean, default=True)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'admin': self.admin,
            'active': self.active
        }

class Categoria(db.Model):
    __tablename__ = 'categoria'
    id = Column(Integer, primary_key=True)
    categoria_type = Column(String(50), unique=True, nullable=False)  # 'planet' or 'people'

    def serialize(self):
        return {
            'id': self.id,
            'categoria_type': self.categoria_type
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = Column(Integer, primary_key=True)
    categoria_type = Column(String(50), ForeignKey('categoria.categoria_type'), nullable=False)
    name = Column(String(250), nullable=False)
    climate = Column(String(250), nullable=True)
    diameter = Column(String(250), nullable=True)
    gravity = Column(String(250), nullable=True)
    orbital_period = Column(String(250), nullable=True)
    population = Column(String(250), nullable=True)
    rotation_period = Column(String(250), nullable=True)
    surface_water = Column(String(250), nullable=True)
    terrain = Column(String(250), nullable=True)
    categoria = relationship('Categoria', backref='planets', foreign_keys=[categoria_type])

    def serialize(self):
        return {
            'id': self.id,
            'categoria_type': self.categoria_type,
            'name': self.name,
            'climate': self.climate,
            'diameter': self.diameter,
            'gravity': self.gravity,
            'orbital_period': self.orbital_period,
            'population': self.population,
            'rotation_period': self.rotation_period,
            'surface_water': self.surface_water,
            'terrain': self.terrain
        }

class People(db.Model):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    categoria_type = Column(String(50), ForeignKey('categoria.categoria_type'), nullable=False)
    name = Column(String(250), nullable=False)
    birth_year = Column(String(250), nullable=True)
    eye_color = Column(String(250), nullable=True)
    gender = Column(String(250), nullable=True)
    hair_color = Column(String(250), nullable=True)
    height = Column(String(250), nullable=True)
    mass = Column(String(250), nullable=True)
    skin_color = Column(String(250), nullable=True)
    homeworld_id = Column(Integer, ForeignKey('planet.id'), nullable=True)
    homeworld = relationship('Planet', backref='residents', foreign_keys=[homeworld_id])
    species = Column(String(250), nullable=True)
    starships = Column(String(250), nullable=True)
    vehicles = Column(String(250), nullable=True)
    categoria = relationship('Categoria', backref='peoples', foreign_keys=[categoria_type])

    def serialize(self):
        return {
            'id': self.id,
            'categoria_type': self.categoria_type,
            'name': self.name,
            'birth_year': self.birth_year,
            'eye_color': self.eye_color,
            'gender': self.gender,
            'hair_color': self.hair_color,
            'height': self.height,
            'mass': self.mass,
            'skin_color': self.skin_color,
            'homeworld_id': self.homeworld_id,
            'species': self.species,
            'starships': self.starships,
            'vehicles': self.vehicles
        }

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    categoria_type = Column(String(50), ForeignKey('categoria.categoria_type'), nullable=False)
    categoria_item_id = Column(Integer, nullable=False)
    user = relationship('User', backref='favorites')
    categoria = relationship('Categoria', backref='favorites', foreign_keys=[categoria_type])

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'categoria_type': self.categoria_type,
            'categoria_item_id': self.categoria_item_id
        }
