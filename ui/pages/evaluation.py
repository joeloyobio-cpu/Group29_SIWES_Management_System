import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

from database.database import get_connection

from ui.theme import (
    BACKGROUND,
    CARD,
    TEXT,
    TEXT_LIGHT,
    BLUE,
    BLUE_HOVER,
    SUCCESS,
    WARNING,
    BORDER,
    CORNER_RADIUS,
)

from ui.components import (
    PageHeader,
    Card,
    SectionHeader,
    PrimaryButton,
    SecondaryButton,
)


class EvaluationPage(ctk.CTkFrame):

    def __init__(self, parent, user_data=None):
        super().__init__(
            parent,
            fg_color=BACKGROUND
        )

        self.user_data = user_data or {}

        self.role = str(
            self.user_data.get(
                "role",
                "student"
            )
        ).lower()

        self.student_id = None
        self.supervisor_id = None

        self.students = []
        self.evaluations = []

        self._find_user_record()

        if self.role == "supervisor":
            self._build_supervisor_ui()
            self._load_supervisor_data()

        elif self.role == "student":
            self._build_student_ui()
            self._load_student_evaluations()

        else:
            self._build_student_ui()
            self._load_student_evaluations()

    # =========================================================
    # FIND USER RECORD
    # =========================================================

    def _find_user_record(self):

        email = self.user_data.get("email")

        if not email:
            return

        try:

            conn = get_connection()

            if self.role == "student":

                row = conn.execute(
                    """
                    SELECT id
                    FROM students
                    WHERE LOWER(email) = LOWER(?)
                    LIMIT 1
                    """,
                    (email,)
                ).fetchone()

                if row:
                    self.student_id = row[0]

            elif self.role == "supervisor":

                row = conn.execute(
                    """
                    SELECT id
                    FROM supervisors
                    WHERE LOWER(email) = LOWER(?)
                    LIMIT 1
                    """,
                    (email,)
                ).fetchone()

                if row:
                    self.supervisor_id = row[0]

            conn.close()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to identify your account.\n\n{e}"
            )

    # =========================================================
    # STUDENT UI
    # =========================================================

    def _build_student_ui(self):

        header = PageHeader(
            self,
            title="Supervisor Feedback",
            subtitle="View evaluations and feedback provided by your supervisor."
        )

        header.pack(
            fill="x",
            padx=24,
            pady=(20, 12)
        )

        content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        content.pack(
            fill="both",
            expand=True,
            padx=24,
            pady=(0, 24)
        )

        card = Card(content)

        card.pack(
            fill="both",
            expand=True
        )

        SectionHeader(
            card,
            title="My Evaluations",
            subtitle="Your supervisor evaluation records."
        ).pack(
            fill="x",
            padx=20,
            pady=(18, 12)
        )

        self.student_scroll = ctk.CTkScrollableFrame(
            card,
            fg_color="transparent"
        )

        self.student_scroll.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

    # =========================================================
    # LOAD STUDENT EVALUATIONS
    # =========================================================

    def _load_student_evaluations(self):

        if not self.student_id:

            self._show_student_message(
                "No student record is linked to this account."
            )

            return

        try:

            conn = get_connection()

            rows = conn.execute(
                """
                SELECT
                    e.id,
                    s.full_name,
                    sup.full_name,
                    e.technical_skills,
                    e.punctuality,
                    e.teamwork,
                    e.communication,
                    e.professionalism,
                    e.comments,
                    e.evaluation_date
                FROM evaluations e

                JOIN students s
                    ON e.student_id = s.id

                LEFT JOIN supervisors sup
                    ON e.supervisor_id = sup.id

                WHERE e.student_id = ?

                ORDER BY e.evaluation_date DESC
                """,
                (self.student_id,)
            ).fetchall()

            conn.close()

            self.evaluations = rows

            self._display_student_evaluations()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load your evaluations.\n\n{e}"
            )

    # =========================================================
    # DISPLAY STUDENT EVALUATIONS
    # =========================================================

    def _display_student_evaluations(self):

        for widget in self.student_scroll.winfo_children():
            widget.destroy()

        if not self.evaluations:

            self._show_student_message(
                "No supervisor evaluation has been recorded yet."
            )

            return

        for evaluation in self.evaluations:

            (
                evaluation_id,
                student_name,
                supervisor_name,
                technical,
                punctuality,
                teamwork,
                communication,
                professionalism,
                comments,
                evaluation_date
            ) = evaluation

            card = ctk.CTkFrame(
                self.student_scroll,
                fg_color=CARD,
                corner_radius=10,
                border_width=1,
                border_color=BORDER
            )

            card.pack(
                fill="x",
                pady=(0, 15)
            )

            title = ctk.CTkLabel(
                card,
                text="Supervisor Evaluation",
                font=ctk.CTkFont(
                    size=19,
                    weight="bold"
                ),
                text_color=TEXT
            )

            title.pack(
                anchor="w",
                padx=20,
                pady=(18, 4)
            )

            supervisor_label = ctk.CTkLabel(
                card,
                text=(
                    f"Supervisor: "
                    f"{supervisor_name or 'N/A'}"
                ),
                font=ctk.CTkFont(
                    size=13,
                    weight="bold"
                ),
                text_color=TEXT_LIGHT
            )

            supervisor_label.pack(
                anchor="w",
                padx=20,
                pady=(0, 3)
            )

            date_label = ctk.CTkLabel(
                card,
                text=(
                    f"Evaluation Date: "
                    f"{self._format_date(evaluation_date)}"
                ),
                font=ctk.CTkFont(
                    size=13
                ),
                text_color=TEXT_LIGHT
            )

            date_label.pack(
                anchor="w",
                padx=20,
                pady=(0, 15)
            )

            scores = ctk.CTkFrame(
                card,
                fg_color=BACKGROUND,
                corner_radius=8
            )

            scores.pack(
                fill="x",
                padx=20,
                pady=(0, 15)
            )

            score_data = [
                ("Technical Skills", technical),
                ("Punctuality", punctuality),
                ("Teamwork", teamwork),
                ("Communication", communication),
                ("Professionalism", professionalism),
            ]

            for index, (label, score) in enumerate(score_data):

                score_label = ctk.CTkLabel(
                    scores,
                    text=f"{label}: {score}/10",
                    font=ctk.CTkFont(
                        size=13,
                        weight="bold"
                    ),
                    text_color=TEXT
                )

                score_label.grid(
                    row=index // 2,
                    column=index % 2,
                    sticky="w",
                    padx=15,
                    pady=8
                )

            comments_title = ctk.CTkLabel(
                card,
                text="Supervisor Comments",
                font=ctk.CTkFont(
                    size=13,
                    weight="bold"
                ),
                text_color=TEXT
            )

            comments_title.pack(
                anchor="w",
                padx=20,
                pady=(0, 5)
            )

            comments_label = ctk.CTkLabel(
                card,
                text=comments or "No comments provided.",
                font=ctk.CTkFont(
                    size=13
                ),
                text_color=TEXT_LIGHT,
                justify="left",
                anchor="w",
                wraplength=700
            )

            comments_label.pack(
                anchor="w",
                padx=20,
                pady=(0, 20)
            )

    # =========================================================
    # STUDENT EMPTY MESSAGE
    # =========================================================

    def _show_student_message(self, message):

        for widget in self.student_scroll.winfo_children():
            widget.destroy()

        label = ctk.CTkLabel(
            self.student_scroll,
            text=message,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            text_color=TEXT_LIGHT
        )

        label.pack(
            pady=80
        )

    # =========================================================
    # SUPERVISOR UI
    # =========================================================

    def _build_supervisor_ui(self):

        header = PageHeader(
            self,
            title="Student Evaluation",
            subtitle="Evaluate students assigned to you."
        )

        header.pack(
            fill="x",
            padx=24,
            pady=(20, 12)
        )

        content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        content.pack(
            fill="both",
            expand=True,
            padx=24,
            pady=(0, 24)
        )

        card = Card(content)

        card.pack(
            fill="both",
            expand=True
        )

        SectionHeader(
            card,
            title="Evaluate Student",
            subtitle="Rate student performance from 1 to 10."
        ).pack(
            fill="x",
            padx=20,
            pady=(18, 12)
        )

        form = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        form.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        form.grid_columnconfigure(
            0,
            weight=1
        )

        # Student

        ctk.CTkLabel(
            form,
            text="Assigned Student",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=TEXT
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 6)
        )

        self.student_combo = ctk.CTkComboBox(
            form,
            values=["Loading..."],
            height=42,
            corner_radius=CORNER_RADIUS,
            border_color=BORDER,
            fg_color=CARD,
            button_color=BLUE,
            button_hover_color=BLUE_HOVER,
            text_color=TEXT,
            state="readonly",
            command=self._student_selected
        )

        self.student_combo.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 18)
        )

        # Scores

        self.technical_entry = self._create_score(
            form,
            "Technical Skills",
            2
        )

        self.punctuality_entry = self._create_score(
            form,
            "Punctuality",
            4
        )

        self.teamwork_entry = self._create_score(
            form,
            "Teamwork",
            6
        )

        self.communication_entry = self._create_score(
            form,
            "Communication",
            8
        )

        self.professionalism_entry = self._create_score(
            form,
            "Professionalism",
            10
        )

        # Comments

        ctk.CTkLabel(
            form,
            text="Comments",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=TEXT
        ).grid(
            row=12,
            column=0,
            sticky="w",
            pady=(0, 6)
        )

        self.comments_text = ctk.CTkTextbox(
            form,
            height=100,
            corner_radius=CORNER_RADIUS,
            border_width=1,
            border_color=BORDER,
            fg_color=CARD,
            text_color=TEXT
        )

        self.comments_text.grid(
            row=13,
            column=0,
            sticky="ew",
            pady=(0, 18)
        )

        # Date

        ctk.CTkLabel(
            form,
            text="Evaluation Date",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=TEXT
        ).grid(
            row=14,
            column=0,
            sticky="w",
            pady=(0, 6)
        )

        self.date_entry = ctk.CTkEntry(
            form,
            height=42,
            corner_radius=CORNER_RADIUS,
            border_color=BORDER,
            fg_color=CARD,
            text_color=TEXT
        )

        self.date_entry.insert(
            0,
            datetime.now().strftime("%d/%m/%Y")
        )

        self.date_entry.grid(
            row=15,
            column=0,
            sticky="ew",
            pady=(0, 18)
        )

        buttons = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        buttons.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        SecondaryButton(
            buttons,
            text="Clear",
            command=self._clear_form
        ).pack(
            side="left"
        )

        PrimaryButton(
            buttons,
            text="Save Evaluation",
            command=self._save_evaluation
        ).pack(
            side="right"
        )

    # =========================================================
    # LOAD SUPERVISOR DATA
    # =========================================================

    def _load_supervisor_data(self):

        if not self.supervisor_id:

            self.student_combo.configure(
                values=["Supervisor profile not found"]
            )

            self.student_combo.set(
                "Supervisor profile not found"
            )

            return

        try:

            conn = get_connection()

            rows = conn.execute(
                """
                SELECT DISTINCT
                    s.id,
                    s.full_name,
                    s.email,
                    s.student_id_number

                FROM students s

                JOIN placements p
                    ON p.student_id = s.id

                WHERE p.supervisor_id = ?

                AND LOWER(COALESCE(p.status, '')) = 'active'

                ORDER BY s.full_name
                """,
                (self.supervisor_id,)
            ).fetchall()

            conn.close()

            self.students = rows

            names = [
                row[1]
                for row in rows
            ]

            if names:

                self.student_combo.configure(
                    values=names
                )

                self.student_combo.set(
                    names[0]
                )

                self._student_selected(
                    names[0]
                )

            else:

                self.student_combo.configure(
                    values=["No assigned students"]
                )

                self.student_combo.set(
                    "No assigned students"
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load assigned students.\n\n{e}"
            )

    # =========================================================
    # SCORE FIELD
    # =========================================================

    def _create_score(
        self,
        parent,
        label,
        row
    ):

        ctk.CTkLabel(
            parent,
            text=f"{label} (1-10)",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=TEXT
        ).grid(
            row=row,
            column=0,
            sticky="w",
            pady=(0, 6)
        )

        entry = ctk.CTkEntry(
            parent,
            placeholder_text="Enter score",
            height=42,
            corner_radius=CORNER_RADIUS,
            border_color=BORDER,
            fg_color=CARD,
            text_color=TEXT
        )

        entry.grid(
            row=row + 1,
            column=0,
            sticky="ew",
            pady=(0, 15)
        )

        return entry

    # =========================================================
    # STUDENT SELECTED
    # =========================================================

    def _student_selected(self, name):

        for student in self.students:

            if student[1] == name:

                self.student_id = student[0]

                break

    # =========================================================
    # SAVE EVALUATION
    # =========================================================

    def _save_evaluation(self):

        if not self.student_id:

            messagebox.showwarning(
                "Student Required",
                "Please select an assigned student."
            )

            return

        scores = [
            (
                "Technical Skills",
                self.technical_entry.get()
            ),
            (
                "Punctuality",
                self.punctuality_entry.get()
            ),
            (
                "Teamwork",
                self.teamwork_entry.get()
            ),
            (
                "Communication",
                self.communication_entry.get()
            ),
            (
                "Professionalism",
                self.professionalism_entry.get()
            ),
        ]

        values = []

        for label, value in scores:

            try:

                score = int(value)

                if score < 1 or score > 10:
                    raise ValueError

                values.append(score)

            except ValueError:

                messagebox.showwarning(
                    "Invalid Score",
                    f"{label} must be between 1 and 10."
                )

                return

        try:

            evaluation_date = datetime.strptime(
                self.date_entry.get().strip(),
                "%d/%m/%Y"
            ).strftime("%Y-%m-%d")

        except ValueError:

            messagebox.showwarning(
                "Invalid Date",
                "Use date format DD/MM/YYYY."
            )

            return

        comments = self.comments_text.get(
            "1.0",
            "end"
        ).strip()

        try:

            conn = get_connection()

            # Security check:
            # make sure this student is actually assigned
            # to the logged-in supervisor.

            assigned = conn.execute(
                """
                SELECT id
                FROM placements
                WHERE student_id = ?
                AND supervisor_id = ?
                AND LOWER(COALESCE(status, '')) = 'active'
                LIMIT 1
                """,
                (
                    self.student_id,
                    self.supervisor_id
                )
            ).fetchone()

            if not assigned:

                conn.close()

                messagebox.showerror(
                    "Access Denied",
                    "This student is not assigned to you."
                )

                return

            conn.execute(
                """
                INSERT INTO evaluations (
                    student_id,
                    supervisor_id,
                    technical_skills,
                    punctuality,
                    teamwork,
                    communication,
                    professionalism,
                    comments,
                    evaluation_date
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    self.student_id,
                    self.supervisor_id,
                    values[0],
                    values[1],
                    values[2],
                    values[3],
                    values[4],
                    comments,
                    evaluation_date
                )
            )

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Student evaluation saved successfully."
            )

            self._clear_form()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to save evaluation.\n\n{e}"
            )

    # =========================================================
    # CLEAR
    # =========================================================

    def _clear_form(self):

        if not self.role == "supervisor":
            return

        for entry in [
            self.technical_entry,
            self.punctuality_entry,
            self.teamwork_entry,
            self.communication_entry,
            self.professionalism_entry
        ]:

            entry.delete(
                0,
                "end"
            )

        self.comments_text.delete(
            "1.0",
            "end"
        )

        self.date_entry.delete(
            0,
            "end"
        )

        self.date_entry.insert(
            0,
            datetime.now().strftime("%d/%m/%Y")
        )

    # =========================================================
    # DATE FORMAT
    # =========================================================

    @staticmethod
    def _format_date(value):

        if not value:
            return "N/A"

        try:

            return datetime.strptime(
                value,
                "%Y-%m-%d"
            ).strftime("%d/%m/%Y")

        except ValueError:

            return value


# =============================================================
# STANDALONE TEST
# =============================================================

if __name__ == "__main__":

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()

    app.geometry(
        "1100x750"
    )

    app.title(
        "SIWES Evaluation"
    )

    test_user = {
        "id": 1,
        "username": "supervisor1",
        "full_name": "Supervisor",
        "email": "supervisor@siwes.com",
        "role": "supervisor"
    }

    page = EvaluationPage(
        app,
        user_data=test_user
    )

    page.pack(
        fill="both",
        expand=True
    )

    app.mainloop()