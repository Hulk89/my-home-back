from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

SESSION = None
ENGINE = None

def getEngine(**kwargs):
    engine_str = 'mysql+mysqldb://{user}:{password}@{host}:{port}/{db}'
    engine = create_engine(engine_str.format(**kwargs))
    return engine


def initialize(**config):
    global ENGINE, SESSION
    from models import models  # package.module
    engine = getEngine(**config)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    ENGINE = engine
    SESSION = Session()

    models.User.make_onlyone_user(SESSION,
                                  config["root_name"],
                                  config["root_password"])


