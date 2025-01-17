import datetime

import sqlalchemy
from sqlalchemy.orm import relationship

from app.data.sqlalchemybase import SqlAlchemyBase


class Song(SqlAlchemyBase):
    __tablename__ = 'song'

    # Ids
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    track_id = sqlalchemy.Column(sqlalchemy.Integer, index=True, nullable=True, unique=True)
    persistent_id = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True, unique=True)
    x_id = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True, unique=True)

    # Foreign keys
    album_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('album.id'))
    album = relationship('Album', back_populates='songs')

    # Normal columns
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True)
    artist = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True)
    genre = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True)
    composer = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    grouping = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    work = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    location = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date_released = sqlalchemy.Column(sqlalchemy.DateTime, index=True)
    date_modified = sqlalchemy.Column(sqlalchemy.DateTime, index=True)
    date_added = sqlalchemy.Column(sqlalchemy.DateTime, index=True)
    date_added_orig = sqlalchemy.Column(sqlalchemy.DateTime, index=True)
    is_data_added_fixed = sqlalchemy.Column(sqlalchemy.Boolean)
    date_imported = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, index=True)
    mov_number = sqlalchemy.Column(sqlalchemy.Integer)
    mov_count = sqlalchemy.Column(sqlalchemy.Integer)
    mov_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    size = sqlalchemy.Column(sqlalchemy.Integer)
    duration = sqlalchemy.Column(sqlalchemy.Integer)
    duration_rep = sqlalchemy.Column(sqlalchemy.String)
    disc_number = sqlalchemy.Column(sqlalchemy.Integer)
    disc_count = sqlalchemy.Column(sqlalchemy.Integer)
    track_number = sqlalchemy.Column(sqlalchemy.Integer)
    track_count = sqlalchemy.Column(sqlalchemy.Integer)
    year = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    bit_rate = sqlalchemy.Column(sqlalchemy.Integer)
    sample_rate = sqlalchemy.Column(sqlalchemy.Integer)
    plays = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    comments = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    file_folder_count = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    sort_album = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    sort_artist = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    sort_composer = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    sort_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    artwork_count = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    normalization = sqlalchemy.Column(sqlalchemy.Integer)
    is_user_added = sqlalchemy.Column(sqlalchemy.Boolean)

    def __repr__(self):
        return f"Song(id={self.id!r}, " \
               f"track_id={self.track_id!r}, " \
               f"name={self.name!r}, " \
               f"artist={self.artist!r})"
