from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.sql import select
from flask import url_for
from database import db

class Forum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    subtitle = db.Column(db.String(200))

    threads = db.relationship('Thread', backref='forum', lazy='dynamic')

    def __init__(self, title, subtitle):
        self.title = title
        self.subtitle = subtitle

def mock_data():
    data = [
        {'title': 'Announcements',
            'subtitle': 'Important shit you need to know.'},
        {'title': 'Action no Dev',
            'subtitle': 'Games that will never be completed.'},
        {'title': 'Juicy Juice',
            'subtitle': 'Everything and/or nothing.'}
    ]

    for datum in data:
        db.session.add(Forum(**datum))

    db.session.commit()

def forum_list():
    return Forum.query.all()
