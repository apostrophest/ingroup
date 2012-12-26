
import bcrypt
from flask.ext.login import make_secure_token

from models import User, Applicant


def valid_credentials(session, username, password):
    """
    Validates a user's login credentials.

    :param basestring name: Username to validate
    :param basestring password: Password to validate
    :return: User object of validated user, otherwise None
    :rtype: User, None
    """
    user = session.query(User).filter(User.name==username).first()
    if user is not None:
        if bcrypt.hashpw(password, user.password) == user.password and user.is_active():
            print '=== VALIDATED ==='
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
        user['token'] = make_secure_token(user['name'], user['password'])

        user = User(**user)
        session.add(user)
        session.flush()

        applicant = Applicant(user_id=user.id, reason=reason)
        session.add(applicant)
        session.commit()

        return user

def get_applicants(session):
    return session.query(User).filter(User.id.in_(session.query(Applicant.user_id))).all()


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
        datum['token'] = make_secure_token(datum['name'], datum['password'])
        session.add(User(**datum))

def token_loader(token):
    return User.query.filter(User.token==token).first()

def user_loader(uid):
    user = User.query.filter(User.id==int(uid)).first()
    print "User: auth: {0}, active: {1}, anon: {2}, id: {3}, get_token: {4}, stored_token: {5}".format(
        user.is_authenticated(), user.is_active(), user.is_anonymous(), user.get_id(), user.get_auth_token(), user.token
    )
    return user