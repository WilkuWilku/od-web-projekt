from flask import Flask, render_template, redirect, url_for, request, session
from db import db_init, dao
from time import sleep
import random

app = Flask(__name__)
app.secret_key = 'Gusnq4H7S2O0A-v=2FmaueE>obi/An8yP(DFdk%m1a5ob'
db_init.database_init()

@app.route('/index')
def index():
    verifySessionId()
    return render_template('index.html', username=session.get('usr'))

@app.route('/login', methods=['GET', 'POST'])
def login(error = None):
    if request.method == 'GET':
        return render_template('login.html', error=error)
    else:
        usr = request.form.get('username')
        pwd = request.form.get('password')

        if authenticated_correctly(usr, pwd):
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Nieprawidłowa nazwa użytkownika lub hasło')

@app.route('/logout', methods=['GET'])
def logout():
    dao.logout(session.get('usr'))
    session.clear()
    return redirect(url_for('index'))

@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if validate_signin(username, password):
            #dao.add_user(username, password)
            print('user added: '+username)
            return redirect(url_for('login'))
        print('New user not valid')
        return redirect(url_for('signin'))
    return render_template('signin.html')



def authenticated_correctly(username, password):
    session_id = dao.login(username, password)
    delay = random.randint(250, 750)/1000
    print('response delayed: '+str(delay)+' sec')
    sleep(delay)
    if session_id:
        session['sid'] = session_id
        session['usr'] = username
        session.modified = True
        return True
    else:
        return False

def validate_signin(username, password):
    return username.isalnum() and len(password) >= 8 \
        and len(username) >= 5 \
        and any(char.isdigit() for char in password) \
        and any(char.isupper() for char in password) \
        and any(char.islower() for char in password)


def verifySessionId():
    session_id = session.get('sid')
    if session_id:
        verified_sid = dao.checkSession(session_id)
        if not verified_sid:
            session.clear()

if __name__ == '__main__':
    app.run()