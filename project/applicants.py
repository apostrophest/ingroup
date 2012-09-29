import db
import bcrypt
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.sql import select
from flask import url_for


applicants = Table('applicants', db.get_metadata(),
    Column('id', Integer, primary_key=True),
    Column('reason', String),
    Column('email', String)
)


def drop_table():
    global applicants
    applicants.drop(db.get_engine(), checkfirst=True)


def create_table():
    global applicants
    applicants.create(db.get_engine(), checkfirst=True)


def mock_data():
    pass
