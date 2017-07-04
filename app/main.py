# coding: utf-8
import re
import sys

from flask import flash

reload(sys)
sys.setdefaultencoding('utf-8')
import os
from flask import Flask, url_for
from app.Model.models import *
from flask import request,render_template, redirect
from app import app
from app.Model.database import Db
# from werkzeug.security import generate_password_hash
# from werkzeug.security import check_password_hash
from flask_login import (LoginManager, login_required, login_user, logout_user, current_user)
app = Flask(__name__)
app.secret_key = os.urandom(24)
loginManager = LoginManager(app)

loginManager.session_protection = "strong"
# 可以设置None,'basic','strong'  以提供不同的安全等级,一般设置strong,如果发现异常会登出用户

loginManager.login_view = "login"
loginManager.login_message = "请登录"
db = Db()
dbsession = db.createSession()
courses = dbsession.query(Course).all()
dbsession.close()

@loginManager.user_loader
def load_user(user_id):
    session = db.createSession()
    user = session.query(User).filter(User.userID == user_id).one()
    return user

@app.route('/test')
def test():
    return "hello,world"

@app.route('/')
@app.route('/index')
def index():
    temp_template = render_template('course.html', courses=courses, current_user=current_user)
    return temp_template


@app.route('/login')
def login():
    return render_template('login.html')


_RE_MD5 = re.compile(r'^[0-9a-z]{6,}$')
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/doRegister')
def doRegister():
    name = request.args.get('name', '').encode('utf-8').strip()
    username = request.args.get('username', '').encode('utf-8').strip()
    email = request.args.get('email').strip().lower()
    password = request.args.get('password')
    if not name:
        return "名字不能为空！"
    if not email :
        return "邮箱不能为空！"
    if not _RE_MD5.match(password):
        return "请输入6位以上的密码！"
    user = User(name=name, username=username, password=password, email=email)
    result = user.find_first(User, email)
    if result is not None:
        return "邮箱已经存在"
    else:
        user.insert(user)
        flash('注册成功')
        return redirect(url_for('login'))

@app.route('/doLogin', methods=['POST'])
def doLogin():
    username = request.form['username'].encode('utf-8')
    password = request.form['password']
    dbsession = db.createSession()
    # try:
    # 获取要登陆的用户对象
    user = dbsession.query(User).filter(User.username == username).one()
    dbsession.close()
    if user.password == password:
        # 第一个参数传入用户对象,第二个参数 传入 以后是否自动登陆
        login_user(user)
        courses = dbsession.query(Course).all()
        temp_template = render_template('course.html', courses=courses, current_user=current_user)
        return temp_template
    # return "登录成功!"
    else:
        flash("账号或密码错误")
        return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    temp_template = render_template('course.html', courses=courses, current_user=current_user)
    return temp_template

@app.route('/take')
@login_required
def take():
    dbsession = db.createSession()
    cid = int(request.args.get('id').encode('utf-8'))
    uid = current_user.userID
    take_all = dbsession.query(Take).filter(Take.userid == uid).all()
    dbsession.close()


    if cid in [one.courseid for one in take_all]:
        flash("该课程已选中")
        return redirect(url_for('index'))
    else:
        take = Take(userid=uid, courseid=cid)
        take.insert(take)
        flash("选课成功")
        return redirect(url_for('index'))
        # return "选课成功"

@app.route('/untake')
@login_required
def unTake():

    cid = int(request.args.get('id').encode('utf-8'))
    uid = current_user.userID
    take = Take(userid=uid, courseid=cid)
    dbsession = db.createSession()
    dbsession.query(Take).filter(Take.userid == uid, Take.courseid == cid).delete()
    dbsession.commit()
    flash("退课成功")
    # return "退课成功"
    return redirect(url_for('check'))

@app.route('/check')
@login_required
def check():
    dbsession = db.createSession()
    uid = current_user.userID
    takes= dbsession.query(Take).filter(Take.userid == uid).all()
    dbsession.close()
    myCourses = []
    for take in takes:
        course = dbsession.query(Course).filter(Course.courseID == take.courseid).one()
        myCourses.append(course)
    temp_template = render_template('take.html', myCourses=myCourses, current_user=current_user)

    return temp_template
        # print result.courseid, course.title
if __name__ == '__main__':
    db = Db()
    # session = db.createSession()
    # app.run(debug=True)
    app.run(host='0.0.0.0')
    db.shutdown()