
from sqlalchemy.sql import and_
from sqlalchemy.sql.expression import desc, select
from sqlalchemy.sql.operators import in_op

import prefs
from models import Thread, LastRead


def thread_list(session, number=prefs.THREADS_PER_PAGE, page=None):
    threads = session.query(Thread).order_by(desc(Thread.last_post_time))[(page-1)*number:page*number]
    return threads

def mark_read(session, user, thread, last_post):
    pass

def unread_posts(session, user, threads):
    thread_ids = [t.id for t in threads]
    if not thread_ids:
        return []
    post_selection = select([LastRead.c.thread_id, LastRead.c.post_number]).where(
        and_(LastRead.c.user_id == user.id, in_op(LastRead.c.thread_id, thread_ids))
    )
    return session.execute(post_selection).fetchall()

def thread_from_id(session, thread_id):
    return session.query(Thread).filter_by(id=thread_id).first()


def create_thread(session, title):
    new_thread = Thread(title)
    session.add(new_thread)
    session.flush()
    return new_thread
