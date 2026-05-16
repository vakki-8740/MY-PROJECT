import sqlite3
from config import Config

def get_db_connection():
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'user')''')
        
    c.execute('''CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        mobile TEXT,
        email TEXT,
        service_password TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id))''')

    # Pre-Login Data (Signup Not Needed)
    if not c.execute("SELECT id FROM users WHERE username='user1'").fetchone():
        c.execute("INSERT INTO users (username, password, role) VALUES ('user1', '12345', 'user')")
    if not c.execute("SELECT id FROM users WHERE username='admin'").fetchone():
        c.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')")
    
    conn.commit()
    conn.close()

def verify_login(username, password):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()
    conn.close()
    return dict(user) if user else None

def save_request(user_id, name, mobile, email, pwd):
    conn = get_db_connection()
    conn.execute("INSERT INTO requests (user_id, name, mobile, email, service_password) VALUES (?,?,?,?,?)",
                 (user_id, name, mobile, email, pwd))
    conn.commit()
    conn.close()

def get_user_requests(user_id):
    conn = get_db_connection()
    reqs = conn.execute("SELECT * FROM requests WHERE user_id=? ORDER BY created_at DESC", (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in reqs]

def get_all_login_data():
    conn = get_db_connection()
    users = conn.execute("SELECT username, password, role FROM users").fetchall()
    conn.close()
    return [dict(u) for u in users]

def get_all_requests():
    conn = get_db_connection()
    reqs = conn.execute("SELECT r.*, u.username FROM requests r JOIN users u ON r.user_id=u.id ORDER BY r.created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in reqs]