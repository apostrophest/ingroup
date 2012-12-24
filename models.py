__author__ = 'Stephen Thompson <stephen@chomadoma.net>'

from database import db

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
    threads = db.relationship('Thread', backref='author', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return bool(self.approved)

    def is_anonymous(self):
        return not self.approved

    def get_id(self):
        return unicode(self.id)

    def get_auth_token(self):
        return unicode(self.token)

    def __repr__(self):
        return u"<User: id={0:>s}, name={1:>s}, display_name={2:>s}, email={3:>s}, approved={4:>s}>".format(
            str(self.id), self.name, self.display_name, self.email, repr(bool(self.approved)))

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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', foreign_keys=user_id)
    reason = db.Column(db.String(256))

    inviter_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    inviter = db.relationship('User', foreign_keys=inviter_id)

    def __repr__(self):
        return u'<Applicant id={0:>s}, user={1:>s}, reason={2:>s}'.format(str(self.id), self.user, self.reason)


LastRead = db.Table('last_read',
                db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                db.Column('thread_id', db.Integer, db.ForeignKey('thread.id')),
                db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
            )
