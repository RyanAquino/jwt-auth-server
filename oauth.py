"""
Google OAuth Module
"""
from google.oauth2 import id_token
from google.auth.transport import requests
from flask import request, make_response, Blueprint
from helper import generate_token, generate_refresh_token, user_exist, register_user
import time

oauth_api = Blueprint('oauth_api', __name__)


@oauth_api.route('/oauth', methods=['POST'])
def oauth():

    try:
        token = request.form.get('id_token')
        GOOGLE_CLIENT_ID = '81239065828-vimeqa555r7tmhut5f3erii0ukt22kti.apps.googleusercontent.com'
        id_info = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        token_expiry = id_info['exp']

        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            return make_response({'Error': 'Wrong issuer'}, 401)

        if id_info['aud'] != GOOGLE_CLIENT_ID:
            return make_response({'Error': 'Wrong aud'}, 401)

        if token_expiry <= time.time():
            return make_response({'Error': 'Token expired'}, 403)

        user_id_token = int(id_info['sub'])
        email = id_info['email']
        username = id_info['email'].split('@')[0]

        if not user_exist(user_id_token):
            register_user(user_id_token, 'google', email, username)

        oauth_token = generate_token({'id': int(user_id_token)})
        oauth_refresh = generate_refresh_token({'id': user_id_token})

        payload = {
            'token': oauth_token.decode(),
            'refresh_token': oauth_refresh.decode()
        }

        res = make_response(payload)
        res.set_cookie(key='refresh_token', value=payload['refresh_token'], httponly=True, domain='127.0.0.1',
                       path='/refresh-token')

        # samesite = 'Lax' Google API 127.0.0.1 not working

        return res

    except ValueError:
        return make_response('invalid token', 400)
