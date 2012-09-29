import db
import bcrypt
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.sql import select
from flask import url_for


invitees = Table('invitees', db.get_metadata(),
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('email', String),
    Column('code', String),
    Column('inviter', ForeignKey('users.id'))
)


def drop_table():
    invitees.drop(db.get_engine(), checkfirst=True)


def create_table():
    invitees.create(db.get_engine(), checkfirst=True)


def mock_data():
    pass