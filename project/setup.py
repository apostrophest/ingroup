import users
import forums
import threads
import posts
import applicants
import invitees
import argparse

parser = argparse.ArgumentParser(description='Set up an ingroup install.')
parser.add_argument('--mock', dest='mock', action='store_const',
                   const=True, default=False,
                   help='Set up the install with mock data rather \
                   than a clean install.')

args = parser.parse_args()

print 'Cleaning up...'

users.drop_table()
forums.drop_table()
threads.drop_table()
posts.drop_table()
applicants.drop_table()
invitees.drop_table()

users.create_table()
forums.create_table()
threads.create_table()
posts.create_table()
applicants.create_table()
invitees.create_table()

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

print 'Done.'
