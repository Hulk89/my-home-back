from flask import jsonify, request 
from functools import wraps
import jwt
from datetime import datetime, timedelta

from models import database as db
from models import models

def token_required(f, secret_key):
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
            data = jwt.decode(token, secret_key)
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


def encode_jwt(user, secret_key):
    token = jwt.encode({
                    'sub': user,
                    'iat': datetime.utcnow(),
                    'exp': datetime.utcnow() + timedelta(minutes=30)},
                secret_key)
    return token

