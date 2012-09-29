from sqlalchemy import create_engine, MetaData

engine = None
metadata = MetaData()


def get_metadata():
    return metadata


def get_engine():
    global engine

    if engine != None:
        return engine
    else:
        engine = create_engine('sqlite:///ingroup.db', echo=True)
        return engine


def get_conn():
    return get_engine().connect()
