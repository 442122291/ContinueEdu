#coding:utf-8
import os
from flask import Flask
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from sqlalchemy.ext.declarative import declarative_base
from flask import request, render_template
from Model.database import Db
db = Db()
app = Flask(__name__)
app.secret_key = os.urandom(24)
loginManager = LoginManager(app)
# 如果需要延迟创建app 可使用
# loginManager = LoginManager()
# loginManager.init_app(app)

loginManager.session_protection = "strong"
# 可以设置None,'basic','strong'  以提供不同的安全等级,一般设置strong,如果发现异常会登出用户

loginManager.login_view = "login"
# 这里填写你的登陆界面的路由
from sqlalchemy import Column,String,Integer
from flask_login import UserMixin
Base = declarative_base()
class User(UserMixin, Base):
    __tablename__ = 'user'
    userID = Column(Integer, primary_key=True)
    username = Column(String(64),unique=True)

    def get_id(self):
        text_type = str
        try:
            return text_type(self.userID)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def is_authenticated(self):
        return True
    #
    # def is_authenticated(self):
    #     return True
    # def is_active(self):
    #     return True
@loginManager.user_loader
def load_user(user_id):
    # print user_id
    session = db.createSession()
    user = session.query(User).filter(User.userID == user_id).one()
    # print user.userID
    return user
    # return User.query.get(int(user_id))

@app.route('/')
def test():
    return "hello, noname."

@app.route('/index')
# @login_required
def index():
    # print current_user.is_authenticated()
    temp_template = render_template('test.html', current_user=current_user)
    return temp_template
    # return "只有登陆用户能看到我"


@app.route('/login')
def login():
    #获取要登陆的用户对象
    dbsession = db.createSession()
    # user = User.query.filter_by(username = 'ryc').first()
    user = dbsession.query(User).filter(User.username == 'ryc').one()
    # print user.userID
    dbsession.close()
    #第一个参数传入用户对象,第二个参数 传入 以后是否自动登陆
    login_user(user)
    return "success!"
    # temp_template = render_template('test.html', current_user=current_user)
    # return temp_template
@app.route('/logout')
def logout():
    #登出
    logout_user
    # return "logout!"
    temp_template = render_template('test.html', current_user=current_user)
    return temp_template

if __name__ == '__main__':
    app.run(debug=True)