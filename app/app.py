# -- coding: utf-8 --
from flask import Flask, jsonify, request, escape, send_file
from flask_cors import CORS
import json
import argparse
import os

from config import Config
from models import database as db
from models import models
from routes.verify import encode_jwt
from routes.comics import make_comics_blueprint
from routes.todo import make_todo_blueprint

def make_routes(data_path, config):
    app = Flask(__name__)

    app.config.from_object(Config)
    CORS(app)
    with open(config) as f:
        db_config = json.loads(f.read())
    # sqlalchemy 세팅
    db.initialize(**db_config)

    @app.route("/")
    def hello():
        return "Hello World!"

    # TODO: login도 blueprint로 빼자
    @app.route('/login', methods=('POST',))
    def login():
        data = request.get_json()
        if models.User.check_password(db.SESSION,
                                    data['user'],
                                    data['password']):
            print("login success")
            token = encode_jwt(data['user'],
                               app.config["SECRET_KEY"])
            return jsonify({'token': token.decode('UTF-8')})
        else:
            return jsonify({'message': 'Invalid credentials',
                            'authenticated': False}), 401

    comics_blueprint = make_comics_blueprint(data_path, app.config["SECRET_KEY"])
    todo_blueprint = make_todo_blueprint(app.config["SECRET_KEY"])

    app.register_blueprint(comics_blueprint, url_prefix='/comics')
    app.register_blueprint(todo_blueprint, url_prefix='/todo')

    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="my-home-backend")
    parser.add_argument("--config", required=True)
    parser.add_argument("--folder_path", required=True)
    parser.add_argument("--ip", default=None)
    parser.add_argument("--port", default=5000)
    args = parser.parse_args()

    app = make_routes(args.folder_path, args.config)
    app.run(host=args.ip, port=args.port)

