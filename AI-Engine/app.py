from flask import Flask
import subprocess

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, this is AI-Engine!'

@app.route('/create_agent')
def create_agent():
    subprocess.Popen(["python3", "othello/main.py", "random", "extra", "1000"])
    return 'New Agent has been created!'

if __name__ == '__main__':
    app.run(port=3002, debug=True)
