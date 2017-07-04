from flask import Flask
from flask import abort
from flask import redirect
from requests import Session

from app.Model.models import *
from flask import request,render_template
from sqlalchemy.ext.declarative import declarative_base

from app import app
from app.Model.database import Db
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/user/<name>')
def sayHello(name):
    if name == 'baidu':
        return redirect('http://www.baidu.com')
    elif name == 'NO':
        return abort(404)

    return '<h1> Hello,%s </h1>' % name
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, VARCHAR
Base = declarative_base()
class User(UserMixin, Base):
    __tablename__ = 'user'
    userID = Column(Integer, primary_key=True)
    username = Column(String(64),unique=True)
if __name__ == '__main__':
    # app.run(debug=True)
    user = User()
    # print user.find_first(User, email='442122291@qq.com')
    db = Db()
    session = db.createSession()
    # result = session.query(user).one()
    # print session.query(User).filter(User.email =='442122291@qq.com' ).one()
    # user = session.query(User).filter(User.userID == '1').one()
    # print user
    # courses = session.query(Course).all()
    # for course in courses:
    #     print course.title
    # temp_template = render_template('course.html', courses=courses)
    # print result.username

    # Session["isLogin"] = False
    # Session["username"] = 'asdf'
    #
    # print Session['username']
    # db = Db()
    session = db.createSession()

    # take = Take()
    # results = session.query(Take).filter(Take.userid == 1).all()
    # for result in results:
    #     course = session.query(Course).filter(Course.courseID == result.courseid).one()
    #     print result.courseid, course.title
        # print result.courseid
    # print take.userid, take.courseid
    # take.insert(take)
    # session.add(take)
    # session.commit()
    # user = session.query(User).filter(User.username == 'ryc').one()
    # print user.userID
    # take = Take(userid=1, courseid=1)
    # take.delete(take)
    session.query(Take).filter(Take.userid==1,Take.courseid==1).delete()
    session.commit()