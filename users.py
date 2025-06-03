import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

def create_user(email,username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (email,username,password) VALUES (?, ?)", (email,username, hash_password(password)))
    conn.commit()
    conn.close()

def check_user(email, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE email=?", (email,))
    result = c.fetchone()
    conn.close()
    if result:
        return verify_password(password, result[0])
    return False
