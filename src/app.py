from flask import Flask, request, jsonify, json
from flask_migrate import Migrate
from models import db, User

import os

app = Flask(__name__)
app.config['DEBUG'] = True # Para poder depurar los errores
app.config['ENV'] = 'development' # Entorno de desarrollo
app.config['SQLALCHEMY_TRACK_MODIFICACIONS'] = False # Control de Cambios en SQLAlchemy
#app.config['SQLALCHEMY_DATABASE_URI'] = "dialect+driver://<user>:<pass>@<host>:<port>/<dbname>"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root@localhost:3306/prueba" # Conexion a la base de datos
#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

db.init_app(app) # vinculo entre mi app y mis modelos de la base de datos
Migrate(app, db) # db init, db migrate, db upgrade || db downgrade


@app.route('/', methods=['GET'])
def main():
    return "REST API"


@app.route('/api/users', methods=['GET']) # lista todos los usuario existentes
def list_users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))
    return jsonify(users)


@app.route('/api/users', methods=['POST']) # endpoint para crear un usuario nuevo 
def store_user():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User()
    user.username = username
    user.password = password

    # Guardamos el usuario 
    user.save()

    return jsonify(user.serialize()), 201


@app.route('/api/users/<int:id>', methods=['PUT']) # endpoint para actualizar un usuario determinado
def update_user(id):
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.get(id)
    user.username = username
    user.password = password

    # Guardamos el usuario 
    user.update()

    return jsonify(user.serialize()), 200


@app.route('/api/users/search', methods=['GET']) # endpoint para busqueda filtrando por query_string /users/searh/?username=ped
def search_users():
    search = request.args # obtener todos los parametros en el url
    print(search['username']) # imprimiendo el parametro username
    users = User.query.filter(User.username.ilike('%'+search['username']+'%')) # Obteniendo todos los usuarios que contenga el texto indicado en el username
    users = list(map(lambda user: user.serialize(), users)) # convertir todos los objetos de python en un objeto serializable (diccionario)

    return jsonify(users), 200 # retornamos el resultado de la busqueda


@app.route('/api/users/status/<status>', methods=['GET']) # endpoint busca los usuarios por status o valor del campo verified (recibe activos o inactivos)
def users_by_status(status):
    verified = True if status == 'activos' else False # Operador Ternario Python
    users = User.query.filter_by(verified=verified) # [<User 1>, <User 2>]
    #print(users)
    users = list(map(lambda user: user.serialize(), users))
    #print(users)
    return jsonify(users), 200 

if __name__ == '__main__':
    app.run()
