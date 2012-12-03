import bcrypt
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.sql import select
from flask import url_for
from database import db

class Invitee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), unique=True)
    email = db.Column(db.String(100))
    code = db.Column(db.String(32))
    
    inviter_id = db.Column(db.Integer, ForeignKey('user.id'))
    inviter = db.relationship('User')


def mock_data():
    pass
