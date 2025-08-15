from flask import Flask

app = Flask(__name__)

from . import views
from . import music_library

from app.data import session_factory


def _load_settings():
    from app.data.models.settings import Settings

    from app.config.config import update_config_settings
    from app.tools.logger.logger import log
    try:
        log.info("Load or create default settings object")
        session = session_factory.create_session()
        update_config_settings(session, Settings)
    except Exception as e:
        log.warning("Cannot load or create default settings object. Error: %s", e)


def _create_default_music_box_if_needed():
    from app.config.config import (
        MUSIC_LIST_NAME_DEFAULT, MUSIC_LIST_ID_DEFAULT, MUSIC_LIST_X_ID_DEFAULT,
        )
    from app.data.models.music_list import MusicList

    session = session_factory.create_session()
    music_list = session.query(MusicList).first()
    if not music_list:
        music_list = MusicList(
            name=MUSIC_LIST_NAME_DEFAULT,
            id=MUSIC_LIST_ID_DEFAULT,
            x_id=MUSIC_LIST_X_ID_DEFAULT,
            sequence_num=1)
        session.add(music_list)
        session.commit()
    session.close()


_load_settings()
_create_default_music_box_if_needed()
