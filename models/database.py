from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def getEngine(**kwargs):
    engine_str = 'mysql+mysqldb://{user}:{password}@{host}:{port}/{db}'
    engine = create_engine(engine_str.format(**kwargs))
    return engine


def initialize(**config):
    import models
    global ENGINE, SESSION
    engine = getEngine(**config)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    ENGINE = engine
    SESSION = Session()


SESSION = None
ENGINE = None
