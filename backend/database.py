import sqlite3
from datetime import datetime

# Connect to (or create) the database
def get_connection():
    conn = sqlite3.connect("attendance.db")
    return conn

# Create tables when app starts
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Table to store registered students
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            registered_on TEXT
        )
    ''')

    # Table to store attendance records
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database tables created!")

# Add a new student
def add_student(name):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO students (name, registered_on) VALUES (?, ?)",
            (name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        print(f"✅ Student '{name}' registered!")
    except sqlite3.IntegrityError:
        print(f"⚠️ Student '{name}' already exists!")
    conn.close()

# Mark attendance
def mark_attendance(name):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now()
    cursor.execute(
        "INSERT INTO attendance (student_name, date, time) VALUES (?, ?, ?)",
        (name, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"))
    )
    conn.commit()
    conn.close()
    print(f"✅ Attendance marked for '{name}'!")

# Get all attendance records
def get_all_attendance():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance ORDER BY date DESC, time DESC")
    records = cursor.fetchall()
    conn.close()
    return records

# Run this file to test
if __name__ == "__main__":
    create_tables()
    # Get all registered students
def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM students")
    students = [row[0] for row in cursor.fetchall()]
    conn.close()
    return students