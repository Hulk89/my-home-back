from flask import jsonify, request, escape, send_file
from flask import Blueprint
from flask import current_app as app
import os

from routes.verify import token_required

comics = Blueprint('comics', __name__)

@comics.route("/list", methods=('GET', ))
@token_required
def get_comics_list():
    return jsonify(os.listdir(app.config["data_folder_path"]))


@comics.route("/episode_list/<comic_title>", methods=('GET', ))
@token_required
def get_comic_list(comic_title):
    data_path = app.config["data_folder_path"]
    comic_folder = os.path.join(data_path, escape(comic_title))
    comic_list = os.listdir(comic_folder)
    comic_list.sort()
    return jsonify(comic_list)


@comics.route("/image_list", methods=('POST', ))
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


@comics.route("/image", methods=('POST', ))
@token_required
def get_image():
    data_path = app.config["data_folder_path"]
    data = request.get_json()
    comic_title, episode_id, filename = data["title"], data["ep_id"], data["img_filename"]

    comic_folder = os.path.join(data_path, escape(comic_title))
    episode_folder = os.path.join(comic_folder, episode_id)
    image_file = os.path.join(episode_folder, filename)

    return send_file(image_file)


