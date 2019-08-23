from flask import jsonify, request, escape, send_file
from flask import Blueprint
from functools import partial
import os

from routes.verify import token_required

def make_comics_blueprint(comics_folder_path, secret_key):
    comics = Blueprint('comics', __name__)
    token_required_w_secret_key = partial(token_required, secret_key=secret_key)

    @comics.route("/list", methods=('GET', ))
    @token_required_w_secret_key
    def get_comics_list():
        return jsonify(os.listdir(comics_folder_path))


    @comics.route("/episode_list/<comic_title>", methods=('GET', ))
    @token_required_w_secret_key
    def get_comic_list(comic_title):
        comic_folder = os.path.join(comics_folder_path, escape(comic_title))
        comic_list = os.listdir(comic_folder)
        comic_list.sort()
        return jsonify(comic_list)


    @comics.route("/image_list", methods=('POST', ))
    @token_required_w_secret_key
    def get_image_list():
        def get_int_value(image_filename):
            s = ''.join(x for x in image_filename if x.isdigit())
            return int(s)
        data = request.get_json()
        comic_title, episode_id = data["title"], data["ep_id"]

        comic_folder = os.path.join(comics_folder_path, escape(comic_title))
        image_list = os.listdir(os.path.join(comic_folder, episode_id))
        image_list.sort(key=lambda x: get_int_value(x))
        
        return jsonify(image_list)


    @comics.route("/image", methods=('POST', ))
    @token_required_w_secret_key
    def get_image():
        data = request.get_json()
        comic_title, episode_id, filename = data["title"], data["ep_id"], data["img_filename"]

        comic_folder = os.path.join(comics_folder_path, escape(comic_title))
        episode_folder = os.path.join(comic_folder, episode_id)
        image_file = os.path.join(episode_folder, filename)

        return send_file(image_file)

    return comics
