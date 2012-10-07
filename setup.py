import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.curdir), 'project'))

from ingroup import db
import users
import forums
import threads
import posts
import applicants
import invitees
import argparse
import bcrypt

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
    users.mock_data()
    forums.mock_data()
    threads.mock_data()
    posts.mock_data()
    applicants.mock_data()
    invitees.mock_data()
    print 'Mock data installed...'
else:
    # Do a real install...
    # Don't know what that will look like yet.
    print 'Note: Tables are empty without mock data.'


print 'Generating secret key...'
try:
  with open('key.py', 'w') as k:
    k.write("SECRET_KEY = \'ingroup" + bcrypt.gen_salt() + "\'")
    print 'Key generated successfully.'
except IOError:
  print 'Key generation FAILED.'

print 'Done.'
