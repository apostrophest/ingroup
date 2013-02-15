
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
