from google.oauth2 import id_token
from google.auth.transport import requests
from flask import Flask, request, make_response
from flask_cors import CORS
from auth import generate_token, generate_refresh_token
import database
import time

app = Flask(__name__)
CORS(app, supports_credentials=True)


def user_exist(google_id):
    query_user = database.query_one(f'SELECT * FROM users WHERE id={google_id}')

    if not query_user:
        return False

    return True


def register_user(user_data):
    database.insert('INSERT INTO users (id, email,username) VALUES (%(id)s, %(email)s, %(username)s)', user_data)

    return True

@app.route('/oauth', methods=['POST'])
def oauth():
    try:
        token = request.form.get('id_token')

        idinfo = id_token.verify_oauth2_token(token, requests.Request(), '81239065828-vimeqa555r7tmhut5f3erii0ukt22kti.apps.googleusercontent.com')

        token_expiry = idinfo['exp']

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            return make_response({'Error': 'Wrong issuer'}, 401)

        if idinfo['aud'] != '81239065828-vimeqa555r7tmhut5f3erii0ukt22kti.apps.googleusercontent.com':
            return make_response({'Error': 'Wrong aud'}, 401)

        if token_expiry <= time.time():
            return make_response({'Error': 'Token expired'}, 403)

        user_id = idinfo['sub']
        email = idinfo['email']
        username = idinfo['email'].split('@')[0]

        if user_exist(user_id):
            user_data = {
                'id': user_id,
                'email': email,
                'username': username
            }
            register_user(user_data)

        oauth_token = generate_token({'id': user_id})
        oauth_refresh = generate_refresh_token({'id': user_id})

        payload = {
            'token': oauth_token.decode(),
            'refresh_token': oauth_refresh.decode()
        }

        res = make_response(payload)
        res.set_cookie(key='refresh_token', value=payload['refresh_token'], httponly=True, domain='127.0.0.1',
                       path='/refresh-token')

        return res

    except ValueError:
        return make_response('invalid token', 400)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')

