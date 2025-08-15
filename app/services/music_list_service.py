from app.data import session_factory
from app.data.models.music_list import MusicList


def get_total_music_listes():
    session = session_factory.create_session()
    return session.query(MusicList).count() or 0


def get_total_music_list_songs(music_list_id=None):
    session = session_factory.create_session()
    if music_list_id:
        return (session.query(MusicList).
                filter(MusicList.id == music_list_id).first().total_songs or 0)

    music_list = session.query(MusicList).first()
    if music_list:
        return session.query(MusicList).first().total_songs or 0
    return 0

def get_music_list_songs(music_list_id=None):
    session = session_factory.create_session()
    if music_list_id:
        return (session.query(MusicList).
                filter(MusicList.id == music_list_id).first().songs or [])
    return session.query(MusicList).first().songs or []
