import customtkinter as ctk
import sqlite3

from database.database import get_connection
from ui.theme import (
    NAVY,
    BLUE,
    BLUE_HOVER,
    WHITE,
    BACKGROUND,
    CARD,
    TEXT,
    TEXT_LIGHT,
    BORDER,
    SUCCESS,
    ERROR,
)


class SupervisorsDashboard(ctk.CTkFrame):
    """
    Supervisor dashboard.

    Designed to work with auth.py using:
        SupervisorsDashboard(
            user=user_data,
            logout_callback=self.logout
        )
    """

    def __init__(self, user, logout_callback=None):

        # auth.py does not provide a master, so create a dashboard window.
        self.window = ctk.CTk()

        self.window.title("SIWES Management System - Supervisor Dashboard")
        self.window.geometry("1200x750")
        self.window.minsize(1000, 650)

        self.user = user or {}
        self.logout_callback = logout_callback

        # IMPORTANT:
        # Give CTkFrame the window as its master.
        super().__init__(
            master=self.window,
            fg_color=BACKGROUND
        )

        self.pack(fill="both", expand=True)

        self.supervisor_id = self._find_supervisor()

        self._build_ui()
        self.refresh_dashboard()

    # =========================================================
    # DATABASE
    # =========================================================

    def _find_supervisor(self):
        """Find supervisor profile using the logged-in user's email."""

        connection = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            email = self.user.get("email", "")

            cursor.execute(
                """
                SELECT id
                FROM supervisors
                WHERE LOWER(email) = LOWER(?)
                LIMIT 1
                """,
                (email,),
            )

            row = cursor.fetchone()

            return row[0] if row else None

        except Exception as error:
            print(f"Supervisor lookup error: {error}")
            return None

        finally:
            if connection:
                connection.close()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self):

        # ---------------- HEADER ----------------

        header = ctk.CTkFrame(
            self,
            fg_color=NAVY,
            corner_radius=0,
            height=78,
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        left = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )
        left.pack(
            side="left",
            padx=25,
            pady=12
        )

        ctk.CTkLabel(
            left,
            text="SIWES Management System",
            font=ctk.CTkFont(
                size=21,
                weight="bold"
            ),
            text_color=WHITE,
        ).pack(anchor="w")

        ctk.CTkLabel(
            left,
            text="Supervisor Dashboard",
            font=ctk.CTkFont(size=12),
            text_color="#D7E4F2",
        ).pack(anchor="w")

        right = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )
        right.pack(
            side="right",
            padx=20
        )

        full_name = self.user.get(
            "full_name",
            "Supervisor"
        )

        ctk.CTkLabel(
            right,
            text=f"👨‍🏫 {full_name}",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=WHITE,
        ).pack(
            side="left",
            padx=(0, 12)
        )

        ctk.CTkButton(
            right,
            text="Logout",
            width=90,
            height=36,
            fg_color=ERROR,
            hover_color="#B91C1C",
            command=self._logout,
        ).pack(side="left")

        # ---------------- CONTENT ----------------

        self.content = ctk.CTkScrollableFrame(
            self,
            fg_color=BACKGROUND
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=18
        )

        # ---------------- WELCOME ----------------

        ctk.CTkLabel(
            self.content,
            text=f"Welcome, {full_name} 👋",
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            ),
            text_color=TEXT,
        ).pack(anchor="w")

        ctk.CTkLabel(
            self.content,
            text=(
                "Monitor assigned students, review logbooks, "
                "check attendance and manage evaluations."
            ),
            font=ctk.CTkFont(size=13),
            text_color=TEXT_LIGHT,
        ).pack(
            anchor="w",
            pady=(4, 18)
        )

        # ---------------- STAT CARDS ----------------

        stats = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        stats.pack(
            fill="x",
            pady=(0, 18)
        )

        self.students_value = self._stat_card(
            stats,
            "👥",
            "Assigned Students"
        )

        self.logbook_value = self._stat_card(
            stats,
            "📖",
            "Logbook Entries"
        )

        self.attendance_value = self._stat_card(
            stats,
            "📅",
            "Attendance Records"
        )

        self.evaluation_value = self._stat_card(
            stats,
            "⭐",
            "Evaluations"
        )

        # ---------------- ACTIONS ----------------

        actions = ctk.CTkFrame(
            self.content,
            fg_color=CARD,
            corner_radius=10,
            border_width=1,
            border_color=BORDER
        )

        actions.pack(
            fill="x",
            pady=(0, 18)
        )

        ctk.CTkLabel(
            actions,
            text="Supervisor Actions",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            ),
            text_color=TEXT,
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 12)
        )

        buttons = ctk.CTkFrame(
            actions,
            fg_color="transparent"
        )

        buttons.pack(
            fill="x",
            padx=18,
            pady=(0, 18)
        )

        self._action_button(
            buttons,
            "👥 Assigned Students",
            self.show_students
        ).pack(
            side="left",
            padx=(0, 8)
        )

        self._action_button(
            buttons,
            "📖 Student Logbooks",
            self.show_logbooks
        ).pack(
            side="left",
            padx=8
        )

        self._action_button(
            buttons,
            "📅 Attendance",
            self.show_attendance
        ).pack(
            side="left",
            padx=8
        )

        self._action_button(
            buttons,
            "⭐ Evaluations",
            self.show_evaluations
        ).pack(
            side="left",
            padx=8
        )

        # ---------------- DATA CARD ----------------

        self.data_card = ctk.CTkFrame(
            self.content,
            fg_color=CARD,
            corner_radius=10,
            border_width=1,
            border_color=BORDER
        )

        self.data_card.pack(
            fill="both",
            expand=True
        )

        self.data_title = ctk.CTkLabel(
            self.data_card,
            text="Assigned Students",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color=TEXT,
        )

        self.data_title.pack(
            anchor="w",
            padx=18,
            pady=(18, 10)
        )

        self.output = ctk.CTkTextbox(
            self.data_card,
            height=330,
            fg_color=BACKGROUND,
            text_color=TEXT,
            border_width=1,
            border_color=BORDER,
            corner_radius=8,
            font=ctk.CTkFont(size=12)
        )

        self.output.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=(0, 18)
        )

        self.output.configure(
            state="disabled"
        )

    # =========================================================
    # COMPONENTS
    # =========================================================

    def _stat_card(self, parent, icon, title):

        card = ctk.CTkFrame(
            parent,
            fg_color=CARD,
            corner_radius=10,
            border_width=1,
            border_color=BORDER
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=24)
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 2)
        )

        value = ctk.CTkLabel(
            card,
            text="0",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            ),
            text_color=NAVY
        )

        value.pack(
            anchor="w",
            padx=15
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=11),
            text_color=TEXT_LIGHT
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 12)
        )

        return value

    def _action_button(self, parent, text, command):

        return ctk.CTkButton(
            parent,
            text=text,
            height=42,
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
            corner_radius=8,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            command=command
        )

    def _set_output(self, text):

        self.output.configure(
            state="normal"
        )

        self.output.delete(
            "1.0",
            "end"
        )

        self.output.insert(
            "1.0",
            text
        )

        self.output.configure(
            state="disabled"
        )

    # =========================================================
    # STATISTICS
    # =========================================================

    def refresh_dashboard(self):

        connection = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            if not self.supervisor_id:

                self.students_value.configure(text="0")
                self.logbook_value.configure(text="0")
                self.attendance_value.configure(text="0")
                self.evaluation_value.configure(text="0")

                self._set_output(
                    "Your supervisor profile has not been linked yet.\n\n"
                    "Please ask an administrator to link your supervisor "
                    "account to a supervisor profile."
                )

                return

            # Students

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM placements
                WHERE supervisor_id = ?
                """,
                (self.supervisor_id,)
            )

            students = cursor.fetchone()[0]

            # Logbooks

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM logbook_entries le
                INNER JOIN placements p
                    ON p.student_id = le.student_id
                WHERE p.supervisor_id = ?
                """,
                (self.supervisor_id,)
            )

            logbooks = cursor.fetchone()[0]

            # Attendance

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM attendance a
                INNER JOIN placements p
                    ON p.student_id = a.student_id
                WHERE p.supervisor_id = ?
                """,
                (self.supervisor_id,)
            )

            attendance = cursor.fetchone()[0]

            # Evaluations

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM evaluations
                WHERE supervisor_id = ?
                """,
                (self.supervisor_id,)
            )

            evaluations = cursor.fetchone()[0]

            self.students_value.configure(
                text=str(students)
            )

            self.logbook_value.configure(
                text=str(logbooks)
            )

            self.attendance_value.configure(
                text=str(attendance)
            )

            self.evaluation_value.configure(
                text=str(evaluations)
            )

            self.show_students()

        except Exception as error:

            print(
                f"Supervisor dashboard error: {error}"
            )

            self._set_output(
                f"Unable to load dashboard data.\n\n"
                f"Error: {error}"
            )

        finally:

            if connection:
                connection.close()

    # =========================================================
    # STUDENTS
    # =========================================================

    def show_students(self):

        self.data_title.configure(
            text="👥 Assigned Students"
        )

        connection = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            if not self.supervisor_id:

                self._set_output(
                    "No supervisor profile is linked to this account."
                )

                return

            cursor.execute(
                """
                SELECT
                    s.full_name,
                    s.email,
                    s.phone,
                    s.department,
                    s.level,
                    o.organization_name,
                    p.start_date,
                    p.end_date,
                    p.status
                FROM placements p

                INNER JOIN students s
                    ON s.id = p.student_id

                LEFT JOIN organizations o
                    ON o.id = p.organization_id

                WHERE p.supervisor_id = ?

                ORDER BY s.full_name
                """,
                (self.supervisor_id,)
            )

            rows = cursor.fetchall()

            if not rows:

                self._set_output(
                    "No students are currently assigned to you.\n\n"
                    "Students assigned through Placement Management "
                    "will appear here."
                )

                return

            output = []

            for number, row in enumerate(
                rows,
                start=1
            ):

                (
                    name,
                    email,
                    phone,
                    department,
                    level,
                    organization,
                    start_date,
                    end_date,
                    status
                ) = row

                output.append(
                    f"{number}. {name}\n"
                    f"   Email: {email or 'N/A'}\n"
                    f"   Phone: {phone or 'N/A'}\n"
                    f"   Department: {department or 'N/A'}\n"
                    f"   Level: {level or 'N/A'}\n"
                    f"   Organization: {organization or 'N/A'}\n"
                    f"   Placement: "
                    f"{start_date or 'N/A'} → "
                    f"{end_date or 'N/A'}\n"
                    f"   Status: {status or 'N/A'}\n"
                    + "-" * 80
                )

            self._set_output(
                "\n\n".join(output)
            )

        except Exception as error:

            self._set_output(
                f"Unable to load students.\n\n"
                f"Error: {error}"
            )

        finally:

            if connection:
                connection.close()

    # =========================================================
    # LOGBOOKS
    # =========================================================

    def show_logbooks(self):

        self.data_title.configure(
            text="📖 Student Logbooks"
        )

        connection = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            if not self.supervisor_id:

                self._set_output(
                    "Supervisor profile not found."
                )

                return

            cursor.execute(
                """
                SELECT
                    s.full_name,
                    le.date,
                    le.week_number,
                    le.activities,
                    le.skills_learned,
                    le.status
                FROM logbook_entries le

                INNER JOIN students s
                    ON s.id = le.student_id

                INNER JOIN placements p
                    ON p.student_id = le.student_id

                WHERE p.supervisor_id = ?

                ORDER BY le.date DESC
                """,
                (self.supervisor_id,)
            )

            rows = cursor.fetchall()

            if not rows:

                self._set_output(
                    "No student logbook entries found."
                )

                return

            output = []

            for row in rows:

                (
                    student,
                    date,
                    week,
                    activities,
                    skills,
                    status
                ) = row

                output.append(
                    f"Student: {student}\n"
                    f"Date: {date}\n"
                    f"Week: {week}\n"
                    f"Activities: {activities or 'N/A'}\n"
                    f"Skills Learned: {skills or 'N/A'}\n"
                    f"Status: {status or 'Pending'}\n"
                    + "-" * 80
                )

            self._set_output(
                "\n\n".join(output)
            )

        except Exception as error:

            self._set_output(
                f"Unable to load logbooks.\n\n"
                f"Error: {error}"
            )

        finally:

            if connection:
                connection.close()

    # =========================================================
    # ATTENDANCE
    # =========================================================

    def show_attendance(self):

        self.data_title.configure(
            text="📅 Student Attendance"
        )

        connection = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            if not self.supervisor_id:

                self._set_output(
                    "Supervisor profile not found."
                )

                return

            cursor.execute(
                """
                SELECT
                    s.full_name,
                    a.attendance_date,
                    a.status,
                    a.remarks
                FROM attendance a

                INNER JOIN students s
                    ON s.id = a.student_id

                INNER JOIN placements p
                    ON p.student_id = a.student_id

                WHERE p.supervisor_id = ?

                ORDER BY a.attendance_date DESC
                """,
                (self.supervisor_id,)
            )

            rows = cursor.fetchall()

            if not rows:

                self._set_output(
                    "No attendance records found."
                )

                return

            output = []

            for row in rows:

                student, date, status, remarks = row

                output.append(
                    f"Student: {student}\n"
                    f"Date: {date}\n"
                    f"Status: {status}\n"
                    f"Remarks: {remarks or 'N/A'}\n"
                    + "-" * 80
                )

            self._set_output(
                "\n\n".join(output)
            )

        except Exception as error:

            self._set_output(
                f"Unable to load attendance.\n\n"
                f"Error: {error}"
            )

        finally:

            if connection:
                connection.close()

    # =========================================================
    # EVALUATIONS
    # =========================================================

    def show_evaluations(self):

        self.data_title.configure(
            text="⭐ Student Evaluations"
        )

        connection = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            if not self.supervisor_id:

                self._set_output(
                    "Supervisor profile not found."
                )

                return

            cursor.execute(
                """
                SELECT
                    s.full_name,
                    e.technical_skills,
                    e.punctuality,
                    e.teamwork,
                    e.communication,
                    e.professionalism,
                    e.comments,
                    e.evaluation_date
                FROM evaluations e

                INNER JOIN students s
                    ON s.id = e.student_id

                WHERE e.supervisor_id = ?

                ORDER BY e.evaluation_date DESC
                """,
                (self.supervisor_id,)
            )

            rows = cursor.fetchall()

            if not rows:

                self._set_output(
                    "No evaluations have been recorded yet."
                )

                return

            output = []

            for row in rows:

                (
                    student,
                    technical,
                    punctuality,
                    teamwork,
                    communication,
                    professionalism,
                    comments,
                    date
                ) = row

                output.append(
                    f"Student: {student}\n"
                    f"Technical Skills: {technical}/10\n"
                    f"Punctuality: {punctuality}/10\n"
                    f"Teamwork: {teamwork}/10\n"
                    f"Communication: {communication}/10\n"
                    f"Professionalism: {professionalism}/10\n"
                    f"Comments: {comments or 'N/A'}\n"
                    f"Evaluation Date: {date or 'N/A'}\n"
                    + "-" * 80
                )

            self._set_output(
                "\n\n".join(output)
            )

        except Exception as error:

            self._set_output(
                f"Unable to load evaluations.\n\n"
                f"Error: {error}"
            )

        finally:

            if connection:
                connection.close()

    # =========================================================
    # LOGOUT
    # =========================================================

    def _logout(self):

        try:
            self.window.destroy()
        except Exception:
            pass

        if self.logout_callback:
            self.logout_callback()


# =============================================================
# DIRECT TEST
# =============================================================

if __name__ == "__main__":

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    test_user = {
        "id": 1,
        "username": "supervisor1",
        "full_name": "Supervisor",
        "email": "supervisor@siwes.com",
        "role": "supervisor",
    }

    dashboard = SupervisorsDashboard(
        user=test_user
    )

    dashboard.window.mainloop()