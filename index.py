from flask import Flask, request, redirect, url_for, render_template
from flask_login import login_user, logout_user, LoginManager, UserMixin, login_required, current_user
import os
from functions import firestore
app = Flask(__name__)

app.secret_key = os.urandom(24)

# ログイン機能のセットアップ
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login" # ログインしてない時に飛ばされる場所

users = {'dev@mail.com': {'password': 'secret'}}

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
    name = req.form.get('name')
    password = req.form.get('password')
    if name not in users:
        #　ここにサインイン処理を書く
        firestore.signin(name,password)
        return

    user = User()
    user.id = name

    return user


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return '''
                <h1>節目カレンダー<h1>
                <form action='login' method='POST'>
                <input type='text' name='name' id='addname' placeholder='name'/>
                <input type='password' name='password' id='addpassword' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''
    name = 'test'
    password = 'pass'
    
    return redirect("login")


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
    <form action='regist' method='POST'>
    <input type='text' name='' id='' placeholder=''/>
    <input type='password' name='' id='' placeholder=''/>
    <input type='submit' name='submit'/>
    </form>
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