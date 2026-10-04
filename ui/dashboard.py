import customtkinter as ctk

from database.database import (
    get_connection,
    setup_database
)


# ============================================================
# COLORS
# ============================================================

NAVY = "#102F4F"
NAVY_LIGHT = "#163D62"

BLUE = "#2F7DF6"
BLUE_HOVER = "#2469D8"

WHITE = "#FFFFFF"

TEXT = "#102F4F"
TEXT_LIGHT = "#64748B"

INPUT_BG = "#F4F7FB"
BORDER = "#DCE4EE"

SUCCESS = "#16A34A"
ERROR = "#DC2626"


# ============================================================
# DASHBOARD
# ============================================================

class Dashboard:

    def __init__(
        self,
        user,
        logout_callback=None
    ):

        self.user = user
        self.logout_callback = logout_callback

        # Controls whether My Information is in edit mode
        self.editing_information = False

        # Make sure the shared database is ready
        setup_database()

        self.app = ctk.CTkToplevel()

        self.app.title(
            "SIWES Management System"
        )

        self.app.geometry(
            "1200x700"
        )

        self.app.minsize(
            1000,
            600
        )

        self.app.protocol(
            "WM_DELETE_WINDOW",
            self.logout
        )

        self.create_sidebar()
        self.create_main_area()

    # ========================================================
    # SIDEBAR
    # ========================================================

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self.app,
            width=240,
            corner_radius=0,
            fg_color=NAVY
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        title = ctk.CTkLabel(
            self.sidebar,
            text="SIWES\nManagement",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            ),
            text_color=WHITE
        )

        title.pack(
            padx=25,
            pady=(35, 40)
        )

        role = str(
            self.user.get(
                "role",
                "student"
            )
        ).capitalize()

        self.user_label = ctk.CTkLabel(
            self.sidebar,
            text=(
                f"{self.user.get('full_name', 'User')}\n"
                f"{role}"
            ),
            font=ctk.CTkFont(
                size=14
            ),
            text_color="#D7E5F5"
        )

        self.user_label.pack(
            padx=20,
            pady=(0, 30)
        )

        self.create_menu_buttons()

        logout_button = ctk.CTkButton(
            self.sidebar,
            text="Logout",
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.logout
        )

        logout_button.pack(
            side="bottom",
            padx=20,
            pady=25,
            fill="x"
        )

    # ========================================================
    # MENU BUTTONS
    # ========================================================

    def create_menu_buttons(self):

        role = str(
            self.user.get(
                "role",
                "student"
            )
        ).lower()

        if role == "student":

            menu_items = [
                "Dashboard",
                "My Information",
                "Placement",
                "Digital Logbook",
                "Attendance",
                "Evaluation"
            ]

        elif role == "supervisor":

            menu_items = [
                "Dashboard",
                "My Students",
                "Logbook Review",
                "Evaluations"
            ]

        elif role == "admin":

            menu_items = [
                "Dashboard",
                "Students",
                "Supervisors",
                "Organizations",
                "Placements",
                "Reports"
            ]

        else:

            menu_items = [
                "Dashboard"
            ]

        for item in menu_items:

            button = ctk.CTkButton(
                self.sidebar,
                text=item,
                height=40,
                fg_color="transparent",
                hover_color=NAVY_LIGHT,
                anchor="w",
                command=lambda name=item: (
                    self.show_page(name)
                )
            )

            button.pack(
                padx=15,
                pady=3,
                fill="x"
            )

    # ========================================================
    # MAIN AREA
    # ========================================================

    def create_main_area(self):

        self.main_area = ctk.CTkFrame(
            self.app,
            fg_color="#F4F7FB",
            corner_radius=0
        )

        self.main_area.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.show_page(
            "Dashboard"
        )

    # ========================================================
    # PAGE ROUTER
    # ========================================================

    def show_page(self, page_name):

        for widget in self.main_area.winfo_children():

            widget.destroy()

        if page_name == "My Information":

            self.editing_information = False

            self.show_student_information()

        else:

            self.show_placeholder(
                page_name
            )

    # ========================================================
    # GENERAL PLACEHOLDER
    # ========================================================

    def show_placeholder(
        self,
        page_name
    ):

        title = ctk.CTkLabel(
            self.main_area,
            text=page_name,
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            ),
            text_color=TEXT
        )

        title.pack(
            anchor="w",
            padx=40,
            pady=(40, 10)
        )

        welcome = ctk.CTkLabel(
            self.main_area,
            text=(
                f"Welcome, "
                f"{self.user.get('full_name', 'User')}!"
            ),
            font=ctk.CTkFont(
                size=17
            ),
            text_color=TEXT_LIGHT
        )

        welcome.pack(
            anchor="w",
            padx=40
        )

        info = ctk.CTkFrame(
            self.main_area,
            fg_color=WHITE,
            corner_radius=12
        )

        info.pack(
            padx=40,
            pady=30,
            fill="x"
        )

        message = ctk.CTkLabel(
            info,
            text=(
                f"{page_name} module "
                "is ready to be connected."
            ),
            font=ctk.CTkFont(
                size=16
            ),
            text_color=TEXT
        )

        message.pack(
            padx=30,
            pady=30
        )

    # ========================================================
    # STUDENT INFORMATION PAGE
    # ========================================================

    def show_student_information(self):

        title = ctk.CTkLabel(
            self.main_area,
            text="My Information",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            ),
            text_color=TEXT
        )

        title.pack(
            anchor="w",
            padx=40,
            pady=(25, 5)
        )

        subtitle = ctk.CTkLabel(
            self.main_area,
            text=(
                "View and manage your personal "
                "and school information."
            ),
            font=ctk.CTkFont(
                size=14
            ),
            text_color=TEXT_LIGHT
        )

        subtitle.pack(
            anchor="w",
            padx=40,
            pady=(0, 12)
        )

        # ====================================================
        # ACTION BUTTONS
        # ====================================================

        button_bar = ctk.CTkFrame(
            self.main_area,
            fg_color="transparent"
        )

        button_bar.pack(
            fill="x",
            padx=40,
            pady=(0, 10)
        )

        if not self.editing_information:

            edit_button = ctk.CTkButton(
                button_bar,
                text="Edit Information",
                width=160,
                height=40,
                fg_color=BLUE,
                hover_color=BLUE_HOVER,
                command=self.enable_information_editing
            )

            edit_button.pack(
                side="right"
            )

        else:

            save_button = ctk.CTkButton(
                button_bar,
                text="Save Changes",
                width=150,
                height=40,
                fg_color=SUCCESS,
                hover_color="#15803D",
                command=self.save_student_information
            )

            save_button.pack(
                side="right",
                padx=(8, 0)
            )

            cancel_button = ctk.CTkButton(
                button_bar,
                text="Cancel",
                width=100,
                height=40,
                fg_color="#64748B",
                hover_color="#475569",
                command=self.cancel_information_edit
            )

            cancel_button.pack(
                side="right"
            )

        # ====================================================
        # FORM CONTAINER
        # ====================================================

        form = ctk.CTkScrollableFrame(
            self.main_area,
            fg_color=WHITE,
            corner_radius=12
        )

        form.pack(
            padx=40,
            pady=5,
            fill="both",
            expand=True
        )

        form.grid_columnconfigure(
            0,
            weight=1
        )

        form.grid_columnconfigure(
            1,
            weight=1
        )

        # ====================================================
        # PERSONAL INFORMATION
        # ====================================================

        personal_title = ctk.CTkLabel(
            form,
            text="Personal Information",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            ),
            text_color=TEXT
        )

        personal_title.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=25,
            pady=(20, 5)
        )

        personal_subtitle = ctk.CTkLabel(
            form,
            text=(
                "Basic contact and identity information."
            ),
            font=ctk.CTkFont(
                size=13
            ),
            text_color=TEXT_LIGHT
        )

        personal_subtitle.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="w",
            padx=25,
            pady=(0, 10)
        )

        self.info_full_name = self.create_form_input(
            form,
            "Full Name",
            2,
            0
        )

        self.info_email = self.create_form_input(
            form,
            "Email",
            2,
            1
        )

        self.info_phone = self.create_form_input(
            form,
            "Phone Number",
            3,
            0
        )

        self.info_student_id = self.create_form_input(
            form,
            "Student / Matric Number",
            3,
            1
        )

        # ====================================================
        # SCHOOL INFORMATION
        # ====================================================

        school_title = ctk.CTkLabel(
            form,
            text="School Information",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            ),
            text_color=TEXT
        )

        school_title.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="w",
            padx=25,
            pady=(25, 5)
        )

        school_subtitle = ctk.CTkLabel(
            form,
            text=(
                "Academic information used "
                "throughout the SIWES system."
            ),
            font=ctk.CTkFont(
                size=13
            ),
            text_color=TEXT_LIGHT
        )

        school_subtitle.grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="w",
            padx=25,
            pady=(0, 10)
        )

        self.info_institution = self.create_form_input(
            form,
            "School / Institution",
            6,
            0
        )

        self.info_faculty = self.create_form_input(
            form,
            "Faculty",
            6,
            1
        )

        self.info_department = self.create_form_input(
            form,
            "Department",
            7,
            0
        )

        self.info_programme = self.create_form_input(
            form,
            "Programme / Course",
            7,
            1
        )

        self.info_level = self.create_form_input(
            form,
            "Level",
            8,
            0
        )

        self.info_session = self.create_form_input(
            form,
            "Academic Session",
            8,
            1
        )

        # ====================================================
        # STATUS
        # ====================================================

        self.info_status = ctk.CTkLabel(
            form,
            text="",
            font=ctk.CTkFont(
                size=13
            ),
            text_color=TEXT_LIGHT
        )

        self.info_status.grid(
            row=9,
            column=0,
            columnspan=2,
            sticky="w",
            padx=25,
            pady=(20, 30)
        )

        # Load existing information

        self.load_student_information()

    # ========================================================
    # FORM INPUT
    # ========================================================

    def create_form_input(
        self,
        parent,
        label_text,
        row,
        column
    ):

        frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        frame.grid(
            row=row,
            column=column,
            sticky="ew",
            padx=25,
            pady=8
        )

        label = ctk.CTkLabel(
            frame,
            text=label_text,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=TEXT
        )

        label.pack(
            anchor="w",
            pady=(0, 6)
        )

        entry = ctk.CTkEntry(
            frame,
            height=45,
            fg_color=WHITE,
            text_color=TEXT,
            placeholder_text_color="#94A3B8",
            border_color=BORDER,
            border_width=1,
            corner_radius=8
        )

        entry.pack(
            fill="x"
        )

        return entry

    # ========================================================
    # EDIT MODE
    # ========================================================

    def set_information_editable(
        self,
        editable
    ):

        state = (
            "normal"
            if editable
            else "disabled"
        )

        entries = [
            self.info_full_name,
            self.info_email,
            self.info_phone,
            self.info_student_id,
            self.info_institution,
            self.info_faculty,
            self.info_department,
            self.info_programme,
            self.info_level,
            self.info_session
        ]

        for entry in entries:

            entry.configure(
                state=state,
                fg_color=(
                    WHITE
                    if editable
                    else INPUT_BG
                )
            )

    def enable_information_editing(self):

        # Rebuild the page in edit mode
        self.editing_information = True

        self.show_student_information()

    def cancel_information_edit(self):

        # Return to view mode and reload
        # the saved information from the database.
        self.editing_information = False

        self.show_student_information()

    # ========================================================
    # GET USER EMAIL
    # ========================================================

    def get_user_email(self):

        connection = None

        try:

            connection = get_connection()

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT email
                FROM users
                WHERE id = ?
                LIMIT 1
                """,
                (
                    self.user["id"],
                )
            )

            result = cursor.fetchone()

            if result:

                return result[0]

        except Exception as error:

            print(
                f"Error getting email: {error}"
            )

        finally:

            if connection:

                connection.close()

        return None

    # ========================================================
    # LOAD STUDENT INFORMATION
    # ========================================================

    def load_student_information(self):

        email = self.get_user_email()

        if not email:

            self.info_status.configure(
                text=(
                    "Your account does not "
                    "have an email address."
                ),
                text_color=ERROR
            )

            self.set_information_editable(
                self.editing_information
            )

            return

        connection = None

        try:

            connection = get_connection()

            cursor = connection.cursor()

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
                (
                    email,
                )
            )

            student = cursor.fetchone()

            if student:

                (
                    full_name,
                    student_email,
                    phone,
                    student_id_number,
                    institution,
                    faculty,
                    department,
                    programme,
                    level,
                    academic_session
                ) = student

                values = [
                    (
                        self.info_full_name,
                        full_name
                    ),
                    (
                        self.info_email,
                        student_email
                    ),
                    (
                        self.info_phone,
                        phone
                    ),
                    (
                        self.info_student_id,
                        student_id_number
                    ),
                    (
                        self.info_institution,
                        institution
                    ),
                    (
                        self.info_faculty,
                        faculty
                    ),
                    (
                        self.info_department,
                        department
                    ),
                    (
                        self.info_programme,
                        programme
                    ),
                    (
                        self.info_level,
                        level
                    ),
                    (
                        self.info_session,
                        academic_session
                    )
                ]

                for entry, value in values:

                    entry.insert(
                        0,
                        value or ""
                    )

                self.info_status.configure(
                    text=(
                        "Your information "
                        "has been loaded."
                    ),
                    text_color=SUCCESS
                )

            else:

                self.info_full_name.insert(
                    0,
                    self.user.get(
                        "full_name",
                        ""
                    )
                )

                self.info_email.insert(
                    0,
                    email
                )

                self.info_status.configure(
                    text=(
                        "No student profile found. "
                        "Complete your information "
                        "and save."
                    ),
                    text_color=TEXT_LIGHT
                )

        except Exception as error:

            self.info_status.configure(
                text=(
                    "Unable to load student "
                    "information."
                ),
                text_color=ERROR
            )

            print(
                f"Database error: {error}"
            )

        finally:

            if connection:

                connection.close()

        self.set_information_editable(
            self.editing_information
        )

    # ========================================================
    # SAVE STUDENT INFORMATION
    # ========================================================

    def save_student_information(self):

        full_name = (
            self.info_full_name.get().strip()
        )

        email = (
            self.info_email.get().strip()
        )

        phone = (
            self.info_phone.get().strip()
        )

        student_id_number = (
            self.info_student_id.get().strip()
        )

        institution = (
            self.info_institution.get().strip()
        )

        faculty = (
            self.info_faculty.get().strip()
        )

        department = (
            self.info_department.get().strip()
        )

        programme = (
            self.info_programme.get().strip()
        )

        level = (
            self.info_level.get().strip()
        )

        academic_session = (
            self.info_session.get().strip()
        )

        # ====================================================
        # VALIDATION
        # ====================================================

        if not full_name:

            self.info_status.configure(
                text="Full name is required.",
                text_color=ERROR
            )

            return

        if not email:

            self.info_status.configure(
                text="Email is required.",
                text_color=ERROR
            )

            return

        if not department:

            self.info_status.configure(
                text="Department is required.",
                text_color=ERROR
            )

            return

        if not level:

            self.info_status.configure(
                text="Level is required.",
                text_color=ERROR
            )

            return

        connection = None

        try:

            connection = get_connection()

            cursor = connection.cursor()

            current_email = (
                self.get_user_email()
            )

            # ------------------------------------------------
            # Find existing student profile
            # ------------------------------------------------

            cursor.execute(
                """
                SELECT id
                FROM students
                WHERE email = ?
                LIMIT 1
                """,
                (
                    current_email,
                )
            )

            existing = cursor.fetchone()

            # ------------------------------------------------
            # UPDATE
            # ------------------------------------------------

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
                        student_id_number,
                        institution,
                        faculty,
                        department,
                        programme,
                        level,
                        academic_session,
                        existing[0]
                    )
                )

            # ------------------------------------------------
            # INSERT
            # ------------------------------------------------

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
                    VALUES (
                        ?, ?, ?, ?, ?, ?,
                        ?, ?, ?, ?
                    )
                    """,
                    (
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
                )

            # ------------------------------------------------
            # Keep the login user's name/email synchronized
            # ------------------------------------------------

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

            # Update local user object
            self.user["full_name"] = full_name
            self.user["email"] = email

            # Update sidebar
            role = str(
                self.user.get(
                    "role",
                    "student"
                )
            ).capitalize()

            self.user_label.configure(
                text=(
                    f"{full_name}\n"
                    f"{role}"
                )
            )

            self.info_status.configure(
                text=(
                    "Student information "
                    "saved successfully."
                ),
                text_color=SUCCESS
            )

            # Return to view mode
            self.editing_information = False

            # Rebuild page so Edit Information appears again
            self.show_student_information()

            self.info_status.configure(
                text=(
                    "Student information "
                    "saved successfully."
                ),
                text_color=SUCCESS
            )

        except Exception as error:

            if connection:

                connection.rollback()

            self.info_status.configure(
                text=(
                    "Could not save information."
                ),
                text_color=ERROR
            )

            print(
                f"Database error: {error}"
            )

        finally:

            if connection:

                connection.close()

    # ========================================================
    # LOGOUT
    # ========================================================

    def logout(self):

        if self.app.winfo_exists():

            self.app.destroy()

        if self.logout_callback:

            self.logout_callback()


# ============================================================
# TEST DASHBOARD
# ============================================================

if __name__ == "__main__":

    test_user = {
        "id": 1,
        "username": "test",
        "full_name": "Test Student",
        "role": "student"
    }

    dashboard = Dashboard(
        test_user
    )

    dashboard.app.mainloop()