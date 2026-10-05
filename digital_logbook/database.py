# import sqlite3 means that we are importing the sqlite3 module, 
# which allows us to interact with SQLite databases in Python.
import sqlite3

from logbook import LogbookEntry

def row_to_entry(row):

    return LogbookEntry(
        entry_id=row[0],
        student_id=row[1],
        date=row[2],
        week_number=row[3],
        activities=row[4],
        skills_learned=row[5],
        challenges=row[6],
        supervisor_comment=row[7],
        status=row[8]
    )

# create_database() function is defined to create a database and a table for 
# logbook entries if they do not already exist.
def create_database():
    connection = sqlite3.connect("siwes.db")

    cursor = connection.cursor()

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
            status TEXT DEFAULT 'Pending'
        )
    """)

    connection.commit()
    connection.close()


create_database()

# save_entry(entry) function is defined to save a logbook entry to the database.
def save_entry(entry):

    connection = None

    try:
        connection = sqlite3.connect("siwes.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO logbook_entries (
                student_id,
                date,
                week_number,
                activities,
                skills_learned,
                challenges,
                supervisor_comment,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            entry.student_id,
            entry.date,
            entry.week_number,
            entry.activities,
            entry.skills_learned,
            entry.challenges,
            entry.supervisor_comment,
            entry.status
        ))

        entry.entry_id = cursor.lastrowid

        connection.commit()

        return entry

    except sqlite3.Error as error:
        print("Database error:", error)
        return None

    finally:
        if connection:
            connection.close()

def entry_exists(student_id, date, exclude_id=None):

    connection = sqlite3.connect("siwes.db")
    cursor = connection.cursor()

    query = """
        SELECT id
        FROM logbook_entries
        WHERE student_id = ?
        AND date = ?
    """

    parameters = [
        student_id,
        date
    ]

    if exclude_id is not None:
        query += " AND id != ?"
        parameters.append(exclude_id)

    cursor.execute(
        query,
        parameters
    )

    result = cursor.fetchone()

    connection.close()

    return result is not None

# get_entries(student_id) function is defined to retrieve all logbook entries for a 
# specific student from the database.
# where student_id is passed as a parameter to the function. 
# The entries are ordered by date.

def get_entries(student_id):

    connection = sqlite3.connect("siwes.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM logbook_entries
        WHERE student_id = ?
        ORDER BY date
    """, (student_id,))

    rows = cursor.fetchall()

    connection.close()

    entries = []
    
    for row in rows:
        
        entry = row_to_entry(row)
        
        entries.append(entry)
        
    return entries

# search_entries(student_id, keyword) function is defined to search for logbook entries 
# for a specific student that contain a given keyword in the activities, skills learned, 
# or challenges fields.
def search_entries(student_id, keyword):

    connection = sqlite3.connect("siwes.db")
    cursor = connection.cursor()

    search_pattern = f"%{keyword}%"

    cursor.execute("""
        SELECT *
        FROM logbook_entries
        WHERE student_id = ?
        AND (
            activities LIKE ?
            OR skills_learned LIKE ?
            OR challenges LIKE ?
        )
        ORDER BY date
    """, (
        student_id,
        search_pattern,
        search_pattern,
        search_pattern
    ))

    rows = cursor.fetchall()

    connection.close()

    entries = []
    
    for row in rows:
        
        entry = row_to_entry(row)
        
        entries.append(entry)
        
    return entries

# filter_entries(student_id, week_number=None, status=None, keyword=None) 
# function is defined to filter logbook entries for a specific student based on 
# optional criteria such as week number, status, and keyword.
def filter_entries(
    student_id,
    week_number=None,
    status=None,
    keyword=None
):

    connection = sqlite3.connect("siwes.db")
    cursor = connection.cursor()

    query = """
        SELECT *
        FROM logbook_entries
        WHERE student_id = ?
    """

    parameters = [student_id]

    if week_number is not None:
        query += " AND week_number = ?"
        parameters.append(week_number)

    if status is not None:
        query += " AND status = ?"
        parameters.append(status)

    if keyword:
        query += """
            AND (
                activities LIKE ?
                OR skills_learned LIKE ?
                OR challenges LIKE ?
            )
        """

        search_pattern = f"%{keyword}%"

        parameters.extend([
            search_pattern,
            search_pattern,
            search_pattern
        ])

    query += " ORDER BY date"

    cursor.execute(query, parameters)

    rows = cursor.fetchall()

    connection.close()

    entries = []

    entries = []
    
    for row in rows:
        
        entry = row_to_entry(row)
        
        entries.append(entry)
        
    return entries

# update_entry(entry_id, date, week_number, activities, skills_learned, challenges) function is defined to update an existing logbook entry in the database.
def update_entry(entry):

    connection = sqlite3.connect("siwes.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE logbook_entries

        SET
            date = ?,
            week_number = ?,
            activities = ?,
            skills_learned = ?,
            challenges = ?,
            supervisor_comment = ?,
            status = ?

        WHERE id = ?
    """, (
        entry.date,
        entry.week_number,
        entry.activities,
        entry.skills_learned,
        entry.challenges,
        entry.supervisor_comment,
        entry.status,
        entry.entry_id
    ))

    connection.commit()
    connection.close()

# delete_entry(entry_id) function is defined to delete a logbook entry from the database based on the provided entry_id.
def delete_entry(entry):

    connection = sqlite3.connect("siwes.db")
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM logbook_entries
        WHERE id = ?
    """, (entry.entry_id,))

    connection.commit()
    connection.close()

# update_entry_status(entry_id, status, supervisor_comment=None) function is 
# defined to update the status and supervisor comment of a logbook entry in the 
# database based on the provided entry_id.
def update_entry_status(entry_id, status, supervisor_comment=None):

    valid_statuses = ["Pending", "Approved", "Rejected"]

    if status not in valid_statuses:
        raise ValueError("Invalid status.")

    connection = sqlite3.connect("siwes.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE logbook_entries
        SET status = ?,
            supervisor_comment = ?
        WHERE id = ?
    """, (
        status,
        supervisor_comment,
        entry_id
    ))

    if cursor.rowcount == 0:
        connection.close()
        raise ValueError("Logbook entry not found.")

    connection.commit()
    connection.close()

    