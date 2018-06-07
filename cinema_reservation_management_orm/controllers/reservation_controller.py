from model.tables import session, Movie, Projection, Reservation
from controllers.movie_controller import MovieController
from controllers.projection_controller import ProjectionController
from utils.utils import atomic


class ReservationController:
    @classmethod
    def insert_new_reservation(cls, *args):
        pass

    @classmethod
    @atomic
    def make_reservation(cls, user):
        num_tickets = cls.choose_number_of_tickets()
        movie_id = cls.choose_a_movie()

        while(True):
            proj_id = cls.choose_projection(movie_id)
            if ProjectionController.get_num_free_seats(proj_id) < num_tickets:
                print("There are not enough free seats for this projection.Please choose a different projection\n")
            else:
                print("Advancing to choosing the seats!")
                break

        reserved_seats = []
        for i in range(num_tickets):
            reserved_seats.append(cls.reserve_a_seat(proj_id, user))

        print("Your tickets are ready to be reserved.Do you want to finalize the transaction?\n")

        if cls.finalize():
            print("Congratulations!You have just reserved your seats.We wish you happy cinema\n")
        else:
            print("Changes canceled...")

    @classmethod
    def finalize(cls):
        from view.menu import Menu
        menu = """
        Finalize transaction?
        1)Yes
        2)No
        """
        kwargs = Menu.get_input(menu, option=None)
        option = kwargs['option']

        if option == '1':
            session.commit()
            return True
        else:
            session.rollback()
            return False

    @classmethod
    def reserve_a_seat(cls, proj_id, user):
        from view.menu import Menu

        seat_table = ProjectionController.show_seat_table(proj_id)

        while(True):
            menu = """
            1)Reserve a seat
            2)Cancel reservation
            """
            kwargs = Menu.get_input(menu, option=None)
            option = kwargs["option"]
            if option == '1':
                kwargs = Menu.get_input("enter row and col\n", row=None, col=None)
                row, col = kwargs['row'], kwargs['col']
                try:
                    row = int(row)
                    col = int(col)
                    if seat_table[row][col] == '.':
                        session.add(
                            Reservation(
                                user_id=user.id,
                                projection_id=proj_id,
                                row=row,
                                col=col
                            )
                        )
                        print("Seat reserved!\n")
                        break
                    else:
                        print("Seat is taken!\n")
                except Exception:
                    print("Invalid input!\n")
            elif option == '2':
                raise Exception("Canceling reservation...")
            else:
                print("Invalid option!\n")

    @classmethod
    def choose_projection(cls, movie_id):
        from view.menu import Menu

        menu = """
        1)Choose a projection
        2)Cancel reservation
        """

        while(True):
            MovieController.show_projections_of_movie(movie_id)
            kwargs = Menu.get_input(menu, option=None)
            option = kwargs['option']
            if option == '1':
                try:
                    kwargs = Menu.get_input('', projection_by_id=None)
                    projection_id = kwargs['projection_by_id']
                    if cls.is_valid_id(projection_id, 'projection'):
                        return projection_id
                    else:
                        print("Invalid id\n")
                except Exception:
                    print("Invalid input!\n")

            elif option == '2':
                raise Exception("Canceling reservation...")

            else:
                print('Invalid option\n')

    @classmethod
    def choose_number_of_tickets(cls):
        from view.menu import Menu

        menu = """
        1)Choose number of tickets
        2)Cancel reservation
        """
        while(True):
            kwargs = Menu.get_input(menu, option=None)
            option = kwargs['option']
            if option == '1':
                kwargs = Menu.get_input(None, number_of_tickets=None)
                try:
                    num_tickets = int(kwargs['number_of_tickets'])
                    return num_tickets
                except Exception:
                    print("Invalid number tickets\n")
            elif option == '2':
                raise Exception("Canceling reservation...")
            else:
                print("Invalid input!\n")

    @classmethod
    def choose_a_movie(cls):
        from view.menu import Menu

        menu = """
        1)Choose a movie
        2)Cancel reservation
        """

        while(True):
            MovieController.show_all_movies()
            kwargs = Menu.get_input(menu, option=None)
            option = kwargs['option']
            if option == '1':
                movie_id = cls.obtain_movie_id()
                if movie_id:
                    return movie_id
                else:
                    print("Invalid movie id!")
            elif option == '2':
                raise Exception("Canceling reservation...")
            else:
                print("Invalid option")

    @classmethod
    def obtain_movie_id(cls):
        from view.menu import Menu
        from controllers.controller import Controller

        Controller.show_all_movies()
        try:
            kwargs = Menu.get_input("Choose a movie by id", movie_id=None)
            movie_id = int(kwargs['movie_id'])
            if cls.is_valid_id(movie_id, 'movie'):
                return movie_id
            else:
                return None
        except Exception:
            print("Invalid id!\n")

    @classmethod
    def is_valid_id(cls, id, from_table):
        if from_table == 'movie':
            return session.query(Movie).filter(Movie.id == id).scalar() is not None
        elif from_table == 'projection':
            return session.query(Projection).filter(Projection.id == id).scalar() is not None