from flask import Flask, render_template

app = Flask(__name__)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')


if __name__ == '__main__':
    app.run()