# -- coding: utf-8 --
from flask import Flask, jsonify, request, escape, send_file
from flask_cors import CORS
import jwt
import json
from datetime import datetime, timedelta
from functools import wraps
import argparse
import os

from config import Config
from models import database as db
from models import models

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
        token = jwt.encode({
            'sub': data['user'],
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=30)},
          app.config["SECRET_KEY"])
        return jsonify({'token': token.decode('UTF-8')})
    else:
        return jsonify({'message': 'Invalid credentials',
                        'authenticated': False}), 401

def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()
        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }
        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401
        try:
            token = auth_headers[1]
            data = jwt.decode(token, app.config["SECRET_KEY"])
            user = db.SESSION.query(models.User).filter_by(name=data['sub']).first()
            if not user:
                raise RuntimeError("User not found")
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401
    return _verify

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

# Comics 관련
@app.route("/comics_list", methods=('GET', ))
@token_required
def get_comics_list():
    return jsonify(os.listdir(app.config["data_folder_path"]))

@app.route("/comic_list/<comic_title>", methods=('GET', ))
@token_required
def get_comic_list(comic_title):
    data_path = app.config["data_folder_path"]
    comic_folder = os.path.join(data_path, escape(comic_title))
    comic_list = os.listdir(comic_folder)
    comic_list.sort()
    return jsonify(comic_list)

@app.route("/comic/image_list", methods=('POST', ))
@token_required
def get_image_list():
    def get_int_value(image_filename):
        s = ''.join(x for x in image_filename if x.isdigit())
        return int(s)
    data_path = app.config["data_folder_path"]
    data = request.get_json()
    comic_title, episode_id = data["title"], data["ep_id"]

    comic_folder = os.path.join(data_path, escape(comic_title))
    image_list = os.listdir(os.path.join(comic_folder, episode_id))
    image_list.sort(key=lambda x: get_int_value(x))
    
    return jsonify(image_list)

@app.route("/comic/image", methods=('POST', ))
@token_required
def get_image():
    data_path = app.config["data_folder_path"]
    data = request.get_json()
    comic_title, episode_id, filename = data["title"], data["ep_id"], data["img_filename"]

    comic_folder = os.path.join(data_path, escape(comic_title))
    episode_folder = os.path.join(comic_folder, episode_id)
    image_file = os.path.join(episode_folder, filename)

    return send_file(image_file)



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

