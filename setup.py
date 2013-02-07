import os
import sys
import argparse
import getpass

import bcrypt

parser = argparse.ArgumentParser(description='Set up an ingroup install.')
parser.add_argument(dest='opt', type=str, choices=('mock', 'production'), help='Deployment environment. mock: Produces random test data. production: Sets up a blank forum.')

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
    elif args.opt == 'production':
        # Do a real install...
        # Don't know what that will look like yet?
        print 'Create a user'
        print '-------------'
        name = raw_input('Name: ')
        try:
            password = getpass.getpass()
        except getpass.GetPassWarning:
            print '***WARNING: Password may be visible in the terminal!'
            password = getpass.getpass()
        email = raw_input('Email: ')

        user = users.create_user(db.session, name, password, email, reason=None)
        user.approved = True
        db.session.delete(users.get_applicants(db.session)[0])
        db.session.commit()
        print 'User successfully created.'
    else:
        # Don't add any defaults to the database.
        print 'Note: Tables are empty without data.'

print 'Done.'
