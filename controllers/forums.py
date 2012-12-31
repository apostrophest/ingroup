from models import Forum

def create_forum(session, name, description):
    session.add(Forum(name, description))

def mock_data(session):
    data = [
        {'title': 'Announcements',
            'subtitle': 'Important shit you need to know.'},
        {'title': 'Action no Dev',
            'subtitle': 'Games that will never be completed.'},
        {'title': 'Juicy Juice',
            'subtitle': 'Everything and/or nothing.'}
    ]

    for datum in data:
        session.add(Forum(**datum))


def forum_list(session):
    return session.query(Forum).all()
