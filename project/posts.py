
from random import choice
from datetime import datetime

#from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime
#from sqlalchemy.sql import select
from flask import url_for

from database import db
import prefs
import threads
import users


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    content_raw = db.Column(db.Text)
    content_html = db.Column(db.Text)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))

def post_list(thread_id, number=prefs.POSTS_PER_PAGE, page=None, start_at=None):
    global posts

    posts_list = Post.query.filter_by(thread_id=thread_id).limit(number).all()

    threads_table = threads.threads
    users_table = users.users

    posts_select = select([posts.c.id, posts.c.time, posts.c.content_html,\
        users_table.c.name],\
        posts.c.thread == thread_id, from_obj=[posts.join(users_table)]).\
        limit(number).apply_labels()

    result = db.get_engine().execute(posts_select)
    posts_list = []

    for row in result:
        post = dict()
        post['post_id'] = row[posts.c.id]
        post['time'] = row[posts.c.time]
        post['content'] = row[posts.c.content_html]
        post['author'] = dict()
        post['author']['name'] = row[users_table.c.name]
        posts_list.append(post)

    return posts_list


def mock_data():
    global posts
    poster_ids = [1, 2, 3, 4]
    thread_ids = [x for x in xrange(1, 20)]
    contents = [
        "Your long-dormant pager comes back to life displaying 80087734. \
        You flip it around to discover 'hELLBOOB'",
        "You're not fooling anyone. You didn't just 'mention' this guy's \
        racism for the forums' good You didn't like that he had a popular \
        thread",
        "Tell me how this recession is affecting WoW Gold/US Dollar exchange \
        rates",
        "How can anybody condemn rapists while not condemning girls wearing \
        short skirts in the very same breath?",
        "I returned her smile with a cold, Clint Eastwood style death stare, \
        finished off with a little snort of disgust.",
        "I have a pretty big dog (90 ibs) and he gets high with me all the \
        time. I say this because the only time I 'forced' him was the \
        first time",
        "There's no difference between having a few art deco statues in your \
        living room and having a couple of Optimus Prime figures on \
        the mantle",
        "Goons are deeply alienated by PUAs because they're all idealist \
        shy nerds and want to believe that people are intelligent \
        conscious beings",
        "Just because animals can't talk doesn't mean they can't \
        give consent.",
        "Why wouldn't you want to fuck Alf?",
        "Begging's profitable hell the bible talks about beggers from olden \
        times if it wasnt such a profitable job it wouldnt \
        hold the test of time",
        "When the mold started flaking off during the shower and \
        clogging the drain, I knew it was time."
    ]

    mock_posts = []

    for x in xrange(50):
        mock_posts.append({
            'poster': choice(poster_ids),
            'content_html': choice(contents),
            'thread': choice(thread_ids)
        })

    db.get_engine().execute(posts.insert(), mock_posts)
