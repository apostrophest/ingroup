
import bcrypt
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.sql import select
from flask import url_for

from database import db
from models import posts, threads

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), unique=True)
    display_name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    avatar = db.Column(db.String(50))
    email = db.Column(db.String(100))

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    threads = db.relationship('Thread', backref='author', lazy='dynamic')


def validate_login(name, password):

    """
    Validates a user's login credentials.

    :param basestring name: Username to validate
    :param basestring password: Password to validate
    :return: Whether credentials were validated or not
    :rtype: bool
    """
    global users
    find_user = users.select().where(users.c.name == name)
    user = db.get_engine().execute(find_user).fetchone()
    if user is not None:
        if bcrypt.hashpw(password, user['password']) == user['password']:
            return True
    return False


def mock_data():
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
        db.session.add(User(**datum))
