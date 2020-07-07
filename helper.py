"""
Helper functions
"""
from datetime import datetime, timedelta
from config import JWT_REFRESH_SECRET, JWT_SECRET
import jwt
import database


def generate_token(data) -> bytes:
    """
    Generate JWT Token
    :param data: user data -> dict
    :return: token
    """
    if not data:
        return b''

    data['exp'] = datetime.utcnow() + timedelta(seconds=30)
    token = jwt.encode(data, JWT_SECRET)

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
    token = jwt.encode(data, JWT_REFRESH_SECRET)

    return token


def user_exist(user_id_token) -> bool:
    """
    Validate if user is in the database
    :param user_id_token: user provider token id
    :return: True/False if user exist in the db
    """
    query_user = database.query_one(f'SELECT * FROM users WHERE id_token={user_id_token}')

    if not query_user:
        return False

    return True


def register_user(user_id_token, provider, email, username) -> None:
    """
    Register user in the database

    :param user_id_token: user token generated from provider
    :param provider: google | facebook | Twitter | GitHub
    :param email: user email provided from provider
    :param username: username split from email '@'
    :return: None
    """
    user_data = {
        'id_token': user_id_token,
        'provider': provider,
        'email': email,
        'username': username
    }

    database.insert('INSERT INTO users (id_token, provider, email,username) VALUES (%(id_token)s, %(provider)s, %(email)s, %(username)s)', user_data)

