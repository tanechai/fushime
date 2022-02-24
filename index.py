from flask import Flask, request, redirect, url_for, render_template
from flask_login import login_user, logout_user, LoginManager, UserMixin, login_required, current_user

from functions.schedule_manager import schedule_manager
from functions.account_manager import account_manager

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import datetime
import os,re, json

app = Flask(__name__,static_folder='./templates/images')

app.secret_key = os.urandom(24)

# # ログイン機能のセットアップ
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login" # ログインしてない時に飛ばされる場所

# firebaseの設定を読み込む
# api_key =json.loads(os.getenv('firestore_apikey'))
# cred = credentials.Certificate(api_key)
cred = credentials.Certificate('fushime-9ccc3-firebase-adminsdk-9vqsu-a9d6643f4e.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
account = account_manager(db)



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
    uid= account.login(check_name,password)
    print(uid)
    if uid != False:
        user = User(uid)
        print(user)
        login_user(user)
        return redirect(url_for("calendar"))
    else:
        return render_template('login.html', error='パスワードかユーザー名が違います')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    add_name = str(request.form['name'])
    password = str(request.form['password'])
    if re.match('\A[a-z\d]{8,100}\Z(?i)',password) != True:
        return render_template('signup.html',error='パスワードは半角英数字8文字以上です')
    uid = account.signup(add_name,password)
    if uid != False:
        user = User(uid)
        login_user(user)
        return redirect(url_for("calendar"))
    else:
        return render_template('signup.html', error='すでに登録済みのアカウントです')


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
    if subject == '' or date == '':
        return render_template('regist.html',error = '予定名と日が入力されてません')
    # '2022-02-02'
    dt = datetime.datetime.strptime(date, '%Y-%m-%d')
    year = dt.year
    month = dt.month
    day = dt.day
    schedule = schedule_manager(current_user.id,db)
    schedule.add(subject,year,month,day,1)
    return render_template('regist.html',error = '予定が追加されました')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("login"))


# run the app.
if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)