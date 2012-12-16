
import bcrypt

from models import db, User


def valid_credentials(session, username, password):
    """
    Validates a user's login credentials.

    :param basestring name: Username to validate
    :param basestring password: Password to validate
    :return: User object of validated user, otherwise None
    :rtype: User, None
    """
    user = session.query(User).filter(User.name == username).first()
    if user is not None:
        if bcrypt.hashpw(password, user.password) == user.password:
            return user
    return None


def mock_data(session):
    data = [
        {'password': bcrypt.hashpw('one', bcrypt.gensalt()),
            'name': 'one', 'display_name': 'one',
            'avatar': 'one.png'},
        {'password': bcrypt.hashpw('two', bcrypt.gensalt()),
            'name': 'two', 'display_name': 'two',
            'avatar': 'two.png'},
        {'password': bcrypt.hashpw('three', bcrypt.gensalt()),
            'name': 'three', 'display_name': 'three',
            'avatar': 'three.png'},
        {'password': bcrypt.hashpw('four', bcrypt.gensalt()),
            'name': 'four', 'display_name': 'four',
            'avatar': 'four.png'}
        ]

    for datum in data:
        session.add(User(**datum))

def token_loader(token):
    return db.session.query(User).filter(User.token==token).first()

def user_loader(id):
    return db.session.query(User).filter(User.id==int(id)).first()