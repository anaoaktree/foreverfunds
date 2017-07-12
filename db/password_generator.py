import random


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
