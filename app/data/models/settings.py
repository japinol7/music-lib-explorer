import sqlalchemy
from app.data.sqlalchemybase import SqlAlchemyBase
from sqlalchemy.sql import func


class Settings(SqlAlchemyBase):
    __tablename__ = 'settings'

    # Ids
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    # Normal columns
    is_get_spotify_data = sqlalchemy.Column(sqlalchemy.Boolean)
    created = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), server_default=func.now())
    updated = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"Settings(id={self.id!r}, " \
               f"is_get_spotify_data={self.is_get_spotify_data!r})"
