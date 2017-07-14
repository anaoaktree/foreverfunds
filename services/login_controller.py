from flask_login import LoginManager, UserMixin


login_manager = LoginManager()


# User class
class LoginUser(UserMixin):
    pass

