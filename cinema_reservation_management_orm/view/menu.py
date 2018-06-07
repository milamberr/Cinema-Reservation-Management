from controllers.controller import Controller
from getpass import getpass
from utils.exceptions import PasswordInvalidFormatError
from utils.utils import pretty_print


options_text = """
---MENU---
1)Log in
2)Register
3)Show movies
4)Show projections of a movie
5)Make reservation
6)Exit
7)Help
"""

helps_text = """
---HELP---
1)Click 1 if you want to login in the system
2)Click 2 if you want to register
3)Click 3 if you want to see all available movies
4)Click 4 if you want to see all projections of a movie.Choose a movie
5)Click 5 if you want to make a reservation.
6)Click 6 if you want to exit the system.
"""


class Menu:
    controller = Controller()

    def start(self):
        self.user = None

        print("Welcome to the cinema reservation system!\n")
        while(True):
            print(options_text)
            if self.user is not None:
                print("You are logged as {0}".format(self.user.username))

            option = input("Choose an action:\n")
            if option == '1':
                self.user_login()
            elif option == '2':
                self.user_register()
            elif option == '3':
                self.show_all_movies()
            elif option == '4':
                self.show_all_projections_of_movie()
            elif option == '5':
                self.make_reservation()
            elif option == '6':
                return
            elif option == '7':
                print(helps_text)
            else:
                print("Invalid option\n")

    def user_login(self):
        print("---LOG IN---")
        username = input('Username:')
        password = getpass("Password:")

        self.user = self.controller.user_login(username, password)
        if self.user:
            print("Login successful!")
        else:
            print("Login failed")

    def user_register(self):
        print("---REGISTRATION---")
        username = input('Username:')
        password = getpass("Password:")
        try:
            if self.controller.user_register(username, password):
                print("Registration successful")
            else:
                print("Username is taken")
        except PasswordInvalidFormatError as exc:
            print(exc)
            print("Registration failed")

    def show_all_movies(self):
        self.controller.show_all_movies()

    def show_all_projections_of_movie(self):
        self.show_all_movies()
        movie_id = input("Choose a movie:")
        self.controller.show_projections_of_movie(movie_id)

    def _user_is_logged(func):
        tmp_menu = """
        1)Log in
        2)Register
        3)Cancel
        """

        def decorated(self, *args):
            if self.user is None:
                while(self.user is None):
                    print(tmp_menu)
                    option = input("Choose option:")
                    if option == '1':
                        self.user_login()
                    elif option == '2':
                        self.user_register()
                    elif option == '3':
                        print("Going back to menu...")
                        return
                    else:
                        print("Invalid option")
            return func(self, *args)
        return decorated

    @_user_is_logged
    def make_reservation(self):
        self.controller.make_reservation(self.user)

    def reserve_a_seat(self, projection_id):
        self.controller.show_seat_table(projection_id)
        menu = """
        1)Choose a seat
        2)Cancel
        """
        while(True):
            print(menu)
            option = input("Choose option:")
            if option == '1':
                row = input("Choose row:")
                col = input("Choose col:")

                if self.controller.reserve_a_seat(self.logged_user, projection_id, row, col):
                    print("Reserved seat {0}-{1} successfuly!".format(row, col))
                    break
                else:
                    continue
            elif option == '2':
                raise Exception("Canceling reservation...")
            else:
                print("Invalid option!\n")

    @classmethod
    def get_input(cls, menu=None, **kwargs):
        if menu:
            print(menu)
        for key in kwargs.keys():
            kwargs[key] = input("Choose {0}:".format(key))
        return kwargs

