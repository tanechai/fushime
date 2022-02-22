from flask import Flask, request, redirect, url_for, render_template
from flask_login import login_user, logout_user, LoginManager, UserMixin, login_required, current_user

# from functions.schedule_manager import schedule_manager
# from functions.account_manager import account_manager

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore
# import os

app = Flask(__name__)

# app.secret_key = os.urandom(24)

# # ログイン機能のセットアップ
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login" # ログインしてない時に飛ばされる場所

# firebaseの設定を読み込む
# cred = credentials.Certificate()
# firebase_admin.initialize_app(cred)
# db = firestore.client()

#ユーザークラスを定義
class  User(UserMixin):
    def __init__(self,uid):
        self.id = uid


@login_manager.user_loader
def user_loader(uid:str):
    return User(uid)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    name = str(request.form['name'])
    pwd = str(request.form['password'])
    # account = account_manager(db)
    # uid = account.login(name,pwd)
    # if uid != False:
    #     user = User(uid)
    #     login_user(user)
    #     return redirect(url_for("calendar"))
    # else:
    #     return uid



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    name = str(request.form['name'])
    pwd = str(request.form['password'])
    # account = account_manager(db)
    # uid = account.signup(name,pwd)
    # if uid != False:
    #     user = User(uid)
    #     login_user(user)
    #     return redirect(url_for("calendar"))
    # else:
    #     return str(uid)


@app.route('/calendar')
@login_required
def calendar():
    return f'''
    <h1>{current_user.id}さんのカレンダー<h1>
    <a href='regist'>登録</a>
    <a href='logout'>logout</a>
    '''


@app.route('/regist')
@login_required
def regist():
    return f'''
    <h1>登録ページ<h1>
    <a href='calendar'>カレンダーに戻る</a>
    '''


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("login"))


# run the app.
if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)