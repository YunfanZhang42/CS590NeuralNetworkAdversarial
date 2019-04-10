from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('upload')
def upload():
    return 'pass'


@app.route('download')
def upload():
    return 'pass'
