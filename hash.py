from argon2 import PasswordHasher, exceptions


def hash_password(password):
    if not password:
        return
    ph = PasswordHasher()
    hashed = ph.hash(password)

    return hashed


def verify_password(password, db_pass):
    if not password:
        return

    ph = PasswordHasher()

    try:
        return ph.verify(password, db_pass)
    except (exceptions.VerifyMismatchError, exceptions.VerificationError, exceptions.InvalidHash) as err:
        return err
