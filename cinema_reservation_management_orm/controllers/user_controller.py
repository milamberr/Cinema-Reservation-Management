from model.tables import session, User
from utils.utils import hash_password, validate_password


class UserController:
    @classmethod
    def user_login(cls, username, password):
        hashed = hash_password(username, password)
        if session.query(User).filter(User.username == username, User.password == hashed).scalar() is not None:
            return session.query(User).filter(User.username == username, User.password == hashed).one()
        else:
            return None

    @classmethod
    @validate_password
    def register(cls, username, password):
        is_taken = session.query(User).filter(User.username == username).scalar() is not None
        if is_taken:
            return False
        else:
            cls.insert_new_user(username, password)
            return True

    @classmethod
    def insert_new_user(cls, username, password):
        hashed = hash_password(username, password)
        user = User(username=username, password=hashed)
        session.add(user)
        session.commit()