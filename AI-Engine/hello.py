from flask import Flask
import subprocess

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/create_agent')
def create_agent():
    subprocess.run(["python3", "othello/main.py", "random", "extra", "1000"])
    return 'New Agent has been created!'
