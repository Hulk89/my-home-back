from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

SESSION = None
ENGINE = None

def getEngine(**kwargs):
    engine_str = 'mysql+mysqldb://{user}:{password}@{host}:{port}/{db}'
    engine = create_engine(engine_str.format(**kwargs),
                           pool_size=20,
                           pool_recycle=500,
                           max_overflow=20)
    return engine


def initialize(**config):
    global ENGINE, SESSION
    from models import models  # package.module
    engine = getEngine(**config)
    Base.metadata.create_all(engine)
    SESSION = scoped_session(sessionmaker(bind=engine))

    ENGINE = engine
    session = SESSION()

    models.User.make_onlyone_user(session,
                                  config["root_name"],
                                  config["root_password"])

    session.close()

