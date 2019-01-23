import sqlite3, hashlib, random, string, uuid

def add_user(username, password):
    salt = ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(6))
    print('SALT GENERATED FOR '+username+': '+salt)

    connection = sqlite3.connect('db/data.db')
    cursor = connection.cursor()

    cursor.execute('''INSERT INTO UserData(username, password_hash, salt) 
                      VALUES (?, ?, ?)''', (username, hashlib.sha3_512((password+salt).encode()).hexdigest(), salt))

    connection.commit()
    connection.close()

def login(username, password):
    #todo zabezpieczyć username przed SQLinjection
    connection = sqlite3.connect('db/data.db')
    cursor = connection.cursor()

    cursor.execute('''SELECT user_id, password_hash, salt FROM UserData WHERE username = ?''', [username])
    data = cursor.fetchone()
    user_id = data[0]
    password_hash = data[1]
    salt = data[2]
    session_id = None

    if hashlib.sha3_512((password+salt).encode()).hexdigest() == password_hash:
        session_id = str(uuid.uuid4())
        cursor.execute('UPDATE UserData SET session_id = ? WHERE user_id = ?', (session_id, user_id))
        print('SID: '+session_id)
        connection.commit()


    connection.close()

    return session_id

def logout(username):
    connection = sqlite3.connect('db/data.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE UserData SET session_id = NULL WHERE username = ?', [username])
    connection.commit()
    connection.close()

def checkSession(session_id):
    connection = sqlite3.connect('db/data.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM UserData WHERE session_id = ?', [session_id])
    verified = cursor.fetchone()
    connection.close()
    return verified
