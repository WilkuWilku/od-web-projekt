import sqlite3


def database_init():
    connection = sqlite3.connect('db/data.db')
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS UserData (
               user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
               username TEXT NOT NULL UNIQUE,
               session_id TEXT,
               password_hash TEXT NOT NULL,
               salt TEXT NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Notes (
               secure_name TEXT NOT NULL,
               user_id INTEGER NOT NULL,
               uuid_filename TEXT PRIMARY KEY NOT NULL,
               FOREIGN KEY (user_id) REFERENCES UserData(user_id))''')

    connection.commit()
    connection.close()


def drop_users_table():
    connection = sqlite3.connect('db/data.db')
    cursor = connection.cursor()

    cursor.execute('''DROP TABLE IF EXISTS UserData''')

    connection.commit()
    connection.close()


def drop_notes_table():
    connection = sqlite3.connect('db/data.db')
    cursor = connection.cursor()

    cursor.execute('''DROP TABLE IF EXISTS Notes''')

    connection.commit()
    connection.close()
