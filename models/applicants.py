import bcrypt
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.sql import select
from flask import url_for
from database import db

class Applicant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.String(256))
    email = db.Column(db.String(100))


def mock_data():
    pass
