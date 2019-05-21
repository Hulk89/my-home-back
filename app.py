from flask import Flask, jsonify, request
from flask_cors import CORS
import jwt
import json
import sys
from login import Login
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

with open(sys.argv[1]) as f:
    config = json.loads(f.read())

login_db = Login(**config)

SECRET_KEY = config['secret_key']

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/login', methods=('POST',))
def login():
    data = request.get_json()
    if login_db.login(data['user'],
                      data['password']):
        print("login success")
        token = jwt.encode({
            'sub': data['user'],
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=30)},
          SECRET_KEY)
        return jsonify({'token': token.decode('UTF-8')})
    else:
        return jsonify({'message': 'Invalid credentials',
                        'authenticated': False}), 401

def token_required(f):
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
            data = jwt.decode(token, SECRET_KEY)
            return f(data['sub'], *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify

@token_required
@app.route("/download", methods=('POST', ))
def download(name):
    data = request.get_json()
    print(data)


if __name__ == "__main__":
    app.run()
