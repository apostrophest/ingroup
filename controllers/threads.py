from random import choice

import prefs
from models import Thread


def thread_list(session, forum_id, number=prefs.THREADS_PER_PAGE, page=None):
    return session.query(Thread).filter_by(forum_id=forum_id).all()


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

