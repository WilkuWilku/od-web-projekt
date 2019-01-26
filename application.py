from flask import Flask, render_template, redirect, url_for, request, session, flash, abort, send_from_directory
from werkzeug.utils import secure_filename
from db import db_init, dao
from time import sleep
import random, os, uuid

app = Flask(__name__)
app.secret_key = 'Gusnq4H7S2O0A-v=2FmaueE>obi/An8yP(DFdk%m1a5ob'
db_init.database_init()
app.config['UPLOAD_FOLDER'] = 'upload/'
if not os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'])):
    os.mkdir(os.path.join(app.config['UPLOAD_FOLDER']))

@app.route('/index')
def index():
    verify_session_id()
    return render_template('index.html', username=session.get('usr'), notesList=session.get('nl'))


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
    dao.logout(session.get('sid'))
    session.clear()
    return redirect(url_for('index'))


@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if validate_signin(username, password):
            dao.add_user(username, password)
            flash('Pomyślnie utworzono nowe konto')
            return redirect(url_for('index'))
        print('New user not valid')
        return redirect(url_for('signin'))
    if request.method == 'GET':
        verify_session_id()
        return render_template('signin.html', username=session.get('usr'))


@app.route('/api/checkUsername', methods=['POST'])
def check_username():
    username = request.get_json().get('username')
    if not username.isalnum() or dao.is_username_taken(username):
        return 'T'
    else:
        return 'F'


@app.route('/view/<string:file_id>', methods=['GET'])
def view_notes(file_id):
    if not verify_note_access(file_id):
        abort(403)

    with open(os.path.join(app.config.get('UPLOAD_FOLDER'), file_id+'.txt'), 'r') as file:
        note_content = file.read()

    note_data = None

    for note in session.get('nl'):
        if note.get('file_id') == file_id:
            note_data = note
    return render_template('note.html', note=note_data, note_content=note_content)


@app.route('/upload', methods=['POST'])
def upload_notes():
    verify_session_id()
    file = request.files.get('file')
    username = session.get('usr')
    if file and username:
        file_id = str(uuid.uuid4())
        while dao.is_note_uuid_taken(file_id):
            file_id = str(uuid.uuid4())

        secure_fname = secure_filename(file.filename)
        uuid_filename = file_id + '.txt'
        file.save(os.path.join(app.config.get('UPLOAD_FOLDER'), uuid_filename))
        dao.add_notes(secure_fname, file_id, username)

        notes_list = session.get('nl', [])
        notes_list.append({
            "file_id": file_id,
            "name": secure_fname
        })
        session['nl'] = notes_list
    return redirect(url_for('index'))


@app.route('/download/<string:file_id>')
def download_notes(file_id):
    verify_session_id()
    if not verify_note_access(file_id):
        abort(403)
    filename = dao.get_secure_filename(file_id)
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=file_id+'.txt',
                               attachment_filename=filename, as_attachment=True)


def authenticated_correctly(username, password):
    if not username.isalnum():
        return False
    session_id, notes = dao.login(username, password)
    delay = random.randint(420, 850)/1000
    sleep(delay)
    if session_id:
        session['sid'] = session_id
        session['usr'] = username
        session['nl'] = notes
        session.modified = True
        return True
    else:
        return False


def validate_signin(username, password):
    return username.isalnum() and len(password) >= 8 \
        and len(username) >= 5 \
        and any(char.isdigit() for char in password) \
        and any(char.isupper() for char in password) \
        and any(char.islower() for char in password) \
        and not dao.is_username_taken(username)


def verify_session_id():
    session_id = session.get('sid')
    if session_id:
        verified_sid = dao.check_session(session_id)
        if not verified_sid:
            session.clear()


def verify_note_access(file_id):
    return dao.confirm_owner_of_file(file_id, session.get('sid'), session.get('usr'))


if __name__ == '__main__':
    app.run()
