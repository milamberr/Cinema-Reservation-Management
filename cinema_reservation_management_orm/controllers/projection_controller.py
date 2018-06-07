from model.tables import session, Reservation
from pprint import pprint


class ProjectionController:
    @classmethod
    def get_num_free_seats(cls, projection_id):
        return 100 - session.query(Reservation).filter(
            Reservation.projection_id == projection_id
        ).count()

    @classmethod
    def show_seat_table(cls, projection_id):
        seats = session.query(Reservation.row, Reservation.col).filter(
            Reservation.projection_id == projection_id
        ).all()

        seat_table = [
            ['x', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
            ['1', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['2', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['3', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['4', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['5', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['6', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['7', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['8', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['9', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['10', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']
        ]

        for seat in seats:
            seat_table[seat[0]][seat[1]] = 'x'

        pprint(seat_table)

        return seat_table
