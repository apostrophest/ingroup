import db
import bcrypt
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.sql import select
from flask import url_for


users = Table('users', db.get_metadata(),
    Column('id', Integer, primary_key=True),
    Column('name', String, unique=True),
    Column('display_name', String),
    Column('password', String),
    Column('avatar', String),
    Column('email', String)
)


def drop_table():
    global users
    users.drop(db.get_engine(), checkfirst=True)


def create_table():
    global users
    users.create(db.get_engine(), checkfirst=True)


def count():
    global users
    return select([users]).count()


def register_user(name, password):
    pass


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