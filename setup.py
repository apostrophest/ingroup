import os
import sys
import argparse

import bcrypt
#from flask import Flask
#from flask.ext.sqlalchemy import SQLAlchemy

import prefs
from ingroup import db
from models import *

print 'Generating secret key...'
try:
  with open('key.py', 'w') as k:
    k.write("SECRET_KEY = \'ingroup" + bcrypt.gensalt() + "\'")
    print 'Key generated successfully.'
except IOError:
  print 'Key generation FAILED.'

#app = Flask(__name__, template_folder='/home/stephen/ingroup/templates/', static_folder='/home/stephen/ingroup/static')
#app.config.from_object(prefs.Config)
#db = SQLAlchemy(app)

from controllers import users, forums, threads, posts, applicants, invitees

parser = argparse.ArgumentParser(description='Set up an ingroup install.')
parser.add_argument('--mock', dest='mock', action='store_const',
                   const=True, default=False,
                   help='Set up the install with mock data rather \
                   than a clean install.')

args = parser.parse_args()

print 'Cleaning up...'

db.drop_all()

db.create_all()

print 'Tables created...'

if args.mock:
    users.mock_data(db.session)
    forums.mock_data(db.session)
    threads.mock_data(db.session)
    posts.mock_data(db.session)
    applicants.mock_data(db.session)
    invitees.mock_data(db.session)

    db.session.commit()

    print 'Mock data installed...'
else:
    # Do a real install...
    # Don't know what that will look like yet.
    print 'Note: Tables are empty without mock data.'

print 'Done.'
