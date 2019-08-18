# -- coding: utf-8 --
from flask import Flask, jsonify, request, escape, send_file
from flask_cors import CORS
import json
import argparse
import os

from config import Config
from models import database as db
from models import models
from routes.verify import token_required, encode_jwt
from routes.comics import comics

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/login', methods=('POST',))
def login():
    data = request.get_json()
    if models.User.check_password(db.SESSION,
                                  data['user'],
                                  data['password']):
        print("login success")
        token = encode_jwt(data['user'])
        return jsonify({'token': token.decode('UTF-8')})
    else:
        return jsonify({'message': 'Invalid credentials',
                        'authenticated': False}), 401
@app.route("/select", methods=('GET', ))
@token_required
def select():
    print(db.SESSION.query(models.Todo).all())
    return str(db.SESSION.query(models.Todo).all())

@app.route("/put", methods=('POST', ))
@token_required
def put():
    data = request.get_json()
    db.SESSION.add(models.Todo(data["title"],
                               data["description"],
                               models.TodoState.todo))
    db.SESSION.commit()
    return "Good"


app.register_blueprint(comics, url_prefix='/comics')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="my-home-backend")
    parser.add_argument("--config", required=True)
    parser.add_argument("--folder_path", required=True)
    args = parser.parse_args()

    app.config.from_object(Config)
    app.config["data_folder_path"] = args.folder_path
    CORS(app)
    with open(args.config) as f:
        db_config = json.loads(f.read())
    # sqlalchemy 세팅
    db.initialize(**db_config)

    app.run()

