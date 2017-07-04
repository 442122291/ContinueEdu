# #coding:utf-8
# import threading
from sqlalchemy import create_engine
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.settings import *
class Db():
    def __init__(self):
        Base = declarative_base()
        engine = create_engine('%s+%s://%s@%s:%s/%s' % (DB_TYPE, DB_DRIVER, DB_USER, DB_HOST, DB_PORT, DB_DATABASE))
        DBSession = sessionmaker(bind=engine)
        self.dbsession = DBSession()
        import models
        Base.metadata.create_all(bind=engine)

    def shutdown(self):
        self.dbsession.close()

    def createSession(self):
        return self.dbsession

    def get(self, table, id):
        return self.dbsession.query(table).filter(table.userID == id).one()

    def select(self, table):
        users = self.dbsession.query(table).all()
        return users


