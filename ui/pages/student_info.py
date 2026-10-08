import customtkinter as ctk

from database.database import get_connection

from ui.theme import (
    WHITE,
    TEXT,
    TEXT_LIGHT,
    INPUT_BG,
    BORDER,
    SUCCESS,
    ERROR,
    BLUE,
    BLUE_HOVER
)

from ui.components import (
    PageHeader,
    Card,
    PrimaryButton,
    SecondaryButton,
    SuccessButton,
    FormField
)


class StudentInfoPage(ctk.CTkFrame):

    def __init__(self, parent, user):

        super().__init__(
            parent,
            fg_color="#F4F7FB"
        )

        self.user = user
        self.editing = False

        self.build_page()
        self.load_information()

    # ========================================================
    # BUILD PAGE
    # ========================================================

    def build_page(self):

        PageHeader(
            self,
            title="My Information",
            subtitle=(
                "View and manage your personal "
                "and academic information."
            )
        )

        # ----------------------------------------------------
        # SCROLLABLE CONTENT
        # ----------------------------------------------------

        self.content = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=(0, 30)
        )

        # ----------------------------------------------------
        # ACTION BAR
        # ----------------------------------------------------

        action_bar = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        action_bar.pack(
            fill="x",
            pady=(0, 15)
        )

        self.edit_button = PrimaryButton(
            action_bar,
            text="Edit Information",
            command=self.enable_editing,
            width=160
        )

        self.edit_button.pack(
            side="right"
        )

        # ----------------------------------------------------
        # PERSONAL INFORMATION CARD
        # ----------------------------------------------------

        personal_card = Card(
            self.content
        )

        personal_card.pack(
            fill="x",
            pady=(0, 15)
        )

        SectionTitle(
            personal_card,
            "Personal Information",
            "Basic contact and identity information."
        ).pack(
            fill="x",
            padx=25,
            pady=(20, 15)
        )

        personal_grid = ctk.CTkFrame(
            personal_card,
            fg_color="transparent"
        )

        personal_grid.pack(
            fill="x",
            padx=25,
            pady=(0, 25)
        )

        personal_grid.grid_columnconfigure(
            0,
            weight=1
        )

        personal_grid.grid_columnconfigure(
            1,
            weight=1
        )

        self.full_name = FormField(
            personal_grid,
            "Full Name",
            placeholder="Enter your full name"
        )

        self.full_name.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 10),
            pady=8
        )

        self.email = FormField(
            personal_grid,
            "Email",
            placeholder="Enter your email"
        )

        self.email.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(10, 0),
            pady=8
        )

        self.phone = FormField(
            personal_grid,
            "Phone Number",
            placeholder="Enter your phone number"
        )

        self.phone.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 10),
            pady=8
        )

        self.student_id = FormField(
            personal_grid,
            "Student / Matric Number",
            placeholder="Enter your student ID"
        )

        self.student_id.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(10, 0),
            pady=8
        )

        # ----------------------------------------------------
        # SCHOOL INFORMATION CARD
        # ----------------------------------------------------

        school_card = Card(
            self.content
        )

        school_card.pack(
            fill="x",
            pady=(0, 15)
        )

        SectionTitle(
            school_card,
            "School Information",
            "Academic information used throughout SIWES."
        ).pack(
            fill="x",
            padx=25,
            pady=(20, 15)
        )

        school_grid = ctk.CTkFrame(
            school_card,
            fg_color="transparent"
        )

        school_grid.pack(
            fill="x",
            padx=25,
            pady=(0, 25)
        )

        school_grid.grid_columnconfigure(
            0,
            weight=1
        )

        school_grid.grid_columnconfigure(
            1,
            weight=1
        )

        self.institution = FormField(
            school_grid,
            "School / Institution",
            placeholder="Enter institution"
        )

        self.institution.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 10),
            pady=8
        )

        self.faculty = FormField(
            school_grid,
            "Faculty",
            placeholder="Enter faculty"
        )

        self.faculty.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(10, 0),
            pady=8
        )

        self.department = FormField(
            school_grid,
            "Department",
            placeholder="Enter department"
        )

        self.department.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 10),
            pady=8
        )

        self.programme = FormField(
            school_grid,
            "Programme / Course",
            placeholder="Enter programme"
        )

        self.programme.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(10, 0),
            pady=8
        )

        self.level = FormField(
            school_grid,
            "Level",
            placeholder="Enter level"
        )

        self.level.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=(0, 10),
            pady=8
        )

        self.session = FormField(
            school_grid,
            "Academic Session",
            placeholder="e.g. 2025/2026"
        )

        self.session.grid(
            row=2,
            column=1,
            sticky="ew",
            padx=(10, 0),
            pady=8
        )

        # ----------------------------------------------------
        # SAVE / CANCEL
        # ----------------------------------------------------

        self.save_bar = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        self.status_label = ctk.CTkLabel(
            self.save_bar,
            text="",
            font=ctk.CTkFont(
                size=13
            ),
            text_color=TEXT_LIGHT
        )

        self.status_label.pack(
            side="left"
        )

        self.cancel_button = SecondaryButton(
            self.save_bar,
            text="Cancel",
            command=self.cancel_editing,
            width=100
        )

        self.cancel_button.pack(
            side="right",
            padx=(8, 0)
        )

        self.save_button = SuccessButton(
            self.save_bar,
            text="Save Changes",
            command=self.save_information,
            width=140
        )

        self.save_button.pack(
            side="right"
        )

        self.save_bar.pack(
            fill="x",
            pady=(0, 20)
        )

        self.set_editable(False)

    # ========================================================
    # LOAD INFORMATION
    # ========================================================

    def load_information(self):

        connection = None

        try:

            connection = get_connection()

            cursor = connection.cursor()

            # Get the account email
            cursor.execute(
                """
                SELECT email
                FROM users
                WHERE id = ?
                LIMIT 1
                """,
                (self.user["id"],)
            )

            account = cursor.fetchone()

            if not account or not account[0]:

                self.status_label.configure(
                    text="No email is associated with this account.",
                    text_color=ERROR
                )

                return

            email = account[0]

            cursor.execute(
                """
                SELECT
                    full_name,
                    email,
                    phone,
                    student_id_number,
                    institution,
                    faculty,
                    department,
                    programme,
                    level,
                    academic_session
                FROM students
                WHERE email = ?
                LIMIT 1
                """,
                (email,)
            )

            student = cursor.fetchone()

            if student:

                values = [
                    (self.full_name, student[0]),
                    (self.email, student[1]),
                    (self.phone, student[2]),
                    (self.student_id, student[3]),
                    (self.institution, student[4]),
                    (self.faculty, student[5]),
                    (self.department, student[6]),
                    (self.programme, student[7]),
                    (self.level, student[8]),
                    (self.session, student[9])
                ]

                for field, value in values:
                    field.set(value)

                self.status_label.configure(
                    text="Student information loaded.",
                    text_color=SUCCESS
                )

            else:

                self.full_name.set(
                    self.user.get(
                        "full_name",
                        ""
                    )
                )

                self.email.set(
                    email
                )

                self.status_label.configure(
                    text=(
                        "No student profile found. "
                        "Click Edit Information to complete it."
                    ),
                    text_color=TEXT_LIGHT
                )

        except Exception as error:

            self.status_label.configure(
                text="Unable to load student information.",
                text_color=ERROR
            )

            print(
                f"Student information error: {error}"
            )

        finally:

            if connection:
                connection.close()

    # ========================================================
    # EDITING
    # ========================================================

    def enable_editing(self):

        self.editing = True

        self.set_editable(True)

        self.edit_button.pack_forget()

        self.save_bar.pack(
            fill="x",
            pady=(0, 20)
        )

        self.status_label.configure(
            text="Editing student information...",
            text_color=TEXT_LIGHT
        )

    def cancel_editing(self):

        self.editing = False

        self.load_information()

        self.set_editable(False)

        self.save_bar.pack_forget()

        self.edit_button.pack(
            side="right"
        )

    def set_editable(self, editable):

        fields = [
            self.full_name,
            self.email,
            self.phone,
            self.student_id,
            self.institution,
            self.faculty,
            self.department,
            self.programme,
            self.level,
            self.session
        ]

        for field in fields:

            field.entry.configure(
                state=(
                    "normal"
                    if editable
                    else "disabled"
                ),
                fg_color=(
                    WHITE
                    if editable
                    else INPUT_BG
                )
            )

    # ========================================================
    # SAVE INFORMATION
    # ========================================================

    def save_information(self):

        full_name = self.full_name.get()
        email = self.email.get()
        phone = self.phone.get()
        student_id = self.student_id.get()
        institution = self.institution.get()
        faculty = self.faculty.get()
        department = self.department.get()
        programme = self.programme.get()
        level = self.level.get()
        academic_session = self.session.get()

        if not full_name:

            self.status_label.configure(
                text="Full name is required.",
                text_color=ERROR
            )

            return

        if not email:

            self.status_label.configure(
                text="Email is required.",
                text_color=ERROR
            )

            return

        if not department:

            self.status_label.configure(
                text="Department is required.",
                text_color=ERROR
            )

            return

        if not level:

            self.status_label.configure(
                text="Level is required.",
                text_color=ERROR
            )

            return

        connection = None

        try:

            connection = get_connection()

            cursor = connection.cursor()

            # Find the current student profile
            cursor.execute(
                """
                SELECT id
                FROM students
                WHERE email = ?
                LIMIT 1
                """,
                (self.user.get("email") or email,)
            )

            existing = cursor.fetchone()

            if existing:

                cursor.execute(
                    """
                    UPDATE students
                    SET
                        full_name = ?,
                        email = ?,
                        phone = ?,
                        student_id_number = ?,
                        institution = ?,
                        faculty = ?,
                        department = ?,
                        programme = ?,
                        level = ?,
                        academic_session = ?
                    WHERE id = ?
                    """,
                    (
                        full_name,
                        email,
                        phone,
                        student_id,
                        institution,
                        faculty,
                        department,
                        programme,
                        level,
                        academic_session,
                        existing[0]
                    )
                )

            else:

                cursor.execute(
                    """
                    INSERT INTO students (
                        full_name,
                        email,
                        phone,
                        student_id_number,
                        institution,
                        faculty,
                        department,
                        programme,
                        level,
                        academic_session
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        full_name,
                        email,
                        phone,
                        student_id,
                        institution,
                        faculty,
                        department,
                        programme,
                        level,
                        academic_session
                    )
                )

            # Keep account information synchronized
            cursor.execute(
                """
                UPDATE users
                SET
                    full_name = ?,
                    email = ?
                WHERE id = ?
                """,
                (
                    full_name,
                    email,
                    self.user["id"]
                )
            )

            connection.commit()

            self.user["full_name"] = full_name
            self.user["email"] = email

            self.status_label.configure(
                text="Student information saved successfully.",
                text_color=SUCCESS
            )

            self.editing = False

            self.set_editable(False)

            self.save_bar.pack_forget()

            self.edit_button.pack(
                side="right"
            )

        except Exception as error:

            if connection:
                connection.rollback()

            self.status_label.configure(
                text="Could not save student information.",
                text_color=ERROR
            )

            print(
                f"Student information error: {error}"
            )

        finally:

            if connection:
                connection.close()


# ============================================================
# SECTION TITLE
# ============================================================

class SectionTitle(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        title,
        subtitle=""
    ):

        super().__init__(
            parent,
            fg_color="transparent"
        )

        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            ),
            text_color=TEXT
        )

        title_label.pack(
            anchor="w"
        )

        if subtitle:

            subtitle_label = ctk.CTkLabel(
                self,
                text=subtitle,
                font=ctk.CTkFont(
                    size=13
                ),
                text_color=TEXT_LIGHT
            )

            subtitle_label.pack(
                anchor="w",
                pady=(3, 0)
            )