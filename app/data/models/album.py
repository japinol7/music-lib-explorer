import datetime
import sqlalchemy
from sqlalchemy import orm

from app.data.sqlalchemybase import SqlAlchemyBase


class Album(SqlAlchemyBase):
    __tablename__ = 'album'

    # Ids
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    x_id = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True, unique=True)

    # Foreign keys
    songs = orm.relationship("Song", back_populates="album", lazy='select')

    # Normal columns
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True)
    artist = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True)
    artist_tracks = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True)
    genre = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True)
    genre_internal = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True)
    composer = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    duration = sqlalchemy.Column(sqlalchemy.Integer)
    duration_rep = sqlalchemy.Column(sqlalchemy.String)
    track_count = sqlalchemy.Column(sqlalchemy.Integer)
    year = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    year_min = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    year_max = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    date_imported = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, index=True)

    def __repr__(self):
        return f"Album(id={self.id!r}, " \
               f"name={self.name!r}, " \
               f"artist={self.artist!r})"
