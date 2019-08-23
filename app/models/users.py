from sqlalchemy import Column, Integer, String
from .database import Base
from werkzeug.security import generate_password_hash, check_password_hash

class User(Base):
    __tablename__ = 'TB_USER'

    id_ = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(16))
    password_hash = Column(String(128))

    def __init__(self, username, password):
        self.name = username
        self.password_hash = generate_password_hash(password)

    @classmethod
    def make_onlyone_user(cls,
                          session,
                          username,
                          password):
        """
        database에서 한번만 호출한다.
        """
        user = session.query(cls).filter_by(name=username).first()
        if not user:
            session.add(cls(username, password))
            session.commit()
        else:
            print("user already exists.")  #TODO logger
        return

    @classmethod
    def check_password(cls,
                       session,
                       username,
                       password):
        """
        user는 한명만 쓸꺼니까 대충 떼우자!
        """
        user = session.query(cls).filter_by(name=username).first()
        return check_password_hash(user.password_hash, password)
