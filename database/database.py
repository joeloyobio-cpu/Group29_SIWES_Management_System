import sqlite3
from pathlib import Path


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_PATH = PROJECT_ROOT / "SIWES.db"
LEGACY_DATABASE_PATH = PROJECT_ROOT / "siwes_management.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    """
    Return a connection to the central SIWES database.
    All project modules should use this function.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    # Enable foreign key relationships
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    # --------------------------------------------------------
    # USERS / AUTHENTICATION
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # STUDENTS
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # SUPERVISORS
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS supervisors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            department TEXT
        )
    """)

    # --------------------------------------------------------
    # ORGANIZATIONS
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # PLACEMENTS
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS placements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            organization_id INTEGER NOT NULL,
            supervisor_id INTEGER,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',

            FOREIGN KEY (student_id)
                REFERENCES students(id),

            FOREIGN KEY (organization_id)
                REFERENCES organizations(id),

            FOREIGN KEY (supervisor_id)
                REFERENCES supervisors(id)
        )
    """)

    # --------------------------------------------------------
    # ATTENDANCE
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            attendance_date TEXT NOT NULL,
            status TEXT NOT NULL,
            remarks TEXT,

            FOREIGN KEY (student_id)
                REFERENCES students(id)
        )
    """)

    # --------------------------------------------------------
    # DIGITAL LOGBOOK
    #
    # This structure comes from the logbook teammate's
    # existing LogbookEntry/database design.
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logbook_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            week_number INTEGER NOT NULL,
            activities TEXT NOT NULL,
            skills_learned TEXT,
            challenges TEXT,
            supervisor_comment TEXT,
            status TEXT DEFAULT 'Pending',

            FOREIGN KEY (student_id)
                REFERENCES students(id)
        )
    """)

    # --------------------------------------------------------
    # OLD / LEGACY LOGBOOK TABLE
    #
    # Kept for compatibility with existing code.
    # New Digital Logbook work should use logbook_entries.
    # --------------------------------------------------------

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

            FOREIGN KEY (student_id)
                REFERENCES students(id)
        )
    """)

    # --------------------------------------------------------
    # EVALUATIONS
    # --------------------------------------------------------

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

            FOREIGN KEY (student_id)
                REFERENCES students(id),

            FOREIGN KEY (supervisor_id)
                REFERENCES supervisors(id)
        )
    """)

    connection.commit()
    connection.close()


# ============================================================
# MIGRATE LEGACY DATABASE
# ============================================================

def migrate_legacy_database():

    if not LEGACY_DATABASE_PATH.exists():
        print("No legacy database found.")
        return

    print("Legacy database found.")
    print("Checking existing data...")

    old_connection = sqlite3.connect(
        LEGACY_DATABASE_PATH
    )

    old_connection.execute(
        "PRAGMA foreign_keys = OFF"
    )

    old_cursor = old_connection.cursor()

    new_connection = get_connection()
    new_cursor = new_connection.cursor()

    tables = [
        "users",
        "students",
        "supervisors",
        "organizations",
        "placements",
        "attendance",
        "logbook",
        "evaluations"
    ]

    try:

        for table in tables:

            # Check if table exists in old database
            old_cursor.execute("""
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                AND name = ?
            """, (table,))

            if old_cursor.fetchone() is None:
                continue

            # Check whether target table already has data
            new_cursor.execute(
                f"SELECT COUNT(*) FROM {table}"
            )

            existing_count = new_cursor.fetchone()[0]

            # Don't repeatedly copy the same legacy data
            if existing_count > 0:
                print(
                    f"{table}: already contains data. "
                    f"Migration skipped."
                )
                continue

            # Get columns
            old_cursor.execute(
                f"PRAGMA table_info({table})"
            )

            columns = [
                row[1]
                for row in old_cursor.fetchall()
            ]

            if not columns:
                continue

            column_list = ", ".join(columns)

            # Read old records
            old_cursor.execute(
                f"SELECT {column_list} FROM {table}"
            )

            rows = old_cursor.fetchall()

            if not rows:
                continue

            placeholders = ", ".join(
                ["?"] * len(columns)
            )

            new_cursor.executemany(
                f"""
                INSERT OR IGNORE INTO {table}
                ({column_list})
                VALUES ({placeholders})
                """,
                rows
            )

            print(
                f"Migrated {len(rows)} record(s) "
                f"from {table}."
            )

        new_connection.commit()

        print("Legacy database migration completed.")

    except sqlite3.Error as error:

        new_connection.rollback()

        print(
            f"Migration error: {error}"
        )

        raise

    finally:

        old_connection.close()
        new_connection.close()


# ============================================================
# COMPLETE DATABASE SETUP
# ============================================================

def setup_database():

    initialize_database()

    migrate_legacy_database()

    print()
    print("==========================================")
    print("SIWES DATABASE READY")
    print("==========================================")
    print(f"Database: {DATABASE_PATH}")


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":

    setup_database()