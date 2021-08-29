from app.data import session_factory
from app.data.models.song import Song


def is_music_lib_imported():
    session = session_factory.create_session()
    song = session.query(Song).first()
    return song and True or False
