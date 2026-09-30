import sqlite3

# Connect to the database
connection = sqlite3.connect("siwes_management.db")

# Create a cursor
cursor = connection.cursor()

# Create the students table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        department TEXT NOT NULL,
        level TEXT NOT NULL
    )
""")

# Save the changes
connection.commit()

print("Database connected successfully!")
print("Students table created successfully!")
# Create the supervisors table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS supervisors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        department TEXT
    )
""")

# Save the changes
connection.commit()

print("Supervisors table created successfully!")
# Create the organizations table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        organization_name TEXT NOT NULL,
        address TEXT,
        contact_person TEXT,
        email TEXT,
        phone TEXT
    )
""")

# Save the changes
connection.commit()

print("Organizations table created successfully!")
# Create the placements table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS placements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        organization_id INTEGER NOT NULL,
        supervisor_id INTEGER,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        status TEXT DEFAULT 'Pending',

        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (organization_id) REFERENCES organizations(id),
        FOREIGN KEY (supervisor_id) REFERENCES supervisors(id)
    )
""")

# Save the changes
connection.commit()

print("Placements table created successfully!")
# Create the attendance table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        attendance_date TEXT NOT NULL,
        status TEXT NOT NULL,
        remarks TEXT,

        FOREIGN KEY (student_id) REFERENCES students(id)
    )
""")

# Save the changes
connection.commit()

print("Attendance table created successfully!")
# Create the logbook table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS logbook (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        entry_date TEXT NOT NULL,
        activity TEXT NOT NULL,
        skills_learned TEXT,
        challenges TEXT,
        supervisor_comment TEXT,
        approval_status TEXT DEFAULT 'Pending',

        FOREIGN KEY (student_id) REFERENCES students(id)
    )
""")

# Save the changes
connection.commit()

print("Logbook table created successfully!")
# Create the evaluations table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        supervisor_id INTEGER NOT NULL,

        technical_skills INTEGER,
        punctuality INTEGER,
        teamwork INTEGER,
        communication INTEGER,
        professionalism INTEGER,

        comments TEXT,
        evaluation_date TEXT NOT NULL,

        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (supervisor_id) REFERENCES supervisors(id)
    )
""")

# ============================================================
# USERS / AUTHENTICATION TABLE
# ============================================================

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE,
        role TEXT NOT NULL,
        is_active INTEGER DEFAULT 1
    )
""")

print("Users table created successfully!")


# Save the changes
connection.commit()

print("Evaluations table created successfully!")