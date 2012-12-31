import os

import key

WEB_ROOT = '/home/t/'
APP_PATH = 'ingroup'

class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ingroup.db'
    SQLALCHEMY_ECHO = True
    SECRET_KEY = key.SECRET_KEY
    APPLICATION_ROOT = os.path.join(WEB_ROOT, APP_PATH)


THREADS_PER_PAGE = 20
POSTS_PER_PAGE = 40
