from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String, Boolean, column

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id',ondelete='CASCADE'),nullable=False)


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,CheckConstraint('value > 3'), index=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    uuid_api_key = Column(String)
