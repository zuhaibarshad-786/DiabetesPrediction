import sqlite3
conn = sqlite3.connect("users.db")
c = conn.cursor()
c.execute("CREATE TABLE users (email TEXT,username TEXT, password TEXT)")
conn.commit()
conn.close()
