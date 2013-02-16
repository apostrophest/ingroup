from datetime import datetime

import markdown
from sqlalchemy.sql.expression import asc

import prefs
from models import Post

def post_list(session, thread_id, number=prefs.POSTS_PER_PAGE, page=None, start_at=None):
    return session.query(Post).filter_by(thread_id=thread_id).order_by(asc(Post.time)).limit(number).all()


def make_post(session, user, thread, raw_text):
    html_text = markdown.markdown(raw_text, safe_mode='escape', output_format='html5')
    new_post = Post(time=datetime.utcnow(), content_raw=raw_text, content_html=html_text, author_id=user.id, thread_id=thread.id)
    session.add(new_post)
    thread.last_post_time = new_post.time
    thread.posts += 1
    new_post.number = thread.posts
    return new_post
