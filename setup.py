import os
import sys
import argparse

import bcrypt

print 'Generating secret key...'
try:
  with open('key.py', 'w') as k:
    k.write("SECRET_KEY = \'ingroup" + bcrypt.gensalt() + "\'")
    print 'Key generated successfully.'
except IOError:
  print 'Key generation FAILED.'

from models import users, forums, threads, posts, applicants, invitees
from database import db
import ingroup


parser = argparse.ArgumentParser(description='Set up an ingroup install.')
parser.add_argument('mock', dest='mock', action='store_const',
                   const=True, default=False,
                   help='Set up the install with mock data rather \
                   than a clean install.')

args = parser.parse_args()

print 'Cleaning up...'

db.drop_all()

db.create_all()

print 'Tables created...'

if args.mock:
    users.mock_data()
    forums.mock_data()
    threads.mock_data()
    posts.mock_data()
    applicants.mock_data()
    invitees.mock_data()

    db.session.commit()

    print 'Mock data installed...'
else:
    # Do a real install...
    # Don't know what that will look like yet.
    print 'Note: Tables are empty without mock data.'

print 'Done.'
