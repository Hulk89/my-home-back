import sqlalchemy as db

def getEngine(**kwargs):
    engine_str = 'mysql+mysqldb://{user}:{password}@{host}:{port}/{db}'
    engine = db.create_engine(engine_str.format(**kwargs))
    return engine

if __name__ == '__main__':
    import sys
    import json

    with open(sys.argv[1]) as f:
        config = json.loads(f.read())
    engine = getEngine(**config)
    connection = engine.connect()

