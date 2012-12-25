from random import choice
from datetime import datetime

import markdown

import prefs
from models import Post

def post_list(session, thread_id, number=prefs.POSTS_PER_PAGE, page=None, start_at=None):
    return session.query(Post).filter_by(thread_id=thread_id).limit(number).all()


def make_post(session, user, thread_id, raw_text):
    html_text = markdown.markdown(raw_text)
    new_post = Post(time=datetime.utcnow(), content_raw=raw_text, content_html=html_text, author_id=user.id, thread_id=thread_id)
    session.add(new_post)
    return new_post

def mock_data(session):
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

    for x in xrange(50):
        session.add(Post(**{'author_id': choice(poster_ids),\
            'content_html': choice(contents), 'thread_id': choice(thread_ids)}))
