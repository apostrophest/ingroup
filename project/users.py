import bcrypt
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.sql import select
from flask import url_for
from ingroup import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), unique=True)
    display_name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    avatar = db.Column(db.String(50))
    email = db.Column(db.String(100))

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    # Possible threads relationship here


def validate_login(name, password):
    global users
    find_user = users.select().where(users.c.name == name)
    user = db.get_engine().execute(find_user).fetchone()
    if user != None:
        if bcrypt.hashpw(password, user['password']) == user['password']:
            return True
    return False


def mock_data():
    db.get_engine().execute(users.insert(), [
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
        ])