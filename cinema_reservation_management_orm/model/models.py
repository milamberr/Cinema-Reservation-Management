class User:
    def __init__(self, id, username):
        self.__username = username
        self.__id = id

    @property
    def username(self):
        return self.__username

    @property
    def id(self):
        return self.__id


class Movie:
    def __init__(self, id, name, rating):
        self.__id = id
        self.__name = name
        self.__rating = rating

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def rating(self):
        return self.__rating


class Projection:
    def __init__(self, projection_id, movie_name, _type, date, time):
        self.__projection_id = projection_id
        self.__movie_name = movie_name
        self.__type = _type
        self.__date = date
        self.__time = time

    @property
    def id(self):
        return self.projection_id

    @property
    def movie_name(self):
        return self.__movie_name

    @property
    def type(self):
        return self.__movie_name

    @property
    def date(self):
        return self.__date

    @property
    def time(self):
        return self.__time
