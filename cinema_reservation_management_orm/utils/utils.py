import hashlib
from tabulate import tabulate
from utils.exceptions import PasswordInvalidFormatError
from model.tables import session


def hash_password(username, password):
    return str(hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        username.encode(),
        10000
    ).hex())


def pretty_print(data, attributes=None):
    print(tabulate(data, headers=attributes, tablefmt='psql'))


def validate_password(func):
    def decorated(*args):
        if args[1] in args[2]:
            raise PasswordInvalidFormatError("The username should not be in the password!")
        if len(args[2]) < 8:
            raise PasswordInvalidFormatError("Password too short")

        has_caps = False
        has_special = False
        has_number = False
        for char in args[2]:
            if char >= '0' and char <= '9':
                has_number = True
            elif char >= 'A' and char <= 'Z':
                has_caps = True
            elif char < 'a' or char > 'z':
                has_special = True

        if not has_caps:
            raise PasswordInvalidFormatError("Password doesnt have capital letter")
        if not has_number:
            raise PasswordInvalidFormatError("Password doesnt have number")
        if not has_special:
            raise PasswordInvalidFormatError("Password doesnt have special symbol")
        return func(*args)
    return decorated


def validate_seat(func):
    def decorated(self, user, projection_id, row, col):
        try:
            row = int(row)
            col = int(col)
            if row < 1 or col < 1 or row > 11 or col > 11:
                print("Invalid row and col!")
                return False
        except Exception as e:
            print(e)
            print("Invalid input!\n")
       
        return func(self, user, projection_id, row, col)
    return decorated


def accepts(*args):
    def acceptor(func):
        def decorated(*args1):
            if len(args1[1:]) != len(args):
                raise TypeError("Invalid number of arguments")
            for i in range(len(args)):
                if not isinstance(args1[i + 1], args[i]):
                    raise TypeError("Invalid arguments")

            return func(args1)
        return decorated
    return acceptor


def atomic(func):
    def decorated(self, *args):
        try:
            func(self, *args)
        except Exception as e:
            print(e)
            session.rollback()
    return decorated
