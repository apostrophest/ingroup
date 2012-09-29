import db
from random import choice
from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import select
from flask import url_for


posts = Table('posts', db.get_metadata(),
    Column('id', Integer, primary_key=True),
    Column('poster', Integer, ForeignKey('users.id')),
    Column('time', DateTime),
    Column('content_raw', String),
    Column('content_html', String),
    Column('thread', Integer, ForeignKey('threads.id'))
)


def drop_table():
    global posts
    posts.drop(db.get_engine(), checkfirst=True)


def create_table():
    global posts
    posts.create(db.get_engine(), checkfirst=True)


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
