
import sqlite3

def create_database():
    conn = sqlite3.connect("college.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        student_id TEXT PRIMARY KEY,
        name TEXT,
        program TEXT,
        department TEXT,
        semester INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS marks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        subject TEXT,
        internal INTEGER,
        external INTEGER,
        total INTEGER,
        percentage REAL
    )
    """)

    cur.execute("INSERT OR IGNORE INTO users VALUES(1,'admin','admin123','Admin')")
    cur.execute("INSERT OR IGNORE INTO users VALUES(2,'staff','staff123','Staff')")
    cur.execute("INSERT OR IGNORE INTO users VALUES(3,'student','student123','Student')")

    conn.commit()
    conn.close()
