"""
Hashing Module utilizing Argon2 hash
"""
from argon2 import PasswordHasher, exceptions


def hash_password(password):
    """
    Hash Password
    :param password: password to be hashed
    :return: hashed password
    """
    if not password:
        return
    ph = PasswordHasher()
    hashed = ph.hash(password)

    return hashed


def verify_password(password, db_pass):
    """
    Verify password match

    :param password: password to be checked
    :param db_pass: password saved on Database
    :return: True / False if password matched
    """
    if not password:
        return

    ph = PasswordHasher()

    try:
        return ph.verify(password, db_pass)
    except (exceptions.VerifyMismatchError, exceptions.VerificationError, exceptions.InvalidHash) as err:
        return err
