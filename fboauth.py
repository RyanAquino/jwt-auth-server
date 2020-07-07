"""
Facebook OAuth Module
"""
from flask import request, make_response, Blueprint
from helper import generate_token, generate_refresh_token, user_exist, register_user

fb_oauth_api = Blueprint('fb_oauth_api', __name__)


@fb_oauth_api.route('/fboauth', methods=['POST'])
def fboauth():
    user_info = request.json

    user_id = int(user_info['id'])
    username = user_info['email'].split('@')[0]

    if not user_exist(user_id):
        register_user(user_id, 'facebook', user_info['email'], username)

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
