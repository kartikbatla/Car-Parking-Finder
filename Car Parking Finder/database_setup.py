import sqlite3
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, name TEXT, email TEXT, location TEXT)''')
    conn.commit()
    conn.close()

init_db()  # Call this function when the app starts to create the database if it doesn't exist
