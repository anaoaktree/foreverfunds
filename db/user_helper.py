from services.login_service import validate_password, hashing
from db.entities import db, User


# db change methods
def add_user(username, password,email, permissions):
    hashed_password = hashing(password)
    user = User(username, hashed_password,email, permissions)
    db.session.add(user)
    db.session.commit() ## TODO: optimise this by only saving when user leaves the page (for bulk user adding)


def change_password(user, old_password, new_password1, new_password2):
    if validate_password(user, old_password):
        if new_password1 == new_password2:
            user.setPassword(hashing(new_password1))
            db.session.commit()
            return True, "Successfuly changed the password"
        else:
            return False, "Passwords don't match!"
    else:
        return False, "Wrong password!"

