import prefs
from random import choice
import users
import forums
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

    last_post_id = db.Column(db.Integer, ForeignKey('post.id'))
    last_post = db.relationship('Post')

    posts = db.relationship('Post', backref='thread', lazy='dynamic')


def thread_list(forum_id, number=prefs.THREADS_PER_PAGE, page=None):
    global threads
    # Pages of threads, or orders of threads, not implemented yet
    thread_select = select([threads.c.id, threads.c.title, users.users.c.name],
        threads.c.forum == forum_id, from_obj=[threads.join(users.users)]).\
        limit(number).apply_labels()

    result = db.get_engine().execute(thread_select)
    thread_list = []

    for row in result:
        thread = dict()
        thread['id'] = row['threads_id']
        thread['title'] = row['threads_title']
        thread['author'] = row['users_name']
        thread_list.append(thread)

    return thread_list


def mock_data():
    global threads
    forum_ids = [1, 2, 3]
    thread_titles = [
        'hello 20XX', 'Beekeeping', 'MiKKKro$fot LoseBlows', 'my story from band camp',
        'The system is going down for maintenance now.', 'girl porblems',
        'A comprehensive treatise concerning my support for Willard Romney']
    author_ids = [1, 2, 3, 4]

    mock_threads = []

    for x in xrange(20):
        mock_threads.append({
            'forum': choice(forum_ids),
            'title': choice(thread_titles),
            'author': choice(author_ids)
            })

    db.get_engine().execute(threads.insert(), mock_threads)
