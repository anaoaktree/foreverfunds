import random
from hashlib import sha256
from db.entities import db, User


# password validation functions
def validate_password(user, password):
    hashed_password = hashing(password)
    return hashed_password == user.password


def hashing(password):
    hashed_password = sha256(password.encode('utf-8'))
    return hashed_password.hexdigest()


# db change methods
def add_user(username, password, permissions):
    hashed_password = hashing(password)
    user = User(username, hashed_password, permissions)
    db.session.add(user)
    db.session.commit()


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


# This function generates a password with 10 characters, with numbers, and lower and upper case letters
def password_generator():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    pw_length = 10
    new_password = ""

    for i in range(pw_length):
        next_index = random.randrange(len(alphabet))
        new_password = new_password + alphabet[next_index]

    # replace 1 or 2 characters with a number
    for i in range(random.randrange(1, 3)):
        replace_index = random.randrange(len(new_password) // 2)
        new_password = new_password[0:replace_index] + str(random.randrange(10)) + new_password[replace_index + 1:]

    # replace 1 or 2 letters with an uppercase letter
    for i in range(random.randrange(1, 3)):
        replace_index = random.randrange(len(new_password) // 2, len(new_password))
        new_password = new_password[0:replace_index] + new_password[replace_index].upper() + new_password[replace_index + 1:]

    return new_password
