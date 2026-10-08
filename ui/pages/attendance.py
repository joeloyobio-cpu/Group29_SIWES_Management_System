import csv
import datetime as dt
from tkinter import messagebox, filedialog

import customtkinter as ctk

from database.database import get_connection

from ui.theme import (
    NAVY,
    BLUE,
    BLUE_HOVER,
    WHITE,
    BACKGROUND,
    INPUT_BG,
    TEXT,
    TEXT_LIGHT,
    BORDER,
    SUCCESS,
    ERROR,
    WARNING
)


# ============================================================
# CONSTANTS
# ============================================================

DATE_FMT = "%Y-%m-%d"

PRESENT = "Present"
ABSENT = "Absent"

MIN_PERCENT = 75.0


# ============================================================
# ATTENDANCE PAGE
# ============================================================

class AttendancePage(ctk.CTkFrame):

    def __init__(self, parent, user_data):

        super().__init__(
            parent,
            fg_color=BACKGROUND
        )

        self.user_data = user_data

        self.students = []
        self.pending = {}

        self.report_headers = []
        self.report_rows = []

        self.ensure_attendance_table()
        self.load_students()
        self.build_page()

    # ========================================================
    # DATABASE SETUP
    # ========================================================

    def ensure_attendance_table(self):

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    attendance_date TEXT NOT NULL,
                    status TEXT NOT NULL,
                    remarks TEXT,
                    UNIQUE(student_id, attendance_date),
                    FOREIGN KEY(student_id)
                        REFERENCES students(id)
                        ON DELETE CASCADE
                )
                """
            )

            conn.commit()
            conn.close()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to prepare attendance table.\n\n{e}"
            )

    # ========================================================
    # DATE HELPERS
    # ========================================================

    def today(self):

        return dt.date.today().strftime(
            DATE_FMT
        )

    def valid_date(self, value):

        try:

            dt.datetime.strptime(
                value.strip(),
                DATE_FMT
            )

            return True

        except ValueError:

            return False

    def get_date_value(self, entry):

        value = entry.get().strip()

        if not value:

            return None

        if not self.valid_date(value):

            raise ValueError(
                f"'{value}' is not a valid date. "
                "Use YYYY-MM-DD."
            )

        return value

    # ========================================================
    # STUDENTS
    # ========================================================

    def load_students(self):

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    full_name,
                    email,
                    student_id_number
                FROM students
                ORDER BY full_name
                """
            )

            self.students = cursor.fetchall()

            conn.close()

        except Exception as e:

            self.students = []

            messagebox.showerror(
                "Database Error",
                f"Unable to load students.\n\n{e}"
            )

    def student_choices(self):

        choices = [
            "All students"
        ]

        for student in self.students:

            student_number = (
                student[3]
                if student[3]
                else "N/A"
            )

            choices.append(
                f"{student_number} - {student[1]}"
            )

        return choices

    def student_id_from_choice(self, choice):

        if (
            not choice
            or choice == "All students"
        ):

            return None

        for student in self.students:

            student_number = (
                student[3]
                if student[3]
                else "N/A"
            )

            label = (
                f"{student_number} - "
                f"{student[1]}"
            )

            if label == choice:

                return student[0]

        return None

    # ========================================================
    # MAIN PAGE
    # ========================================================

    def build_page(self):

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=40,
            pady=(30, 15)
        )

        ctk.CTkLabel(
            header,
            text="Attendance",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            ),
            text_color=TEXT
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            header,
            text=(
                "Record, monitor and manage "
                "SIWES attendance."
            ),
            font=ctk.CTkFont(
                size=14
            ),
            text_color=TEXT_LIGHT
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        self.create_statistics()
        self.create_tabs()

    # ========================================================
    # STATISTICS
    # ========================================================

    def create_statistics(self):

        container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        container.pack(
            fill="x",
            padx=40,
            pady=(0, 20)
        )

        for column in range(4):

            container.grid_columnconfigure(
                column,
                weight=1
            )

        self.total_card = self.create_stat_card(
            container,
            0,
            "Students",
            str(len(self.students)),
            BLUE
        )

        self.present_card = self.create_stat_card(
            container,
            1,
            "Present Today",
            "0",
            SUCCESS
        )

        self.absent_card = self.create_stat_card(
            container,
            2,
            "Absent Today",
            "0",
            ERROR
        )

        self.average_card = self.create_stat_card(
            container,
            3,
            "Average Attendance",
            "0%",
            WARNING
        )

        self.refresh_statistics()

    def create_stat_card(
        self,
        parent,
        column,
        title,
        value,
        value_color
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color=WHITE,
            corner_radius=12,
            border_width=1,
            border_color=BORDER
        )

        card.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=5
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=TEXT_LIGHT
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 2)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            ),
            text_color=value_color
        )

        value_label.pack(
            anchor="w",
            padx=18,
            pady=(0, 15)
        )

        return value_label

    def refresh_statistics(self):

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    SUM(
                        CASE
                            WHEN status = 'Present'
                            THEN 1
                            ELSE 0
                        END
                    ),
                    SUM(
                        CASE
                            WHEN status = 'Absent'
                            THEN 1
                            ELSE 0
                        END
                    )
                FROM attendance
                WHERE attendance_date = ?
                """,
                (self.today(),)
            )

            row = cursor.fetchone()

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM attendance
                """
            )

            total_records = (
                cursor.fetchone()[0]
                or 0
            )

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM attendance
                WHERE status = 'Present'
                """
            )

            total_present = (
                cursor.fetchone()[0]
                or 0
            )

            conn.close()

            present = row[0] or 0
            absent = row[1] or 0

            average = (
                total_present
                / total_records
                * 100
                if total_records
                else 0
            )

            self.total_card.configure(
                text=str(len(self.students))
            )

            self.present_card.configure(
                text=str(present)
            )

            self.absent_card.configure(
                text=str(absent)
            )

            self.average_card.configure(
                text=f"{average:.1f}%"
            )

        except Exception:

            pass

    # ========================================================
    # TABS
    # ========================================================

    def create_tabs(self):

        self.tabview = ctk.CTkTabview(
            self,
            fg_color=BACKGROUND,
            segmented_button_fg_color=WHITE,
            segmented_button_selected_color=BLUE,
            segmented_button_selected_hover_color=BLUE_HOVER,
            segmented_button_unselected_color=WHITE,
            segmented_button_unselected_hover_color=INPUT_BG
        )

        self.tabview.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=(0, 30)
        )

        self.record_tab = self.tabview.add(
            "Record Attendance"
        )

        self.history_tab = self.tabview.add(
            "Attendance History"
        )

        self.percentage_tab = self.tabview.add(
            "Attendance Percentage"
        )

        self.reports_tab = self.tabview.add(
            "Reports"
        )

        self.build_record_tab()
        self.build_history_tab()
        self.build_percentage_tab()
        self.build_reports_tab()

    # ========================================================
    # RECORD ATTENDANCE
    # ========================================================

    def build_record_tab(self):

        top = ctk.CTkFrame(
            self.record_tab,
            fg_color=WHITE,
            corner_radius=10,
            border_width=1,
            border_color=BORDER
        )

        top.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            top,
            text="Date",
            text_color=TEXT,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        ).pack(
            side="left",
            padx=(15, 5),
            pady=12
        )

        self.record_date = ctk.CTkEntry(
            top,
            width=130,
            height=38,
            fg_color=INPUT_BG,
            border_color=BORDER
        )

        self.record_date.pack(
            side="left"
        )

        self.record_date.insert(
            0,
            self.today()
        )

        ctk.CTkButton(
            top,
            text="Today",
            width=80,
            height=38,
            fg_color=INPUT_BG,
            hover_color="#E2E8F0",
            text_color=TEXT,
            command=self.set_today
        ).pack(
            side="left",
            padx=8
        )

        ctk.CTkButton(
            top,
            text="Load Day",
            width=100,
            height=38,
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
            text_color=WHITE,
            command=self.load_day
        ).pack(
            side="left"
        )

        table = ctk.CTkFrame(
            self.record_tab,
            fg_color=WHITE,
            corner_radius=10,
            border_width=1,
            border_color=BORDER
        )

        table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        header = ctk.CTkFrame(
            table,
            fg_color=INPUT_BG,
            corner_radius=6
        )

        header.pack(
            fill="x",
            padx=15,
            pady=(15, 5)
        )

        ctk.CTkLabel(
            header,
            text="Student",
            text_color=TEXT,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        ).pack(
            side="left",
            padx=15,
            pady=10
        )

        ctk.CTkLabel(
            header,
            text="Status",
            text_color=TEXT,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        ).pack(
            side="right",
            padx=40,
            pady=10
        )

        self.record_scroll = ctk.CTkScrollableFrame(
            table,
            fg_color=INPUT_BG
        )

        self.record_scroll.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        self.record_rows = {}

        bottom = ctk.CTkFrame(
            table,
            fg_color="transparent"
        )

        bottom.pack(
            fill="x",
            padx=15,
            pady=(5, 15)
        )

        ctk.CTkButton(
            bottom,
            text="All Present",
            width=110,
            height=38,
            fg_color=SUCCESS,
            hover_color="#15803D",
            command=lambda:
                self.mark_all(PRESENT)
        ).pack(
            side="left",
            padx=(0, 8)
        )

        ctk.CTkButton(
            bottom,
            text="All Absent",
            width=110,
            height=38,
            fg_color=ERROR,
            hover_color="#B91C1C",
            command=lambda:
                self.mark_all(ABSENT)
        ).pack(
            side="left"
        )

        self.record_info = ctk.CTkLabel(
            bottom,
            text="",
            text_color=TEXT_LIGHT
        )

        self.record_info.pack(
            side="left",
            padx=20
        )

        ctk.CTkButton(
            bottom,
            text="Save Attendance",
            width=150,
            height=40,
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
            text_color=WHITE,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            command=self.save_day
        ).pack(
            side="right"
        )

        self.load_day()

    # ========================================================
    # LOAD DAY
    # ========================================================

    def set_today(self):

        self.record_date.delete(
            0,
            "end"
        )

        self.record_date.insert(
            0,
            self.today()
        )

        self.load_day()

    def load_day(self):

        date = self.record_date.get().strip()

        if not self.valid_date(date):

            messagebox.showerror(
                "Invalid Date",
                "Use YYYY-MM-DD."
            )

            return

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    student_id,
                    status
                FROM attendance
                WHERE attendance_date = ?
                """,
                (date,)
            )

            saved = {
                row[0]: row[1]
                for row in cursor.fetchall()
            }

            conn.close()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

            return

        self.pending = {}

        for widget in self.record_scroll.winfo_children():

            widget.destroy()

        self.record_rows = {}

        if not self.students:

            ctk.CTkLabel(
                self.record_scroll,
                text=(
                    "No students found.\n\n"
                    "Create student records first "
                    "from Student Information."
                ),
                font=ctk.CTkFont(
                    size=15
                ),
                text_color=TEXT_LIGHT
            ).pack(
                pady=80
            )

            return

        for student in self.students:

            student_id = student[0]

            status = saved.get(
                student_id,
                PRESENT
            )

            self.pending[
                student_id
            ] = status

            self.create_record_row(
                student,
                status
            )

        note = (
            "Already recorded"
            if saved
            else "New attendance"
        )

        self.record_info.configure(
            text=f"{date} • {note}"
        )

    # ========================================================
    # RECORD ROW
    # ========================================================

    def create_record_row(
        self,
        student,
        status
    ):

        student_id = student[0]
        name = student[1]
        student_number = (
            student[3]
            if student[3]
            else "N/A"
        )

        row = ctk.CTkFrame(
            self.record_scroll,
            fg_color=WHITE,
            corner_radius=8
        )

        row.pack(
            fill="x",
            pady=4
        )

        info = ctk.CTkFrame(
            row,
            fg_color="transparent"
        )

        info.pack(
            side="left",
            fill="x",
            expand=True,
            padx=15,
            pady=10
        )

        ctk.CTkLabel(
            info,
            text=name,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=TEXT
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            info,
            text=student_number,
            text_color=TEXT_LIGHT
        ).pack(
            anchor="w"
        )

        variable = ctk.StringVar(
            value=status
        )

        menu = ctk.CTkOptionMenu(
            row,
            values=[
                PRESENT,
                ABSENT
            ],
            variable=variable,
            width=120,
            height=36,
            command=lambda value,
            sid=student_id:
                self.change_status(
                    sid,
                    value
                )
        )

        menu.pack(
            side="right",
            padx=15,
            pady=8
        )

        self.record_rows[
            student_id
        ] = {
            "variable": variable,
            "menu": menu
        }

        self.style_status_menu(
            menu,
            status
        )

    def style_status_menu(
        self,
        menu,
        status
    ):

        if status == PRESENT:

            menu.configure(
                fg_color=SUCCESS,
                button_color=SUCCESS,
                button_hover_color="#15803D"
            )

        else:

            menu.configure(
                fg_color=ERROR,
                button_color=ERROR,
                button_hover_color="#B91C1C"
            )

    # ========================================================
    # CHANGE STATUS
    # ========================================================

    def change_status(
        self,
        student_id,
        status
    ):

        self.pending[
            student_id
        ] = status

        if student_id in self.record_rows:

            menu = self.record_rows[
                student_id
            ]["menu"]

            self.style_status_menu(
                menu,
                status
            )

    # ========================================================
    # MARK ALL
    # ========================================================

    def mark_all(
        self,
        status
    ):

        for student_id in self.pending:

            self.pending[
                student_id
            ] = status

            if student_id in self.record_rows:

                data = self.record_rows[
                    student_id
                ]

                data["variable"].set(
                    status
                )

                self.style_status_menu(
                    data["menu"],
                    status
                )

    # ========================================================
    # SAVE
    # ========================================================

    def save_day(self):

        date = self.record_date.get().strip()

        if not self.valid_date(date):

            messagebox.showerror(
                "Invalid Date",
                "Use YYYY-MM-DD."
            )

            return

        if not self.pending:

            messagebox.showinfo(
                "Nothing to Save",
                "There are no students to record."
            )

            return

        try:

            conn = get_connection()
            cursor = conn.cursor()

            for student_id, status in self.pending.items():

                cursor.execute(
                    """
                    INSERT INTO attendance
                    (
                        student_id,
                        attendance_date,
                        status
                    )
                    VALUES (?, ?, ?)
                    ON CONFLICT(student_id, attendance_date)
                    DO UPDATE SET
                        status = excluded.status
                    """,
                    (
                        student_id,
                        date,
                        status
                    )
                )

            conn.commit()
            conn.close()

            present = sum(
                1
                for status in self.pending.values()
                if status == PRESENT
            )

            absent = (
                len(self.pending)
                - present
            )

            messagebox.showinfo(
                "Attendance Saved",
                (
                    f"Attendance for {date} saved.\n\n"
                    f"Present: {present}\n"
                    f"Absent: {absent}"
                )
            )

            self.refresh_statistics()

        except Exception as e:

            messagebox.showerror(
                "Save Error",
                str(e)
            )

    # ========================================================
    # HISTORY
    # ========================================================

    def build_history_tab(self):

        filters = ctk.CTkFrame(
            self.history_tab,
            fg_color=WHITE,
            corner_radius=10,
            border_width=1,
            border_color=BORDER
        )

        filters.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            filters,
            text="Student",
            text_color=TEXT
        ).pack(
            side="left",
            padx=(15, 5),
            pady=12
        )

        self.history_student = ctk.CTkComboBox(
            filters,
            values=self.student_choices(),
            width=220
        )

        self.history_student.pack(
            side="left"
        )

        self.history_student.set(
            "All students"
        )

        ctk.CTkLabel(
            filters,
            text="From",
            text_color=TEXT
        ).pack(
            side="left",
            padx=(15, 5)
        )

        self.history_from = ctk.CTkEntry(
            filters,
            width=120,
            placeholder_text="YYYY-MM-DD"
        )

        self.history_from.pack(
            side="left"
        )

        ctk.CTkLabel(
            filters,
            text="To",
            text_color=TEXT
        ).pack(
            side="left",
            padx=5
        )

        self.history_to = ctk.CTkEntry(
            filters,
            width=120,
            placeholder_text="YYYY-MM-DD"
        )

        self.history_to.pack(
            side="left"
        )

        self.history_status = ctk.CTkComboBox(
            filters,
            values=[
                "Any",
                PRESENT,
                ABSENT
            ],
            width=110
        )

        self.history_status.pack(
            side="left",
            padx=10
        )

        self.history_status.set(
            "Any"
        )

        ctk.CTkButton(
            filters,
            text="Search",
            width=90,
            height=38,
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
            command=self.load_history
        ).pack(
            side="left"
        )

        self.history_scroll = ctk.CTkScrollableFrame(
            self.history_tab,
            fg_color=INPUT_BG
        )

        self.history_scroll.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        self.history_count = ctk.CTkLabel(
            self.history_tab,
            text="0 records",
            text_color=TEXT_LIGHT
        )

        self.history_count.pack(
            anchor="e",
            padx=15,
            pady=(0, 8)
        )

    def load_history(self):

        try:

            start = self.get_date_value(
                self.history_from
            )

            end = self.get_date_value(
                self.history_to
            )

        except ValueError as e:

            messagebox.showerror(
                "Invalid Date",
                str(e)
            )

            return

        student_id = self.student_id_from_choice(
            self.history_student.get()
        )

        status = self.history_status.get()

        try:

            conn = get_connection()
            cursor = conn.cursor()

            query = """
                SELECT
                    a.id,
                    a.attendance_date,
                    s.full_name,
                    s.student_id_number,
                    a.status,
                    a.remarks
                FROM attendance a
                JOIN students s
                    ON s.id = a.student_id
                WHERE 1 = 1
            """

            params = []

            if student_id:

                query += """
                    AND a.student_id = ?
                """

                params.append(
                    student_id
                )

            if start:

                query += """
                    AND a.attendance_date >= ?
                """

                params.append(
                    start
                )

            if end:

                query += """
                    AND a.attendance_date <= ?
                """

                params.append(
                    end
                )

            if status != "Any":

                query += """
                    AND a.status = ?
                """

                params.append(
                    status
                )

            query += """
                ORDER BY
                    a.attendance_date DESC,
                    s.full_name
            """

            cursor.execute(
                query,
                params
            )

            rows = cursor.fetchall()

            conn.close()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

            return

        for widget in self.history_scroll.winfo_children():

            widget.destroy()

        if not rows:

            ctk.CTkLabel(
                self.history_scroll,
                text="No attendance records found.",
                font=ctk.CTkFont(
                    size=15
                ),
                text_color=TEXT_LIGHT
            ).pack(
                pady=80
            )

        else:

            for row in rows:

                self.create_history_row(
                    row
                )

        self.history_count.configure(
            text=f"{len(rows)} record(s)"
        )

    def create_history_row(
        self,
        row
    ):

        record_id = row[0]
        date = row[1]
        name = row[2]
        student_number = row[3] or "N/A"
        status = row[4]

        card = ctk.CTkFrame(
            self.history_scroll,
            fg_color=WHITE,
            corner_radius=8
        )

        card.pack(
            fill="x",
            pady=4
        )

        info = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        info.pack(
            side="left",
            fill="x",
            expand=True,
            padx=15,
            pady=10
        )

        ctk.CTkLabel(
            info,
            text=name,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=TEXT
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            info,
            text=f"{student_number}  •  {date}",
            text_color=TEXT_LIGHT
        ).pack(
            anchor="w"
        )

        ctk.CTkButton(
            card,
            text="Toggle",
            width=80,
            height=32,
            fg_color=(
                SUCCESS
                if status == ABSENT
                else ERROR
            ),
            hover_color=(
                "#15803D"
                if status == ABSENT
                else "#B91C1C"
            ),
            text_color=WHITE,
            command=lambda:
                self.toggle_history(
                    record_id,
                    status
                )
        ).pack(
            side="right",
            padx=10
        )

        ctk.CTkLabel(
            card,
            text=status,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=(
                SUCCESS
                if status == PRESENT
                else ERROR
            )
        ).pack(
            side="right",
            padx=15
        )

    def toggle_history(
        self,
        record_id,
        current_status
    ):

        new_status = (
            ABSENT
            if current_status == PRESENT
            else PRESENT
        )

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE attendance
                SET status = ?
                WHERE id = ?
                """,
                (
                    new_status,
                    record_id
                )
            )

            conn.commit()
            conn.close()

            self.load_history()
            self.refresh_statistics()

        except Exception as e:

            messagebox.showerror(
                "Update Error",
                str(e)
            )

    # ========================================================
    # PERCENTAGE
    # ========================================================

    def build_percentage_tab(self):

        top = ctk.CTkFrame(
            self.percentage_tab,
            fg_color=WHITE,
            corner_radius=10,
            border_width=1,
            border_color=BORDER
        )

        top.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            top,
            text="From",
            text_color=TEXT
        ).pack(
            side="left",
            padx=(15, 5),
            pady=12
        )

        self.percent_from = ctk.CTkEntry(
            top,
            width=120,
            placeholder_text="YYYY-MM-DD"
        )

        self.percent_from.pack(
            side="left"
        )

        ctk.CTkLabel(
            top,
            text="To",
            text_color=TEXT
        ).pack(
            side="left",
            padx=5
        )

        self.percent_to = ctk.CTkEntry(
            top,
            width=120,
            placeholder_text="YYYY-MM-DD"
        )

        self.percent_to.pack(
            side="left"
        )

        ctk.CTkButton(
            top,
            text="Calculate",
            width=100,
            height=38,
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
            command=self.load_percentages
        ).pack(
            side="left",
            padx=10
        )

        ctk.CTkLabel(
            top,
            text="Below 75% = Low Attendance",
            text_color=ERROR
        ).pack(
            side="right",
            padx=15
        )

        self.percent_scroll = ctk.CTkScrollableFrame(
            self.percentage_tab,
            fg_color=INPUT_BG
        )

        self.percent_scroll.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

    def load_percentages(self):

        try:

            start = self.get_date_value(
                self.percent_from
            )

            end = self.get_date_value(
                self.percent_to
            )

        except ValueError as e:

            messagebox.showerror(
                "Invalid Date",
                str(e)
            )

            return

        try:

            conn = get_connection()
            cursor = conn.cursor()

            query = """
                SELECT
                    s.id,
                    s.full_name,
                    s.student_id_number,
                    COUNT(a.id),
                    SUM(
                        CASE
                            WHEN a.status = 'Present'
                            THEN 1
                            ELSE 0
                        END
                    ),
                    SUM(
                        CASE
                            WHEN a.status = 'Absent'
                            THEN 1
                            ELSE 0
                        END
                    )
                FROM students s
                LEFT JOIN attendance a
                    ON a.student_id = s.id
            """

            conditions = []
            params = []

            if start:

                conditions.append(
                    "a.attendance_date >= ?"
                )

                params.append(
                    start
                )

            if end:

                conditions.append(
                    "a.attendance_date <= ?"
                )

                params.append(
                    end
                )

            if conditions:

                query += (
                    " WHERE "
                    + " AND ".join(
                        conditions
                    )
                )

            query += """
                GROUP BY s.id
                ORDER BY s.full_name
            """

            cursor.execute(
                query,
                params
            )

            rows = cursor.fetchall()

            conn.close()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

            return

        for widget in self.percent_scroll.winfo_children():

            widget.destroy()

        for row in rows:

            total = row[3] or 0
            present = row[4] or 0
            absent = row[5] or 0

            percentage = (
                present
                / total
                * 100
                if total
                else 0
            )

            self.create_percentage_row(
                row,
                total,
                present,
                absent,
                percentage
            )

    def create_percentage_row(
        self,
        row,
        total,
        present,
        absent,
        percentage
    ):

        card = ctk.CTkFrame(
            self.percent_scroll,
            fg_color=WHITE,
            corner_radius=8
        )

        card.pack(
            fill="x",
            pady=4
        )

        info = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        info.pack(
            side="left",
            fill="x",
            expand=True,
            padx=15,
            pady=10
        )

        ctk.CTkLabel(
            info,
            text=row[1],
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=TEXT
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            info,
            text=row[2] or "N/A",
            text_color=TEXT_LIGHT
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            card,
            text=(
                f"{total} days • "
                f"{present} present • "
                f"{absent} absent"
            ),
            text_color=TEXT_LIGHT
        ).pack(
            side="right",
            padx=20
        )

        ctk.CTkLabel(
            card,
            text=f"{percentage:.1f}%",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            ),
            text_color=(
                SUCCESS
                if percentage >= MIN_PERCENT
                else ERROR
            )
        ).pack(
            side="right",
            padx=20
        )

    # ========================================================
    # REPORTS
    # ========================================================

    def build_reports_tab(self):

        top = ctk.CTkFrame(
            self.reports_tab,
            fg_color=WHITE,
            corner_radius=10,
            border_width=1,
            border_color=BORDER
        )

        top.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.report_type = ctk.CTkComboBox(
            top,
            values=[
                "Summary Report",
                "Student Report",
                "Daily Report"
            ],
            width=170
        )

        self.report_type.pack(
            side="left",
            padx=(15, 5),
            pady=12
        )

        self.report_type.set(
            "Summary Report"
        )

        self.report_student = ctk.CTkComboBox(
            top,
            values=self.student_choices(),
            width=230
        )

        self.report_student.pack(
            side="left",
            padx=5
        )

        self.report_student.set(
            "All students"
        )

        self.report_from = ctk.CTkEntry(
            top,
            width=120,
            placeholder_text="Date / From"
        )

        self.report_from.pack(
            side="left",
            padx=5
        )

        self.report_to = ctk.CTkEntry(
            top,
            width=120,
            placeholder_text="To"
        )

        self.report_to.pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            top,
            text="Generate",
            width=100,
            height=38,
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
            command=self.generate_report
        ).pack(
            side="left",
            padx=8
        )

        ctk.CTkButton(
            top,
            text="Export CSV",
            width=100,
            height=38,
            fg_color=INPUT_BG,
            hover_color="#E2E8F0",
            text_color=TEXT,
            command=self.export_csv
        ).pack(
            side="left"
        )

        self.report_text = ctk.CTkTextbox(
            self.reports_tab,
            fg_color=WHITE,
            border_width=1,
            border_color=BORDER,
            text_color=TEXT
        )

        self.report_text.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

    def generate_report(self):

        kind = self.report_type.get()

        try:

            start = self.get_date_value(
                self.report_from
            )

            end = self.get_date_value(
                self.report_to
            )

        except ValueError as e:

            messagebox.showerror(
                "Invalid Date",
                str(e)
            )

            return

        if kind == "Summary Report":

            self.generate_summary(
                start,
                end
            )

        elif kind == "Student Report":

            self.generate_student_report(
                start,
                end
            )

        else:

            self.generate_daily_report(
                start
            )

    def generate_summary(
        self,
        start,
        end
    ):

        try:

            conn = get_connection()
            cursor = conn.cursor()

            query = """
                SELECT
                    s.full_name,
                    s.student_id_number,
                    COUNT(a.id),
                    SUM(
                        CASE
                            WHEN a.status = 'Present'
                            THEN 1
                            ELSE 0
                        END
                    ),
                    SUM(
                        CASE
                            WHEN a.status = 'Absent'
                            THEN 1
                            ELSE 0
                        END
                    )
                FROM students s
                LEFT JOIN attendance a
                    ON a.student_id = s.id
            """

            conditions = []
            params = []

            if start:

                conditions.append(
                    "a.attendance_date >= ?"
                )

                params.append(start)

            if end:

                conditions.append(
                    "a.attendance_date <= ?"
                )

                params.append(end)

            if conditions:

                query += (
                    " WHERE "
                    + " AND ".join(
                        conditions
                    )
                )

            query += """
                GROUP BY s.id
                ORDER BY s.full_name
            """

            cursor.execute(
                query,
                params
            )

            rows = cursor.fetchall()

            conn.close()

        except Exception as e:

            messagebox.showerror(
                "Report Error",
                str(e)
            )

            return

        headers = [
            "Student",
            "Student ID",
            "Days",
            "Present",
            "Absent",
            "Percentage",
            "Remark"
        ]

        report_rows = []

        for row in rows:

            total = row[2] or 0
            present = row[3] or 0
            absent = row[4] or 0

            percentage = (
                present / total * 100
                if total
                else 0
            )

            report_rows.append(
                (
                    row[0],
                    row[1] or "N/A",
                    total,
                    present,
                    absent,
                    f"{percentage:.1f}%",
                    (
                        "OK"
                        if percentage >= MIN_PERCENT
                        else "LOW"
                    )
                )
            )

        self.display_report(
            "SIWES ATTENDANCE SUMMARY",
            headers,
            report_rows
        )

    def generate_student_report(
        self,
        start,
        end
    ):

        student_id = self.student_id_from_choice(
            self.report_student.get()
        )

        if not student_id:

            messagebox.showwarning(
                "Select Student",
                "Choose a student first."
            )

            return

        try:

            conn = get_connection()
            cursor = conn.cursor()

            query = """
                SELECT
                    attendance_date,
                    status,
                    remarks
                FROM attendance
                WHERE student_id = ?
            """

            params = [
                student_id
            ]

            if start:

                query += """
                    AND attendance_date >= ?
                """

                params.append(start)

            if end:

                query += """
                    AND attendance_date <= ?
                """

                params.append(end)

            query += """
                ORDER BY attendance_date DESC
            """

            cursor.execute(
                query,
                params
            )

            rows = cursor.fetchall()

            conn.close()

        except Exception as e:

            messagebox.showerror(
                "Report Error",
                str(e)
            )

            return

        headers = [
            "Date",
            "Status",
            "Remarks"
        ]

        report_rows = [
            (
                row[0],
                row[1],
                row[2] or ""
            )
            for row in rows
        ]

        self.display_report(
            "STUDENT ATTENDANCE REPORT",
            headers,
            report_rows
        )

    def generate_daily_report(
        self,
        date
    ):

        if not date:

            messagebox.showwarning(
                "Date Needed",
                "Enter a date."
            )

            return

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    s.full_name,
                    s.student_id_number,
                    a.status,
                    a.remarks
                FROM attendance a
                JOIN students s
                    ON s.id = a.student_id
                WHERE a.attendance_date = ?
                ORDER BY s.full_name
                """,
                (date,)
            )

            rows = cursor.fetchall()

            conn.close()

        except Exception as e:

            messagebox.showerror(
                "Report Error",
                str(e)
            )

            return

        headers = [
            "Student",
            "Student ID",
            "Status",
            "Remarks"
        ]

        report_rows = [
            (
                row[0],
                row[1] or "N/A",
                row[2],
                row[3] or ""
            )
            for row in rows
        ]

        self.display_report(
            f"DAILY ATTENDANCE: {date}",
            headers,
            report_rows
        )

    def display_report(
        self,
        title,
        headers,
        rows
    ):

        self.report_headers = headers
        self.report_rows = rows

        self.report_text.delete(
            "1.0",
            "end"
        )

        output = [
            title,
            f"Generated: {self.today()}",
            ""
        ]

        if not rows:

            output.append(
                "No records found."
            )

        else:

            widths = []

            for index, header in enumerate(headers):

                values = [
                    str(row[index])
                    for row in rows
                ]

                widths.append(
                    max(
                        len(str(header)),
                        *[
                            len(value)
                            for value in values
                        ]
                    )
                )

            def format_row(row):

                return "   ".join(
                    str(value).ljust(
                        widths[index]
                    )
                    for index, value
                    in enumerate(row)
                )

            output.append(
                format_row(headers)
            )

            output.append(
                "   ".join(
                    "-" * width
                    for width in widths
                )
            )

            for row in rows:

                output.append(
                    format_row(row)
                )

        self.report_text.insert(
            "1.0",
            "\n".join(output)
        )

    def export_csv(self):

        if not self.report_rows:

            messagebox.showinfo(
                "Nothing to Export",
                "Generate a report first."
            )

            return

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                (
                    "CSV files",
                    "*.csv"
                )
            ]
        )

        if not path:

            return

        try:

            with open(
                path,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(
                    file
                )

                writer.writerow(
                    self.report_headers
                )

                writer.writerows(
                    self.report_rows
                )

            messagebox.showinfo(
                "Exported",
                f"Report saved to:\n{path}"
            )

        except Exception as e:

            messagebox.showerror(
                "Export Error",
                str(e)
            )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    ctk.set_appearance_mode(
        "light"
    )

    ctk.set_default_color_theme(
        "blue"
    )

    root = ctk.CTk()

    root.geometry(
        "1200x700"
    )

    root.title(
        "SIWES Attendance"
    )

    test_user = {
        "id": 1,
        "username": "test",
        "full_name": "Test Student",
        "role": "student"
    }

    page = AttendancePage(
        root,
        test_user
    )

    page.pack(
        fill="both",
        expand=True
    )

    root.mainloop()