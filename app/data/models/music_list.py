import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.ext.hybrid import hybrid_property

from app.data.sqlalchemybase import SqlAlchemyBase


class MusicList(SqlAlchemyBase):
    __tablename__ = 'music_list'

    # Ids
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    x_id = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True, unique=True)

    # Foreign keys
    songs = orm.relationship("Song", back_populates="music_list", lazy='select')

    # Normal columns
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True)
    sequence_num = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    date_created = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, index=True)

    @hybrid_property
    def total_songs(self):
        return len(self.songs)


def __repr__(self):
        return f"MusicList(id={self.id!r}, " \
               f"name={self.name!r}, " \
               f"len={len(self.songs)!r})"
