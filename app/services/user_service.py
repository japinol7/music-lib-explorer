from app.data import session_factory
from app.data.models.user import User


def get_default_user():
    session = session_factory.create_session()

    user = session.query(User).filter(User.email == 'test_user_1@test.test.com.test').first()
    if user:
        return user

    user = User()
    user.email = 'test_user_1@test.test.com.test'
    user.name = 'User 1'
    session.add(user)
    session.commit()

    return user
