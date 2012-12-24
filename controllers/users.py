
import bcrypt
from flask.ext.login import make_secure_token

from models import db, User, Applicant


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
        if bcrypt.hashpw(password, user.password) == user.password and user.is_active():
            return user
    return None

def create_user(session, username, password, email, reason):
    user = session.query(User).filter(User.name==username).first()
    if user is not None:
        return None
    else:
        user = {
            'name': username,
            'display_name': username,
            'email': email,
            'avatar': 'new_user.png',
            'approved': False,
            'timezone': 'UTC',
            'password': bcrypt.hashpw(password, bcrypt.gensalt(12))
        }
        user['token'] = make_secure_token(user['name'], bcrypt.gensalt(12), user['password'])

        user = User(**user)
        session.add(user)
        session.flush()

        applicant = Applicant(user_id=user.id, reason=reason)
        session.add(applicant)
        session.commit()

        return user

def mock_data(session):
    data = [
        {'password': bcrypt.hashpw(u'one', bcrypt.gensalt()), 'timezone': 'America/New York',
            'name': u'one', 'display_name': u'one',
            'avatar': u'one.png', 'approved': True, 'email': u'one@one.com'},
        {'password': bcrypt.hashpw(u'two', bcrypt.gensalt()), 'timezone': 'America/New York',
            'name': u'two', 'display_name': u'two',
            'avatar': u'two.png', 'approved': True, 'email': u'two@two.com'},
        {'password': bcrypt.hashpw(u'three', bcrypt.gensalt()), 'timezone': 'America/New York',
            'name': u'three', 'display_name': u'three',
            'avatar': u'three.png', 'approved': True, 'email': u'three@three.com'},
        {'password': bcrypt.hashpw(u'four', bcrypt.gensalt()), 'timezone': 'America/New York',
            'name': u'four', 'display_name': u'four',
            'avatar': u'four.png', 'approved': True, 'email': u'four@four.com'}
        ]

    for datum in data:
        datum['token'] = make_secure_token(datum['name'], bcrypt.gensalt(12), datum['password'])
        session.add(User(**datum))

def token_loader(token):
    return db.session.query(User).filter(User.token==token).first()

def user_loader(id):
    return db.session.query(User).filter(User.id==int(id)).first()