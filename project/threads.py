import prefs
from random import choice
import users
import forums
import posts
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.sql import select
from flask import url_for
from database import db


class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    replies = db.Column(db.Integer)

    forum_id = db.Column(db.Integer, db.ForeignKey('forum.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    #last_post_id = db.Column(db.Integer, ForeignKey('Post.id'))
    #last_post = db.relationship('Post', uselist=False)

    posts = db.relationship('Post', backref='thread', lazy='dynamic')


def thread_list(forum_id, number=prefs.THREADS_PER_PAGE, page=None):
    return Thread.query.filter_by(forum_id=forum_id).all()


def mock_data():
    global threads
    forum_ids = [1, 2, 3]
    thread_titles = [
        'hello 20XX', 'Beekeeping', 'MiKKKro$fot LoseBlows', 'my story from band camp',
        'The system is going down for maintenance now.', 'girl porblems',
        'A comprehensive treatise concerning my support for Willard Romney']
    author_ids = [1, 2, 3, 4]

    for x in xrange(20):
        db.session.add(Thread(**{
            'forum_id': choice(forum_ids),
            'title': choice(thread_titles),
            'author_id': choice(author_ids)}))

    db.session.commit()
