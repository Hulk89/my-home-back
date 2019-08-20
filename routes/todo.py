from flask import jsonify, request, escape, send_file
from flask import Blueprint
from functools import partial
from routes.verify import token_required
from models import database as db
from models import models


def make_todo_blueprint(secret_key):
    todo = Blueprint('todo', __name__)
    token_required_w_secret_key = partial(token_required,
                                          secret_key=secret_key)

    @todo.route("/select", methods=('GET', ))
    @token_required_w_secret_key
    def select():
        return str(db.SESSION.query(models.Todo).all())


    @todo.route("/put", methods=('POST', ))
    @token_required_w_secret_key
    def put():
        data = request.get_json()
        db.SESSION.add(models.Todo(data["title"],
                                   data["description"],
                                   models.TodoState.todo))
        db.SESSION.commit()
        return "Good"

    return todo

