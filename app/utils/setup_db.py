import logging

from app.data import session_factory
from app.data.models.user import User
from app.services import user_service

user: User = None


def setup_db():
    global user
    session_factory.global_init('hover_share.sqlite')
    session_factory.create_tables()
    user = user_service.get_default_user()
