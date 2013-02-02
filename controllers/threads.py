from random import choice

import prefs
from models import Thread
from posts import make_post


def thread_list(session, forum_id, number=prefs.THREADS_PER_PAGE, page=None):
    return session.query(Thread).filter_by(forum_id=forum_id).all()


def thread_from_id(session, thread_id):
    return session.query(Thread).filter_by(id=thread_id).first()

def post_thread(session, forum_id, title, content, author):
    new_thread_id = create_thread(session, forum_id, title, author.id)
    new_post = make_post(session, author, new_thread_id, content)
    session.flush()
    return new_thread_id, new_post.id

def create_thread(session, forum_id, title, author_id):
    new_thread = Thread(forum_id, title, author_id)
    session.add(new_thread)
    session.flush()
    return new_thread.id

def mock_data(session):
    global threads
    forum_ids = [1, 2, 3]
    thread_titles = [
        'hello 20XX', 'Beekeeping', 'MiKKKro$fot LoseBlows', 'my story from band camp',
        'The system is going down for maintenance now.', 'girl porblems',
        'A comprehensive treatise concerning my support for Willard Romney']
    author_ids = [1, 2, 3, 4]

    for x in xrange(20):
        session.add(Thread(**{
            'forum_id': choice(forum_ids),
            'title': choice(thread_titles),
            'author_id': choice(author_ids)}))

