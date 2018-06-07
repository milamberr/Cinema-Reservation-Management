from model.tables import session, Movie, Projection
from utils.utils import accepts, pretty_print


class MovieController:
    @classmethod
    def insert_new_movie(cls, name, rating):
        movie = Movie(name=name, rating=rating)
        session.add(movie)
        # session.commit()

    @classmethod
    def show_all_movies(cls):
        print("---MOVIES---")
        all_movies = session.query(Movie).all()
        all_movies = [movie.attributes() for movie in all_movies]
        pretty_print(all_movies, attributes=['id', 'name', 'rating'])
        return all_movies

    @classmethod
    def show_projections_of_movie(cls, movie_id):
        from controllers.reservation_controller import ReservationController

        try:
            movie_id = int(movie_id)
        except Exception:
            return None

        else:
            if ReservationController.is_valid_id(movie_id, 'movie'):
                movies = session.query(
                    Projection.id,
                    Movie.name,
                    Projection._type,
                    Projection.date,
                    Projection.time
                ).join(Movie).filter(Movie.id == movie_id).all()

            else:
                movies = None

        if movies:
            pretty_print(movies, attributes=['id', 'movie_name', 'type', 'date', 'time'])
        else:
            print("There is no such movie")

