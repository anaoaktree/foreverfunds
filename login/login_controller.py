from flask_login import LoginManager, UserMixin
from hashlib import sha256

login_manager = LoginManager()


# validation functions
def validate_login(user, password):
    hashed_password = hashing(password)
    return hashed_password == user.password


def hashing(password):
    hashed_password = sha256(password.encode('utf-8'))
    return hashed_password.hexdigest()


# User class

class LoginUser(UserMixin):
    pass

