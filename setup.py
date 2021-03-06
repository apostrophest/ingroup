import argparse
import getpass

import bcrypt

parser = argparse.ArgumentParser(description='Set up an ingroup install.')
parser.add_argument(dest='opt', type=str, choices=('production',), help='Deployment environment. production: Sets up a blank forum.')

args = parser.parse_args()

print 'Generating secret key...'
try:
    with open('key.py', 'w') as k:
        k.write("SECRET_KEY = \'ingroup" + bcrypt.gensalt() + "\'")
        print 'Key generated successfully.'
except IOError:
    print 'Key generation FAILED.'

print 'Cleaning up...'

from database import db, create_flask_app
app = create_flask_app()

from controllers import users, applicants

with app.test_request_context():
    db.drop_all()

    db.create_all()

    print 'Tables created...'

    if args.opt == 'production':
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

        user = users.create_user(db.session, name, password, email)
        applicant = applicants.create_applicant(db.session, user, 'ingroup creator')
        db.session.flush()
        applicants.accept_applicant(db.session, applicant.id, user)
        db.session.commit()
        print 'User successfully created.'
    else:
        # Don't add any defaults to the database.
        print 'Note: Tables are empty without data.'

print 'Done.'
