
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
    return session.query(Applicant).all()

def accept_applicant(session, applicant_id, accepter):
    applicant = session.query(Applicant).filter(Applicant.id==applicant_id).first()
    applicant.user.approved = True
    session.commit()
    # TODO: send email to applicant

def reject_applicant(session, applicant_id, rejecter):
    applicant = session.query(Applicant).filter(Applicant.id==applicant_id).first()
    session.delete(applicant.user)
    session.delete(applicant)
    session.commit()
    # TODO: sent email to applicant


def token_loader(token):
    return User.query.filter(User.token==token).first()

def user_loader(uid):
    user = User.query.filter(User.id==int(uid)).first()
    return user