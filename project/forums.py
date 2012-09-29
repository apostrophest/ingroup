import db
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.sql import select
from flask import url_for


forums = Table('forums', db.get_metadata(),
    Column('id', Integer, primary_key=True),
    Column('title', String),
    Column('subtitle', String)
)


def drop_table():
    forums.drop(db.get_engine(), checkfirst=True)


def create_table():
    forums.create(db.get_engine(), checkfirst=True)


def mock_data():
    db.get_engine().execute(forums.insert(), [
        {'title': 'Announcements',
            'subtitle': 'Important shit you need to know.'},
        {'title': 'Action no Dev',
            'subtitle': 'Games that will never be completed.'},
        {'title': 'Juicy Juice',
            'subtitle': 'Everything and/or nothing.'}
        ])


def forum_list():
    forums_select = select([forums])
    result = db.get_engine().execute(forums_select)

    forums_list = []
    for row in result:
        forums_list.append(dict(row))

    return forums_list
