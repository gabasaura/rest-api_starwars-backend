import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, User, Categoria, Planet, People, Favorite

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///starwars_api.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# Inicializa Flask-Migrate
migrate = Migrate(app, db)


@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def main():
    data = {
        "msg": "Blog StarWars"
    }
    return jsonify(data), 200

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    
    # Validar la entrada
    if not data or 'username' not in data or 'email' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    # Crear un nuevo usuario
    new_user = User(
        username=data['username'],
        email=data['email'],
        admin=data.get('admin', False),
        active=data.get('active', True)
    )
    
    try:
        # Agregar y guardar en la base de datos
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200


@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    return jsonify([person.serialize() for person in people]), 200

@app.route('/people', methods=['POST'])
def create_person():
    data = request.json
    
    # Validar la entrada
    if not data or 'name' not in data or 'categoria_type' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    # Crear una nueva persona
    new_person = People(
        name=data['name'],
        categoria_type=data['categoria_type'],
        birth_year=data.get('birth_year'),
        eye_color=data.get('eye_color'),
        gender=data.get('gender'),
        hair_color=data.get('hair_color'),
        height=data.get('height'),
        mass=data.get('mass'),
        skin_color=data.get('skin_color'),
        homeworld_id=data.get('homeworld_id'),
        species=data.get('species'),
        starships=data.get('starships'),
        vehicles=data.get('vehicles')
    )
    
    try:
        # Agregar y guardar en la base de datos
        db.session.add(new_person)
        db.session.commit()
        return jsonify(new_person.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/people/<int:id>', methods=['DELETE'])
def delete_person(id):
    person = People.query.get(id)
    if person:
        try:
            db.session.delete(person)
            db.session.commit()
            return jsonify({'message': 'Person deleted'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Person not found'}), 404


@app.route('/planet', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route('/planet', methods=['POST'])
def create_planet():
    data = request.json
    
    # Validar la entrada
    if not data or 'name' not in data or 'categoria_type' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    # Crear un nuevo planeta
    new_planet = Planet(
        name=data['name'],
        categoria_type=data['categoria_type'],
        climate=data.get('climate'),
        diameter=data.get('diameter'),
        gravity=data.get('gravity'),
        orbital_period=data.get('orbital_period'),
        population=data.get('population'),
        rotation_period=data.get('rotation_period'),
        surface_water=data.get('surface_water'),
        terrain=data.get('terrain')
    )
    
    try:
        # Agregar y guardar en la base de datos
        db.session.add(new_planet)
        db.session.commit()
        return jsonify(new_planet.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/planet/<int:id>', methods=['DELETE'])
def delete_planet(id):
    planet = Planet.query.get(id)
    if planet:
        try:
            db.session.delete(planet)
            db.session.commit()
            return jsonify({'message': 'Planet deleted'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Planet not found'}), 404


@app.route('/user/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify([favorite.serialize() for favorite in favorites]), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite(people_id=None, planet_id=None):
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    
    if people_id:
        favorite = Favorite(user_id=user_id, categoria_type='people', categoria_item_id=people_id)
    elif planet_id:
        favorite = Favorite(user_id=user_id, categoria_type='planet', categoria_item_id=planet_id)
    else:
        return jsonify({"error": "Favorite type is required"}), 400
    
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify(favorite.serialize()), 201

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite(people_id=None, planet_id=None):
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    if people_id:
        favorite = Favorite.query.filter_by(user_id=user_id, categoria_type='people', categoria_item_id=people_id).first()
    elif planet_id:
        favorite = Favorite.query.filter_by(user_id=user_id, categoria_type='planet', categoria_item_id=planet_id).first()
    else:
        return jsonify({"error": "Favorite type is required"}), 400

    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite removed"}), 200


"""
# Ejemplo de creación de usuario directamente en app.py
@app.route('/create_test_user', methods=['POST'])
def create_test_user():
    with app.app_context():
        user = User(username="user_beta", email="email@starwars.test", admin=False, active=True)
        db.session.add(user)
        db.session.commit()
        return jsonify(user.serialize()), 201

"""

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()