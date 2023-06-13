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
from models import db, User, Planet

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all() #devuelve una lista[] del modelo a devolver, es decir el modelo.
    result = list(map(lambda item: item.serialize(), all_users))
    return jsonify(result), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    print(user_id)
    user = User.query.filter_by(id=user_id)
    print(user)
    return jsonify(user.serialize()), 200

@app.route('/planet', methods=['GET'])
def get_planets():
    all_planets = Planet.query.all() #devuelve una lista[] del modelo a devolver, es decir el modelo.
    result = list(map(lambda item: item.serialize(), all_planets))
    return jsonify(result), 200

# @app.route('/people', methods=['GET'])
# def get_people():
#     all_people = People.query.all() #devuelve una lista[] del modelo a devolver, es decir el modelo.
#     result = list(map(lambda item: item.serialize(), all_people))
#     return jsonify(result), 200

# @app.route('/people', methods=['POST'])
# def create_planet():
#     body = request.get_json()
#     planet = Planet(planet_name = body["planet_name"],population = body["population"])
#     db.session.add(planet) #agrega el registro a la tabla
#     db.session.commit() #guarda los cambios

#     print(request.get_json())
#     response_body = {
#         "msg":"se creo planet"
#     }

#     return jsonify(response_body), 200 

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
