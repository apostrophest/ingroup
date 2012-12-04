
import bcrypt

from models import User


def validate_login(name, password):
    """
    Validates a user's login credentials.

    :param basestring name: Username to validate
    :param basestring password: Password to validate
    :return: Whether credentials were validated or not
    :rtype: bool
    """
    user = User.select().where(User.name == name).one()
    if user is not None:
        if bcrypt.hashpw(password, user['password']) == user['password']:
            return True
    return False


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
