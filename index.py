from flask import Flask, request, redirect, url_for
from flask_login import login_user, logout_user, LoginManager, UserMixin, login_required, current_user
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)

# ログイン機能のセットアップ
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login" # ログインしてない時に飛ばされる場所

users = {'dev@mail.com': {'password': 'secret'}}

# firebaseの設定を読み込む
# cred = credentials.Certificate("path/to/fushime-9ccc3-firebase-adminsdk-9vqsu-a9d6643f4e.json")
# firebase_admin.initialize_app(cred)
# db = firestore.client()

class  User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(req):
    email = req.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    return user


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
                <h1>節目カレンダー<h1>
                <form action='login' method='POST'>
                <input type='text' name='name' id='name' placeholder='name'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    name = request.form['name']
    if request.form['password'] == users[name]['password']:
        user = User()
        user.id = name
        login_user(user)
        return redirect(url_for("calendar"))

    return 'Bad login'


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