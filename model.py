import json

import jwt

import db

ALGORITHM = 'HS256'
jwt_secret_key = "zbQzq1OWae"


def verify_jwt_token(jwt_token):
    try:
        payload = jwt.decode(jwt_token, jwt_secret_key, ALGORITHM)
        user_id = payload['user_id']
        response = db.get_user_by_id(user_id)
        valid_user = response
        print('valid_user: ',valid_user)
        if valid_user:
            return json.dumps({'user_id': user_id, 'valid': True}), 200
        else:
            json.dumps({'message': 'Invalid token'}), 401
    except jwt.ExpiredSignatureError:
        return json.dumps({'message': 'Token has expired'}), 401

    except jwt.InvalidTokenError:
        return json.dumps({'message': 'Invalid token'}), 401


def generate_jwt_token(user_id):
    payload = {
        'user_id': user_id,
    }
    token = jwt.encode(payload, jwt_secret_key, ALGORITHM)
    return token
