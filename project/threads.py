import prefs
from random import choice
import db
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.sql import select
from flask import url_for


threads = Table('threads', db.get_metadata(),
    Column('id', Integer, primary_key=True),
    Column('title', String),
    Column('forum', Integer, ForeignKey('forums.id')),
    Column('author', Integer, ForeignKey('users.id')),
    Column('last_post', Integer, ForeignKey('posts.id')),
    Column('replies', Integer)
)


def drop_table():
    global threads
    threads.drop(db.get_engine(), checkfirst=True)


def create_table():
    global threads
    threads.create(db.get_engine(), checkfirst=True)


def object_translation(row):
    thread = dict()

    # Simple translations
    thread['id'] = row['id']
    thread['title'] = row['title']
    thread['replies'] = row['replies']

    # Author information
    thread['author'] = dict()

    # Derived information
    thread['url'] = url_for('thread_view', id=row['id'])

    thread['last_post'] = dict()
    thread['last_post']['author'] = last_post_author  # MAKE REAL
    thread['last_post']['time'] = last_post_time  # MAKE REAL
    thread['last_post']['author_url'] = last_post_author_url  # MAKE REAL


def load(number=prefs.THREADS_PER_PAGE, start_post=1):
    pass


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
            'author': choice(author_ids),
            'last_post': None,
            'replies': None
            })

    db.get_engine().execute(threads.insert(mock_threads))
