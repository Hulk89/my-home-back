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
        session = db.SESSION()
        result = str(session.query(models.Todo).all())
        session.close()
        return result


    @todo.route("/put", methods=('POST', ))
    @token_required_w_secret_key
    def put():
        data = request.get_json()
        session = db.SESSION()
        session.add(models.Todo(data["title"],
                                data["description"],
                                models.TodoState.todo))
        session.commit()
        session.close()
        return "Good"

    return todo

