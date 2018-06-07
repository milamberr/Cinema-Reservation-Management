from controllers.movie_controller import MovieController
from controllers.projection_controller import ProjectionController
from controllers.reservation_controller import ReservationController
from controllers.user_controller import UserController


class Controller:
    @classmethod
    def user_login(cls, username, password):
        return UserController.user_login(username, password)

    @classmethod
    def user_register(cls, username, password):
        return UserController.register(username, password)

    @classmethod
    def show_all_movies(cls):
        return MovieController.show_all_movies()

    @classmethod
    def show_projections_of_movie(cls, movie_id):
        return MovieController.show_projections_of_movie(movie_id)

    @classmethod
    def make_reservation(cls, user):
        ReservationController.make_reservation(user)
