#coding:utf-8
from sqlalchemy import Column, Integer, String, VARCHAR, Text, CHAR, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from database import Db
from flask_login import UserMixin
Base = declarative_base()

class Model(UserMixin):
    def __init__(self):
        self.db = Db()
    def insert(self, cls):
        session = self.db.createSession()
        try:
            session.add(cls)
            session.commit()
            session.close()
        except:
             pass
    def delete(self, cls):
        try:
            session = self.db.createSession()
            session.delete(cls)
            session.commit()
            session.close()
        except:
             pass
    def select(self, cls):
        session = self.db.createSession()
        results = session.query(cls).all()
        session.close()
        return results
    def find_first(self, cls, email):
        dbsession = self.db.createSession()
        # news = session.query(News).filter(News.id == result_['id']).first()
        result = dbsession.query(cls).filter(cls.email == email).first()
        dbsession.close()
        return result

# 表的结构

class User(Model, Base):
    # 表的名字:
    __tablename__ = 'user'

    userID = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(20), nullable=False)
    password = Column(VARCHAR(20), nullable=False)
    sex = Column(VARCHAR(1))
    email = Column(VARCHAR(30), nullable=False)
    tel = Column(VARCHAR(11))
    address = Column(VARCHAR(50))
    age = Column(Integer)

    def __init__(self, name='', username='', password='', email=''):
        self.db = Db()
        self.name = name
        self.username = username
        self.password = password
        self.email = email

    def get_id(self):
        text_type = str
        try:
            return text_type(self.userID)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def is_authenticated(self):
            return True

class Teacher(Base, Model):
    __tablename__ = 'teacher'

    teacherID = Column(VARCHAR(10), primary_key=True)
    name = Column(VARCHAR(10), nullable=False)
    salary = Column(Integer)

class Course(Base, Model):
    __tablename__ = 'course'

    courseID = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(20), nullable=False)
    credit = Column(Integer)

class Take(Base, Model):
    __tablename__ = 'take'

    userid = Column(Integer, ForeignKey('user.userID'), primary_key=True)
    courseid = Column(VARCHAR(10), ForeignKey('course.courseID'), primary_key=True)
    grade = Column(Integer)

    def __init__(self, userid='', courseid=''):
        self.db = Db()
        self.userid = userid
        self.courseid = courseid









# user = session.query(User).one()
# print user.username