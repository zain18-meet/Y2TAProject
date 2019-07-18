from werkzeug.security import check_password_hash, generate_password_hash
import os
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///database.db')

DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()



#### USER TABLE DATABASE ####
class User(Base, UserMixin):

    __tablename__ = "users"

    id                       = Column(Integer, primary_key=True, autoincrement=True)
    email                    = Column(String, unique=True, nullable=False)
    pw_hash                = Column(String)
    name                 = Column(String, nullable=False)

    def __repr__(self):
      return "<User: %s, password: %s>" % (
        self.email, self.pw_hash)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)





Base.metadata.create_all(engine)
