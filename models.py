__author__ = 'Stephen Thompson <stephen@chomadoma.net>'

from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), unique=True)
    display_name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    avatar = db.Column(db.String(50))
    email = db.Column(db.String(100))

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    threads = db.relationship('Thread', backref='author', lazy='dynamic')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    content_raw = db.Column(db.Text)
    content_html = db.Column(db.Text)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    replies = db.Column(db.Integer)

    forum_id = db.Column(db.Integer, db.ForeignKey('forum.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    #last_post_id = db.Column(db.Integer, ForeignKey('Post.id'))
    #last_post = db.relationship('Post', uselist=False)

    posts = db.relationship('Post', backref='thread', lazy='dynamic')

class Forum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    subtitle = db.Column(db.String(200))

    threads = db.relationship('Thread', backref='forum', lazy='dynamic')

    def __init__(self, title, subtitle):
        self.title = title
        self.subtitle = subtitle

class Applicant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.String(256))
    email = db.Column(db.String(100))

class Invitee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), unique=True)
    email = db.Column(db.String(100))
    code = db.Column(db.String(32))

    inviter_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    inviter = db.relationship('User')


