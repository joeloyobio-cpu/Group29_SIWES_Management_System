import customtkinter as ctk
import sqlite3
from pathlib import Path


# ============================================================
# DATABASE
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "siwes_management.db"


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

    def __init__(self, user, logout_callback=None):

        self.user = user
        self.logout_callback = logout_callback

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

        user_label = ctk.CTkLabel(
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

        user_label.pack(
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

            self.show_student_information()

        else:

            self.show_placeholder(
                page_name
            )

    # ========================================================
    # GENERAL PLACEHOLDER
    # ========================================================

    def show_placeholder(self, page_name):

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
    # STUDENT INFORMATION
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
            pady=(30, 5)
        )

        subtitle = ctk.CTkLabel(
            self.main_area,
            text=(
                "View and update your SIWES "
                "student information."
            ),
            font=ctk.CTkFont(
                size=14
            ),
            text_color=TEXT_LIGHT
        )

        subtitle.pack(
            anchor="w",
            padx=40,
            pady=(0, 20)
        )

        # ----------------------------------------------------
        # FORM CONTAINER
        # ----------------------------------------------------

        form = ctk.CTkScrollableFrame(
            self.main_area,
            fg_color=WHITE,
            corner_radius=12
        )

        form.pack(
            padx=40,
            pady=10,
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

        # ----------------------------------------------------
        # INPUTS
        # ----------------------------------------------------

        self.info_full_name = self.create_form_input(
            form,
            "Full Name",
            0,
            0
        )

        self.info_email = self.create_form_input(
            form,
            "Email",
            0,
            1
        )

        self.info_phone = self.create_form_input(
            form,
            "Phone Number",
            1,
            0
        )

        self.info_department = self.create_form_input(
            form,
            "Department",
            1,
            1
        )

        self.info_level = self.create_form_input(
            form,
            "Level",
            2,
            0
        )

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        self.info_status = ctk.CTkLabel(
            form,
            text="",
            font=ctk.CTkFont(
                size=13
            )
        )

        self.info_status.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="w",
            padx=25,
            pady=(20, 10)
        )

        # ----------------------------------------------------
        # SAVE BUTTON
        # ----------------------------------------------------

        save_button = ctk.CTkButton(
            form,
            text="Save Information",
            height=45,
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            command=self.save_student_information
        )

        save_button.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="w",
            padx=25,
            pady=(5, 30)
        )

        # ----------------------------------------------------
        # LOAD DATA
        # ----------------------------------------------------

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
            pady=12
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
            fg_color=INPUT_BG,
            border_color=BORDER,
            border_width=1,
            corner_radius=8
        )

        entry.pack(
            fill="x"
        )

        return entry

    # ========================================================
    # GET USER EMAIL
    # ========================================================

    def get_user_email(self):

        connection = None

        try:

            connection = sqlite3.connect(
                DATABASE_PATH
            )

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

        except sqlite3.Error as error:

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

            return

        connection = None

        try:

            connection = sqlite3.connect(
                DATABASE_PATH
            )

            cursor = connection.cursor()

            # Make sure students table exists
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    department TEXT NOT NULL,
                    level TEXT NOT NULL
                )
                """
            )

            cursor.execute(
                """
                SELECT
                    full_name,
                    email,
                    phone,
                    department,
                    level
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

                full_name, email, phone, department, level = student

                self.info_full_name.insert(
                    0,
                    full_name or ""
                )

                self.info_email.insert(
                    0,
                    email or ""
                )

                self.info_phone.insert(
                    0,
                    phone or ""
                )

                self.info_department.insert(
                    0,
                    department or ""
                )

                self.info_level.insert(
                    0,
                    level or ""
                )

                self.info_status.configure(
                    text="Your information has been loaded.",
                    text_color=SUCCESS
                )

            else:

                # New student profile
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
                        "Enter your details and save."
                    ),
                    text_color=TEXT_LIGHT
                )

        except sqlite3.Error as error:

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

        department = (
            self.info_department.get().strip()
        )

        level = (
            self.info_level.get().strip()
        )

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

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

            connection = sqlite3.connect(
                DATABASE_PATH
            )

            cursor = connection.cursor()

            # Make sure table exists
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    department TEXT NOT NULL,
                    level TEXT NOT NULL
                )
                """
            )

            # Check whether profile exists
            cursor.execute(
                """
                SELECT id
                FROM students
                WHERE email = ?
                LIMIT 1
                """,
                (
                    email,
                )
            )

            existing = cursor.fetchone()

            if existing:

                cursor.execute(
                    """
                    UPDATE students
                    SET
                        full_name = ?,
                        phone = ?,
                        department = ?,
                        level = ?
                    WHERE email = ?
                    """,
                    (
                        full_name,
                        phone,
                        department,
                        level,
                        email
                    )
                )

            else:

                cursor.execute(
                    """
                    INSERT INTO students (
                        full_name,
                        email,
                        phone,
                        department,
                        level
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        full_name,
                        email,
                        phone,
                        department,
                        level
                    )
                )

            connection.commit()

            self.info_status.configure(
                text=(
                    "Student information "
                    "saved successfully."
                ),
                text_color=SUCCESS
            )

            # Update sidebar name
            self.user["full_name"] = full_name

        except sqlite3.IntegrityError:

            self.info_status.configure(
                text=(
                    "That email already belongs "
                    "to another student."
                ),
                text_color=ERROR
            )

        except sqlite3.Error as error:

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