"""
Analytics module for the SIWES Management System.

This module reads information from the SQLite database and
produces statistics for reports and dashboards.

Module: Reports & Analytics
Developer: Samuel Okpo
"""

import sqlite3
from pathlib import Path


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# SQLite database
DATABASE_PATH = PROJECT_ROOT / "SIWES.db"


class Analytics:
    """Handles statistical calculations for the SIWES system."""

    def __init__(self, database_path=DATABASE_PATH):
        self.database_path = database_path

    def connect(self):
        """Create a connection to the SQLite database."""
        return sqlite3.connect(self.database_path)

    def _table_exists(self, cursor, table_name):
        """Check whether a table exists in the database."""
        cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table' AND name=?
            """,
            (table_name,)
        )

        return cursor.fetchone() is not None

    def get_total_users(self):
        """Return the total number of registered users."""
        with self.connect() as connection:
            cursor = connection.cursor()

            if not self._table_exists(cursor, "users"):
                return 0

            cursor.execute("SELECT COUNT(*) FROM users")
            return cursor.fetchone()[0]

    def get_total_students(self):
        """
        Return the number of students.

        This currently uses the users table because the authentication
        module already contains a role column.
        """
        with self.connect() as connection:
            cursor = connection.cursor()

            if not self._table_exists(cursor, "users"):
                return 0

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM users
                WHERE LOWER(role) = 'student'
                """
            )

            return cursor.fetchone()[0]

    def get_total_supervisors(self):
        """Return the number of registered supervisors."""
        with self.connect() as connection:
            cursor = connection.cursor()

            if not self._table_exists(cursor, "users"):
                return 0

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM users
                WHERE LOWER(role) = 'supervisor'
                """
            )

            return cursor.fetchone()[0]

    def get_total_organizations(self):
        """Return the number of internship organizations."""
        with self.connect() as connection:
            cursor = connection.cursor()

            if not self._table_exists(cursor, "organizations"):
                return 0

            cursor.execute("SELECT COUNT(*) FROM organizations")

            return cursor.fetchone()[0]

    def get_total_placements(self):
        """Return the total number of SIWES placements."""
        with self.connect() as connection:
            cursor = connection.cursor()

            if not self._table_exists(cursor, "placements"):
                return 0

            cursor.execute("SELECT COUNT(*) FROM placements")

            return cursor.fetchone()[0]

    def get_placement_status_statistics(self):
        """
        Return placement counts grouped by status.

        Example:
        {
            "Pending": 5,
            "Approved": 10,
            "Active": 20,
            "Completed": 8
        }
        """
        with self.connect() as connection:
            cursor = connection.cursor()

            if not self._table_exists(cursor, "placements"):
                return {}

            cursor.execute(
                """
                SELECT status, COUNT(*)
                FROM placements
                GROUP BY status
                """
            )

            results = cursor.fetchall()

        return {
            str(status): count
            for status, count in results
        }

    def get_attendance_statistics(self):
        """
        Calculate attendance statistics.

        Expected attendance table fields:
        - status
        - student_id

        Accepted status examples:
        Present / Absent
        """
        with self.connect() as connection:
            cursor = connection.cursor()

            if not self._table_exists(cursor, "attendance"):
                return {
                    "present": 0,
                    "absent": 0,
                    "total": 0,
                    "percentage": 0
                }

            cursor.execute(
                """
                SELECT
                    SUM(
                        CASE
                            WHEN LOWER(status) = 'present'
                            THEN 1
                            ELSE 0
                        END
                    ),
                    SUM(
                        CASE
                            WHEN LOWER(status) = 'absent'
                            THEN 1
                            ELSE 0
                        END
                    ),
                    COUNT(*)
                FROM attendance
                """
            )

            present, absent, total = cursor.fetchone()

            present = present or 0
            absent = absent or 0
            total = total or 0

            percentage = (
                (present / total) * 100
                if total > 0
                else 0
            )

            return {
                "present": present,
                "absent": absent,
                "total": total,
                "percentage": round(percentage, 2)
            }

    def get_logbook_statistics(self):
        """Return general digital logbook statistics in a single query."""
        with self.connect() as connection:
            cursor = connection.cursor()

            if not self._table_exists(cursor, "logbook"):
                return {
                    "total_entries": 0,
                    "approved": 0,
                    "pending": 0
                }

            cursor.execute(
                """
                SELECT
                    COUNT(*),
                    SUM(CASE WHEN LOWER(approval_status) = 'approved' THEN 1 ELSE 0 END),
                    SUM(CASE WHEN LOWER(approval_status) = 'pending' THEN 1 ELSE 0 END)
                FROM logbook
                """
            )

            total, approved, pending = cursor.fetchone()

            return {
                "total_entries": total or 0,
                "approved": approved or 0,
                "pending": pending or 0
            }

    def get_summary(self):
        """
        Return a complete summary of available SIWES statistics.
        """
        attendance = self.get_attendance_statistics()
        logbook = self.get_logbook_statistics()

        return {
            "total_users": self.get_total_users(),
            "total_students": self.get_total_students(),
            "total_supervisors": self.get_total_supervisors(),
            "total_organizations": self.get_total_organizations(),
            "total_placements": self.get_total_placements(),
            "attendance": attendance,
            "logbook": logbook,
            "placement_status": self.get_placement_status_statistics()
        }


if __name__ == "__main__":
    analytics = Analytics()

    summary = analytics.get_summary()

    print("\nSIWES REPORT & ANALYTICS")
    print("-" * 30)

    print("Total Users:", summary["total_users"])
    print("Total Students:", summary["total_students"])
    print("Total Supervisors:", summary["total_supervisors"])
    print("Total Organizations:", summary["total_organizations"])
    print("Total Placements:", summary["total_placements"])

    print("\nAttendance")
    print("Present:", summary["attendance"]["present"])
    print("Absent:", summary["attendance"]["absent"])
    print("Attendance:", summary["attendance"]["percentage"], "%")

    print("\nLogbook")
    print("Total Entries:", summary["logbook"]["total_entries"])
    print("Approved:", summary["logbook"]["approved"])
    print("Pending:", summary["logbook"]["pending"])

    print("\nPlacement Status")
    for status, count in summary["placement_status"].items():
        print(f"{status}: {count}")