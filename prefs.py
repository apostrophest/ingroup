import key


class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ingroup.db'
    SQLALCHEMY_ECHO = True
    SECRET_KEY = key.SECRET_KEY
    APPLICATION_ROOT = '/home/stephen/ingroup/'


THREADS_PER_PAGE = 20
POSTS_PER_PAGE = 40