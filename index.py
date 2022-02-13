from flask import Flask, escape, request

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello, World!<h1>'

if __name__ == "__main__":
    app.run(host='localhost', port=8080)