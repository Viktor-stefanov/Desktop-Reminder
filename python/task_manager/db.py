import hashlib
import hmac
import sqlite3
import os


def is_valid_email(email):
    with sqlite3.connect("profiles") as conn:
        curr = conn.cursor()
        curr.execute("SELECT * FROM users WHERE EMAIL=?", (email, ))
        if (new_email := curr.fetchone()) is None:
            return 1
        else:
            if email == new_email:
                return "New e-mail same as the old one!"
            return "User with this e-mail already exists!"

def is_valid_name(name):
    with sqlite3.connect("profiles") as conn:
        curr = conn.cursor()
        curr.execute("SELECT * FROM users WHERE NAME=?", (name, ))
        if curr.fetchone() is None:
            return 1
        else:
            return "This username is taken!"

def user_exists(name, pwd):
    with sqlite3.connect("profiles") as conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT SALT, PASSWORD FROM users WHERE NAME=?", (name, ))
            returned = cur.fetchall()
            if len(returned) == 0:
                return "Incorrect password or username!"

            salt, hashed = returned[0]
            if is_correct_pwd(hashed, salt, pwd):
                return 1
            return "Incorrect password or username!"
        except Exception as e:
            return e

def get_location(u_name):
    try:
        with sqlite3.connect("profiles") as conn:
            cur = conn.cursor()
            cur.execute("SELECT LOCATION FROM users WHERE NAME=?", (u_name, ))
            if (res := cur.fetchone()) is not None:
                return res
    except Exception as e:
        return e

def register_user(u_name, pwd, email, location):
    with sqlite3.connect("profiles") as conn:
        # add a user when he registers
        try:
            pwd_hash, salt = hashing(pwd)
            cur = conn.cursor()
            cur.execute("INSERT INTO users values (?, ?, ?, ?, ?)", (u_name, pwd_hash, salt, email, location))
            conn.commit()
            return 1
        except sqlite3.IntegrityError:
            return "User with this username already exists"
        except Exception as e:
            return e

def edit_username(u_name, new_un):
    if u_name == new_un:
        return "New username same as the old username"
    with sqlite3.connect("profiles") as conn:
        try:
            curr = conn.cursor()
            curr.execute("UPDATE users SET NAME=? WHERE NAME=?", (new_un, u_name))
            return 1
        except sqlite3.IntegrityError:
            return "User with this username already exists!"
        except Exception as e:
            return e

def edit_password(u_name, pwd, new_pwd):
    if pwd == new_pwd:
        return "New password same as the old one"
    with sqlite3.connect("profiles") as conn:
        try:
            curr = conn.cursor()
            hashed_pwd, salt = hashing(new_pwd)
            curr.execute("UPDATE users SET PASSWORD=?, SALT=? WHERE NAME=?", (hashed_pwd, salt, u_name))
            return 1
        except Exception as e:
            return e

def edit_location(un, location):
    try:
        with sqlite3.connect("profiles") as conn:
            cur = conn.cursor()
            cur.execute("UPDATE users SET LOCATION=? WHERE NAME=?", (location, un))
            return 1
    except Exception as e:
        return e

def create_table(conn):
    # create the table if it doesn't already exists
    conn.execute('''CREATE TABLE users
                (NAME TEXT NOT NULL UNIQUE,
                 PASSWORD TEXT NOT NULL UNIQUE,
                 SALT TEXT NOT NULL,
                 EMAIL TEXT NOT NULL,
                 LOCATION TEXT NOT NULL
                 );''')
    conn.commit()

def hashing(pwd):
    # hash a password
    salt = os.urandom(16)
    pwd_hash = hashlib.pbkdf2_hmac("sha512", pwd.encode(), salt, 100000)
    return pwd_hash, salt

def is_correct_pwd(hash, salt, pwd):
    is_correct = hmac.compare_digest(
        hash,
        hashlib.pbkdf2_hmac("sha512", pwd.encode(), salt, 100000)
    )
    return is_correct