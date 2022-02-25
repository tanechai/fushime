from flask import Flask, request, redirect, url_for, render_template, flash
from flask_login import login_user, logout_user, LoginManager, UserMixin, login_required, current_user

from functions.schedule_manager import schedule_manager
from functions.account_manager import account_manager

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import datetime
import os, re, json

app = Flask(__name__,static_folder='./templates/images')

app.secret_key = os.urandom(24)

# # ログイン機能のセットアップ
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login" # ログインしてない時に飛ばされる場所

#firebaseの設定を読み込む
# cred = credentials.Certificate('fushime-9ccc3-firebase-adminsdk-9vqsu-a9d6643f4e.json')
if not firebase_admin._apps:
    api_key =json.loads(os.getenv('firestore_apikey'))
    cred = credentials.Certificate(api_key)
    firebase_admin.initialize_app(cred)
    
db = firestore.client()
account = account_manager(db)

# むっくんの関数
def train_type(nyuuryoku:str):
    syubetu={"特急":1,"快速":2,"普通":3}
    if nyuuryoku in syubetu:
        okurisyubetu=syubetu[nyuuryoku]
        return int(okurisyubetu)    
    else:
        return False


#ユーザークラスを定義
class  User(UserMixin):
    def __init__(self,uid):
        self.name = account.user_name(uid)
        self.id = uid
       
@login_manager.user_loader
def user_loader(uid):
    return User(uid)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET': 
        return render_template('login.html')
    check_name = str(request.form['name'])
    password = str(request.form['password'])
    if check_name == '':
        flash('ユーザー名が空欄です')
        return render_template('login.html')
    if check_name == '':
        flash('パスワードが空欄です')
        return render_template('login.html')
    uid= account.login(check_name,password)
    print(uid)
    if uid != False:
        user = User(uid)
        login_user(user)
        return redirect(url_for("calendar"))
    else:
        flash('パスワードかユーザー名が違います')
        return render_template('login.html')


def is_matched(s):
    return True if re.fullmatch('(?i:\A[a-z\d]{8,100}\Z)', s) else False

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    add_name = str(request.form['name'])
    password = str(request.form['password'])
    if add_name == '':
        flash('ユーザー名が空欄です')
        return render_template('signup.html')
    if is_matched(password) != True:
        flash('パスワードは半角英数字8文字以上です')
        return render_template('signup.html')
    uid = account.signup(add_name,password)
    if uid != False:
        user = User(uid)
        login_user(user)
        return redirect(url_for("calendar"))
    else:
        flash('すでに登録済みのユーザーです')
        return render_template('signup.html')


@app.route('/calendar')
@login_required
def calendar():
    return f'''
    <h1>{current_user.name}さんのカレンダー<h1>
    <a href='regist'>登録</a>
    <a href='logout'>logout</a>
    '''


@app.route('/regist', methods=['GET', 'POST'])
@login_required
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    subject = str(request.form['subject'])
    date = str(request.form['date'])
    importance = str(request.form['importance'])
    if subject == '':
        flash('予定名が入力されてません','error')
        return render_template('regist.html')
    if date == '':
        flash('予定日が入力されてません','error')
        return render_template('regist.html')
    # 日付を変数に格納
    dt = datetime.datetime.strptime(date, '%Y-%m-%d')
    year = dt.year
    month = dt.month
    day = dt.day
    level = train_type(importance)
    if not level:
        flash('重要度が不正です','error')
        return render_template('regist.html')
    schedule = schedule_manager(current_user.id,db)
    schedule.add(subject,year,month,day,level)
    return render_template('regist.html',succes ='予定の登録が完了しました' )


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("login"))


# run the app.
if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)