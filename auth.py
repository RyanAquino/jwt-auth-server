from datetime import datetime, timedelta
from flask import Flask, request, make_response
from flask_cors import CORS
from functools import wraps
import jwt
import database
import hash


def generate_token(data) -> bytes:
    """
    Generate JWT Token
    :param data: user data -> dict
    :return: token
    """
    if not data:
        return b''

    # data should be user id not username
    data['exp'] = datetime.utcnow() + timedelta(seconds=30)
    token = jwt.encode(data, 'secretkey')

    return token


def generate_refresh_token(data) -> bytes:
    """
    Generate refresh JWT Token
    :param data: user data -> dict
    :return: token
    """
    if not data:
        return b''

    data['exp'] = datetime.utcnow() + timedelta(minutes=1)
    token = jwt.encode(data, 'refresh_secret')

    return token


def auth_middleware(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        auth_token = None

        if 'authorization' in request.headers:
            auth_token = request.headers['authorization'].split(' ')
            if len(auth_token) > 1:
                auth_token = auth_token[1]

        if not auth_token: return make_response('Unauthorized', 401)

        try:
            decoded = jwt.decode(auth_token, 'secretkey', algorithm='HS256', options={'require_exp': True, 'verify_exp': True})

            return f(decoded, *args, **kwargs)

        except jwt.exceptions.ExpiredSignatureError:
            return make_response({'error':'Expired Token'}, 403)

        except BaseException:
            return make_response('Token Invalid', 400)

    return decorator


app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/refresh-token', methods=['POST'])
def re_token() -> bytes:
    """
    Cookies: refresh_token
    request.json: refresh_token
    :return: token
    """
    if 'refresh_token' not in request.cookies:
        return make_response('Unauthorized', 401)

    cookie_token = request.cookies['refresh_token']

    try:
        user_data = jwt.decode(cookie_token.encode(), 'refresh_secret', algorithm='HS256')
    except BaseException:
        return make_response('Token Invalid', 400)

    user = database.query_one(f'SELECT * FROM users WHERE username="{user_data["Username"]}"')

    if not user:
        return make_response('Forbidden', 403)

    token = generate_token({'Username': user['username']})
    refresh_token = generate_refresh_token({'Username': user['username']})

    payload = {
        'token': token.decode(),
        'refresh_token': refresh_token.decode()
    }

    res = make_response(payload)
    res.set_cookie(key='refresh_token', value=payload['refresh_token'], httponly=True, path='/refresh-token')

    return res


@app.route('/login', methods=['POST'])
def login() -> dict:
    """
    Login / Set cookie and generate token
    :return: res
    """
    if not request.form or ('username' not in request.form or 'password' not in request.form):
        return make_response({'Error': 'Bad Request'}, 400)

    user_data = request.form
    user = user_data['username']
    password = user_data['password']

    query_user = database.query_one(f'SELECT * FROM users WHERE username="{user}"')

    if not query_user:
        return make_response({'Error': 'Invalid login'}, 401)

    verify_password = hash.verify_password(query_user['password'], password)

    # Must be TRUE
    if verify_password != True:
        return make_response({'Error': 'Password does not match'}, 401)

    refresh_token = generate_refresh_token({'Username': query_user['username']})
    token = generate_token({'Username': query_user['username']})

    payload = {
        'token': token.decode(),
        'refresh_token': refresh_token.decode()
    }

    res = make_response(payload)
    res.set_cookie(key='refresh_token', value=payload['refresh_token'], domain='127.0.0.1', path='/refresh-token')

    return res


@app.route('/logout', methods=['DELETE'])
def delete_token():
    res = make_response('')
    res.delete_cookie(key='refresh_token', path='/refresh-token', domain='127.0.0.1')
    # Does not invalidate all the past refresh token, only the current token at cookies

    return res


@app.route('/protected', methods=['GET'])
@auth_middleware
def protected(data):

    result = database.query_all(f'SELECT * FROM posts WHERE user_id=2')
    # Change to user id

    data = [
        {
            'id1':1,
            'Title':'test1',
            'Body':'Post1'
        },
        {
            'id1': 2,
            'Title': 'test2',
            'Body': 'Post2'
        },
        {
            'id1': 3,
            'Title': 'test3',
            'Body': 'Post3'
        },
        {
            'id': data
        }
    ]

    return make_response({'posts': data, 'query':result}, 200)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
