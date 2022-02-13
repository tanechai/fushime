from flask import Flask, escape, request

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/stream')
def stream():
    name = request.args.get("name", "STREAM")
    return f'Hello, {escape(name)}!'

if __name__ == "__main__":
    app.run(host='localhost', port=8080)