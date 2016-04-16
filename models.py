import datetime as dt

from sqlalchemy import (create_engine, Column, DateTime, String,
                        Integer, ForeignKey, Boolean)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, session_maker
from utils.validation import validate_email_address

engine = create_engine('sqlite:///annoyingbeerguy.db')
Base = declarative_base()

Session = session_maker(bind=engine)


class User(Base):

    __tablename__ = 'user'

    uid = Column(Integer, primary_key=True)
    name = Column(String)
    email_address = Column(String)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def add(cls, email_address, name):
        validate_email_address(email_address)
        session = Session()
        session.add(
            User(**{'email_address': email_address,
                    'name': name})
        )
        session.close()

    def expire(self):
        ''' expires all alerts '''
        pass

    def __repr__(self):
        pass

class Alert(Base):

    __tablename__ = 'alerts'

    uid = Column(Integer, ForeignKey('user.uid'))
    query_id = Column(Integer, primary_key=True)
    query = Column(String)
    created = Column(DateTime)
    expired = Column(Boolean)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        pass

    def expire(self):
        ''' expires this particular alert '''
        pass

    @classmethod
    def add(cls, uid, query):
        session = Session()
        session.add(
            Alert(**{'uid': uid, 'query': query,
                     'created': dt.datetime.today()})
        )
        session.close()
