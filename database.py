import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            details TEXT NOT NULL,
            screenshot TEXT
        )
    ''')
    conn.commit()
    conn.close()
