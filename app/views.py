# coding: utf-8
import re
import sys

from flask import flash
from flask import url_for
from flask_cache import Cache

reload(sys)
sys.setdefaultencoding('utf-8')
from app.Model.models import *
from flask import request,render_template, redirect
# from flask import session
from app import app
from app.Model.database import Db
from hashlib import md5
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import (LoginManager, login_required, login_user,logout_user, UserMixin)
config = {
  'CACHE_TYPE': 'filesystem',
  'CACHE_DIR': 'Cache',
  'CACHE_THRESHOLD': 30,
}
cache = Cache(app, config=config)
db = Db()
course = ''
session = {}
session['isLogin'] = False


@app.route('/test')
def test():
    return "hello,world"

@app.route('/')
@app.route('/index')
def index():
    dbsession = db.createSession()
    cache_key = 'noUser'
    courses = dbsession.query(Course).all()
    dbsession.close()
    temp_template = render_template('course.html', courses=courses, cookies=session)
    cache.set(temp_template, cache_key)
    return temp_template


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/user')
def searchUser():
    result = db.select(User)
    return result[0].username


@app.route('/get')
def show_user():
    id = request.args.get('id')
    user = db.get(User, id)
    return user.username

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
    # password1 = request.args.get('password1')
    # password2 = request.args.get('password2')
    if not name:
        return "名字不能为空！"
    if not email :
        return "邮箱不能为空！"
    if not _RE_MD5.match(password):
        return "请输入6位以上的密码！"
    user = User(name=name, username=username, password=password, email=email)
    result = user.find_first(User, email)
    if result is not None:
        # flash("邮箱已经存在")
        # return redirect(url_for('register'))
        return "邮箱已经存在"
    else:
        user.insert(user)
        return redirect(url_for('login'))

@app.route('/doLogin', methods=['POST'])
def doLogin():
    username = request.form['username'].encode('utf-8')
    password = request.form['password']
    dbsession = db.createSession()
    # try:
    user = dbsession.query(User).filter(User.username == username).one()
    if user.password == password:
        session['isLogin'] = True
        session['username'] = user.username
        session['id'] = user.userID
        # cache_key = 'courses'
        # # 查询缓存
        # temp_template = cache.get(cache_key)
        # if temp_template:
        #     session.close()
        #     return temp_template
        courses = dbsession.query(Course).all()
        dbsession.close()
        temp_template = render_template('course.html', courses=courses, cookies=session)
        # cache.set(temp_template, cache_key)
        return temp_template
    # return "登录成功!"
    else:
        flash("账号或密码错误")
        return redirect(url_for('login'))
    # except:
    #     return "账号不存在!"
    # finally:
    #     session.close()

@app.route('/logout')
def logout():
    from flask import session
    session['isLogin'] = False
    if 'username' in session:
        session.pop('username')
    if 'id' in session:
        session.pop('id')
    cache_key = 'noUser'
    # 查询缓存
    temp_template = cache.get(cache_key)
    if temp_template:
        return temp_template
    dbsession = db.createSession()
    courses = dbsession.query(Course).all()
    dbsession.close()
    temp_template = render_template('course.html', courses=courses, cookies=session)
    return temp_template

@app.route('/take')
def take():
    dbsession = db.createSession()
    courses = dbsession.query(Course).all()
    dbsession.close()
    if not session['isLogin']:

        # temp_template = render_template('course.html', courses=courses, cookies=session)

        # return temp_template
        return "您尚未登录!"
    dbsession = db.createSession()
    courseid = request.args.get('id').encode('utf-8')
    uid = session['id']
    take_all = dbsession.query(Take).filter(Take.userid == uid).all()
    print [one.courseid for one in take_all]
    if courseid in [one.courseid for one in take_all]:
        return "该课程已选中"
    else:
        take = Take(userid=session['id'], courseid=courseid)
        take.insert(take)
        return "选课成功"

@app.route('/check')
def check():
    dbsession = db.createSession()
    uid = request.args.get('id').encode('utf-8')
    takes= dbsession.query(Take).filter(Take.userid == uid).all()
    myCourses = []
    for take in takes:
        course = dbsession.query(Course).filter(Course.courseID == take.courseid).one()
        myCourses.append(course.title)
    temp_template = render_template('take.html', myCourses=myCourses, cookies=session)
    dbsession.close()
    return temp_template
        # print result.courseid, course.title
