from random import choice

from sqlalchemy.sql.expression import desc

import prefs
from models import Thread


def thread_list(session, number=prefs.THREADS_PER_PAGE, page=None):
    threads = session.query(Thread).order_by(desc(Thread.last_post_time))[(page-1)*number:page*number]
    return threads


def thread_from_id(session, thread_id):
    return session.query(Thread).filter_by(id=thread_id).first()


def create_thread(session, title):
    new_thread = Thread(title)
    session.add(new_thread)
    session.flush()
    return new_thread


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

