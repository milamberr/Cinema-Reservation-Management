from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, Date, Time
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker


Base = declarative_base()

engine = create_engine("sqlite:///cinema_reservation_management.db")
Session = sessionmaker(bind=engine)
session = Session()


def create_database():
    Base.metadata.create_all(engine)
    session.add_all([
        Reservation(user_id=3, projection_id=1, row=2, col=1),
        Reservation(user_id=3, projection_id=1, row=3, col=5),
        Reservation(user_id=3, projection_id=1, row=7, col=8),
        Reservation(user_id=2, projection_id=3, row=1, col=1),
        Reservation(user_id=2, projection_id=3, row=1, col=2),
        Reservation(user_id=5, projection_id=5, row=2, col=3),
        Reservation(user_id=6, projection_id=5, row=2, col=4)
    ])
    session.commit()

    session.add_all([
        Movie(name="The Hunger Games:Catching Fire", rating=7.9),
        Movie(name="Wreck-It Ralph", rating=7.8),
        Movie(name="Her", rating=8.3)
    ])
    session.commit()

    session.add_all([
        Projection(movie_id=1, _type="3D", date="2014-04-01", time="19:10"),
        Projection(movie_id=1, _type="2D", date="2014-04-01", time="19:00"),
        Projection(movie_id=1, _type="4DX", date="2014-04-02", time="21:00"),
        Projection(movie_id=3, _type="2D", date="2014-04-05", time="20:20"),
        Projection(movie_id=2, _type="3D", date="2014-04-02", time="22:00"),
        Projection(movie_id=2, _type="3D", date="2014-04-02", time="19:30")
    ])
    session.commit()


class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    rating = Column(Float)

    def __repr__(self):
        return "ID: {0}, Name: {1}, Rating: {2}".format(self.id, self.name, self.rating)

    def attributes(self):
        return [self.id, self.name, self.rating]


class Projection(Base):
    __tablename__ = 'projections'
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey(Movie.id))
    movie = relationship("Movie", backref="projections")
    _type = Column(String)
    date = Column(String)
    time = Column(String)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)


class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship("User", backref='reservations')
    projection_id = Column(Integer, ForeignKey(Projection.id))
    projection = relationship("Projection", backref='reservations')
    row = Column(Integer)
    col = Column(Integer)

