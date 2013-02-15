from datetime import datetime

import html5lib
from html5lib import sanitizer, serializer, treewalkers
import markdown

import prefs
from models import Post

html_parser = html5lib.HTMLParser(tokenizer=sanitizer.HTMLSanitizer)
html_serializer = serializer.HTMLSerializer()

def post_list(session, thread_id, number=prefs.POSTS_PER_PAGE, page=None, start_at=None):
    return session.query(Post).filter_by(thread_id=thread_id).limit(number).all()


def make_post(session, user, thread, raw_text):
    html_text = markdown.markdown(raw_text, safe_mode='escape', output_format='html5')
    new_post = Post(time=datetime.utcnow(), content_raw=raw_text, content_html=html_text, author_id=user.id, thread_id=thread.id)
    session.add(new_post)
    thread.last_post_time = new_post.time
    thread.posts += 1
    new_post.number = thread.posts
    return new_post
