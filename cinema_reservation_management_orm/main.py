from view.menu import Menu
from model.tables import create_database
import os.path


def main():
    if not os.path.isfile("cinema_reservation_management.db"):
        create_database()
    Menu().start()


if __name__ == '__main__':
    main()
