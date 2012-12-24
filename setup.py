import os
import sys
import argparse

import bcrypt

parser = argparse.ArgumentParser(description='Set up an ingroup install.')
mocker = parser.add_subparsers(dest='opt')
mocker.add_parser('mock')
#parser.add_argument(dest='mock', action='store_true', default=False,
#                    help='Set up the install with mock data rather than a clean install.')

args = parser.parse_args()

print 'Generating secret key...'
try:
    with open('key.py', 'w') as k:
        k.write("SECRET_KEY = \'ingroup" + bcrypt.gensalt() + "\'")
        print 'Key generated successfully.'
except IOError:
    print 'Key generation FAILED.'

print 'Cleaning up...'

import prefs
from database import db, create_flask_app
app = create_flask_app()

from controllers import users, forums, threads, posts, applicants


with app.test_request_context():
    db.drop_all()

    db.create_all()

    print 'Tables created...'

    if args.opt == 'mock':
        users.mock_data(db.session)
        forums.mock_data(db.session)
        threads.mock_data(db.session)
        posts.mock_data(db.session)
        applicants.mock_data(db.session)

        db.session.commit()

        print 'Mock data installed...'
    else:
        # Do a real install...
        # Don't know what that will look like yet.
        print 'Note: Tables are empty without mock data.'

print 'Done.'
