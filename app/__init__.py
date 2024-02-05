from flask import Flask

app = Flask(__name__)

from . import views
from . import music_library


def _load_settings():
    from app.data import session_factory
    from app.data.models.settings import Settings

    from app.config.config import update_config_settings
    from app.tools.logger.logger import log
    try:
        log.info("Load or create default settings object")
        session = session_factory.create_session()
        update_config_settings(session, Settings)
    except Exception as e:
        log.warning("Cannot load or create default settings object. Error: %s", e)


_load_settings()
