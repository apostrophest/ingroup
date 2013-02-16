__author__ = 'Stephen Thompson <stephen@chomadoma.net>'

from flask.ext.login import make_secure_token
import pytz

from database import db

utc_tz = pytz.timezone('UTC')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), unique=True)
    display_name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    avatar = db.Column(db.String(50))
    email = db.Column(db.String(100))
    timezone = db.Column(db.String(30))
    token = db.Column(db.String(50))
    approved = db.Column(db.Boolean())

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return bool(self.approved)

    def is_anonymous(self):
        return not self.approved

    def get_id(self):
        return unicode(self.id)

    def get_auth_token(self):
        return make_secure_token(self.name, self.password)

    def __repr__(self):
        return u"<User: id={0:>s}, name={1:>s}, display_name={2:>s}, email={3:>s}, approved={4!r}>".format(
            str(self.id), self.name, self.display_name, self.email, bool(self.approved))

class Post(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), primary_key=True)
    time = db.Column(db.DateTime)
    content_raw = db.Column(db.Text)
    content_html = db.Column(db.Text)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def local_time(self, tz):
        if self.time is not None:
            return utc_tz.localize(self.time).astimezone(tz).strftime("%Y-%m-%d %H:%M")
        return None

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    last_post_time = db.Column(db.DateTime)
    posts = db.Column(db.Integer)

    def __init__(self, title):
        self.title = title
        self.posts = 0

    def __repr__(self):
        return u'<Thread id={0:d}, title={1}>'.format(self.id, self.title)


class Applicant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', foreign_keys=user_id)
    reason = db.Column(db.String(256))

    processor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    processor = db.relationship('User', foreign_keys=processor_id)

    result = db.Column(db.Integer)

    def __init__(self, user, reason):
        self.user = user
        self.name = user.name
        self.reason = reason
        self.result = None
        self.processor_id = None

    @property
    def approved(self):
        if self.result is None:
            return None
        else:
            return bool(self.result)

    @approved.setter
    def approved(self, result):
        self.result = int(result)

    def __repr__(self):
        return u'<Applicant id={0:d}, user={1!r}, reason={2}>'.format(self.id, self.user, self.reason)


LastRead = db.Table('last_read',
                db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                db.Column('thread_id', db.Integer, db.ForeignKey('thread.id'), primary_key=True),
                db.Column('post_number', db.Integer, db.ForeignKey('post.number')),
                db.Index('user_thread_index', 'user_id', 'thread_id')
            )
