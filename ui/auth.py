import customtkinter as ctk
import sqlite3
import hashlib
import os
import re
from pathlib import Path


# ============================================================
# DATABASE PATH
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
# APPEARANCE
# ============================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# ============================================================
# PASSWORD HASHING
# ============================================================

def hash_password(password):
    """
    Create a secure password hash using PBKDF2.
    """

    salt = os.urandom(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000
    )

    return (
        salt.hex()
        + ":"
        + password_hash.hex()
    )


def verify_password(password, stored_password):
    """
    Verify a password against the stored password hash.
    """

    try:
        salt_hex, hash_hex = stored_password.split(":")

        salt = bytes.fromhex(salt_hex)
        original_hash = bytes.fromhex(hash_hex)

        new_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            100000
        )

        return new_hash == original_hash

    except (ValueError, TypeError):
        return False


# ============================================================
# DATABASE SETUP
# ============================================================

def setup_database():
    """
    Make sure the users table exists.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

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

    connection.commit()
    connection.close()


# ============================================================
# AUTHENTICATION WINDOW
# ============================================================

class AuthWindow:

    def __init__(self):

        setup_database()

        self.app = ctk.CTk()

        self.app.title(
            "SIWES Management System"
        )

        self.app.geometry(
            "1200x700"
        )

        self.app.minsize(
            1000,
            620
        )

        self.app.configure(
            fg_color=WHITE
        )

        self.branding_frame = None
        self.form_frame = None

        self.show_login()

        self.app.mainloop()


    # ========================================================
    # BRANDING PANEL
    # ========================================================

    def create_branding_panel(self):

        self.branding_frame = ctk.CTkFrame(
            self.app,
            width=470,
            corner_radius=0,
            fg_color=NAVY
        )

        self.branding_frame.pack(
            side="left",
            fill="both"
        )

        self.branding_frame.pack_propagate(False)

        # Decorative circle
        circle = ctk.CTkFrame(
            self.branding_frame,
            width=260,
            height=260,
            corner_radius=130,
            fg_color=NAVY_LIGHT
        )

        circle.place(
            x=-90,
            y=-90
        )

        # Main content
        content = ctk.CTkFrame(
            self.branding_frame,
            fg_color="transparent"
        )

        content.pack(
            padx=55,
            pady=55,
            fill="both",
            expand=True
        )

        # Graduation cap
        cap = ctk.CTkLabel(
            content,
            text="🎓",
            font=ctk.CTkFont(
                size=58
            )
        )

        cap.pack(
            anchor="w",
            pady=(10, 20)
        )

        # Main title
        title = ctk.CTkLabel(
            content,
            text="SIWES",
            font=ctk.CTkFont(
                size=38,
                weight="bold"
            ),
            text_color=WHITE
        )

        title.pack(
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            content,
            text="Management System",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            ),
            text_color=WHITE
        )

        subtitle.pack(
            anchor="w",
            pady=(0, 20)
        )

        # Motto
        motto = ctk.CTkLabel(
            content,
            text=(
                "...Connecting students,\n"
                "supervisors and institutions\n"
                "for a brighter future."
            ),
            font=ctk.CTkFont(
                size=16
            ),
            text_color="#D7E5F5",
            justify="left"
        )

        motto.pack(
            anchor="w",
            pady=(0, 40)
        )

        # Service areas
        services = [
            (
                "STUDENTS",
                "Manage SIWES activities and logbooks"
            ),
            (
                "SUPERVISORS",
                "Monitor students and provide feedback"
            ),
            (
                "INSTITUTIONS",
                "Manage placements and reports"
            )
        ]

        for heading, description in services:

            service = ctk.CTkFrame(
                content,
                fg_color="transparent"
            )

            service.pack(
                fill="x",
                pady=8
            )

            heading_label = ctk.CTkLabel(
                service,
                text=heading,
                font=ctk.CTkFont(
                    size=13,
                    weight="bold"
                ),
                text_color=WHITE
            )

            heading_label.pack(
                anchor="w"
            )

            description_label = ctk.CTkLabel(
                service,
                text=description,
                font=ctk.CTkFont(
                    size=12
                ),
                text_color="#B8CCE2"
            )

            description_label.pack(
                anchor="w",
                pady=(2, 0)
            )


    # ========================================================
    # FORM AREA
    # ========================================================

    def create_form_area(self):

        self.form_frame = ctk.CTkFrame(
            self.app,
            fg_color=WHITE,
            corner_radius=0
        )

        self.form_frame.pack(
            side="right",
            fill="both",
            expand=True
        )


    # ========================================================
    # CLEAR CURRENT FORM
    # ========================================================

    def clear_form(self):

        if self.form_frame is not None:
            self.form_frame.destroy()

        if self.branding_frame is not None:
            self.branding_frame.destroy()


    # ========================================================
    # LOGIN PAGE
    # ========================================================

    def show_login(self):

        self.clear_form()

        self.create_branding_panel()

        self.create_form_area()

        container = ctk.CTkFrame(
            self.form_frame,
            fg_color="transparent"
        )

        container.pack(
            padx=80,
            pady=55,
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # Heading
        # ----------------------------------------------------

        heading = ctk.CTkLabel(
            container,
            text="Welcome Back",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            ),
            text_color=TEXT
        )

        heading.pack(
            anchor="w"
        )

        description = ctk.CTkLabel(
            container,
            text="Sign in to continue to your SIWES account.",
            font=ctk.CTkFont(
                size=14
            ),
            text_color=TEXT_LIGHT
        )

        description.pack(
            anchor="w",
            pady=(5, 35)
        )

        # ----------------------------------------------------
        # Username / Email
        # ----------------------------------------------------

        username_label = ctk.CTkLabel(
            container,
            text="Username or Email",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=TEXT
        )

        username_label.pack(
            anchor="w"
        )

        self.login_username = ctk.CTkEntry(
            container,
            height=48,
            placeholder_text="Enter your username or email",
            fg_color=INPUT_BG,
            border_color=BORDER,
            border_width=1,
            corner_radius=8
        )

        self.login_username.pack(
            fill="x",
            pady=(7, 20)
        )

        # ----------------------------------------------------
        # Password
        # ----------------------------------------------------

        password_label = ctk.CTkLabel(
            container,
            text="Password",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=TEXT
        )

        password_label.pack(
            anchor="w"
        )

        password_frame = ctk.CTkFrame(
            container,
            fg_color="transparent"
        )

        password_frame.pack(
            fill="x",
            pady=(7, 10)
        )

        self.login_password = ctk.CTkEntry(
            password_frame,
            height=48,
            placeholder_text="Enter your password",
            show="•",
            fg_color=INPUT_BG,
            border_color=BORDER,
            border_width=1,
            corner_radius=8
        )

        self.login_password.pack(
            fill="x",
            expand=True
        )

        self.login_password_button = ctk.CTkButton(
            password_frame,
            text="Show",
            width=65,
            height=40,
            fg_color=WHITE,
            hover_color="#EAF1FB",
            text_color=BLUE,
            command=self.toggle_login_password
        )

        self.login_password_button.place(
            relx=1.0,
            rely=0.5,
            anchor="e",
            x=-5
        )

        # ----------------------------------------------------
        # Remember me
        # ----------------------------------------------------

        self.remember_me = ctk.BooleanVar(
            value=False
        )

        remember = ctk.CTkCheckBox(
            container,
            text="Remember me",
            variable=self.remember_me,
            font=ctk.CTkFont(
                size=13
            ),
            text_color=TEXT_LIGHT,
            checkbox_width=18,
            checkbox_height=18
        )

        remember.pack(
            anchor="w",
            pady=(0, 25)
        )

        # ----------------------------------------------------
        # Status message
        # ----------------------------------------------------

        self.login_status = ctk.CTkLabel(
            container,
            text="",
            font=ctk.CTkFont(
                size=12
            ),
            text_color=ERROR
        )

        self.login_status.pack(
            anchor="w",
            pady=(0, 5)
        )

        # ----------------------------------------------------
        # Sign In button
        # ----------------------------------------------------

        login_button = ctk.CTkButton(
            container,
            text="Sign In",
            height=50,
            corner_radius=8,
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            command=self.login
        )

        login_button.pack(
            fill="x",
            pady=(0, 30)
        )

        # ----------------------------------------------------
        # Create Account
        # ----------------------------------------------------

        bottom = ctk.CTkFrame(
            container,
            fg_color="transparent"
        )

        bottom.pack()

        question = ctk.CTkLabel(
            bottom,
            text="Don't have an account?",
            font=ctk.CTkFont(
                size=13
            ),
            text_color=TEXT_LIGHT
        )

        question.pack(
            side="left"
        )

        signup_button = ctk.CTkButton(
            bottom,
            text="Create Account",
            width=125,
            fg_color="transparent",
            hover_color="#EAF1FB",
            text_color=BLUE,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=self.show_signup
        )

        signup_button.pack(
            side="left",
            padx=(5, 0)
        )

        # Enter key
        self.login_username.bind(
            "<Return>",
            lambda event: self.login()
        )

        self.login_password.bind(
            "<Return>",
            lambda event: self.login()
        )


    # ========================================================
    # SIGNUP PAGE
    # ========================================================

    def show_signup(self):

        self.clear_form()

        self.create_branding_panel()

        self.create_form_area()

        container = ctk.CTkFrame(
            self.form_frame,
            fg_color="transparent"
        )

        container.pack(
            padx=75,
            pady=35,
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # Heading
        # ----------------------------------------------------

        heading = ctk.CTkLabel(
            container,
            text="Create Your Account",
            font=ctk.CTkFont(
                size=29,
                weight="bold"
            ),
            text_color=TEXT
        )

        heading.pack(
            anchor="w"
        )

        description = ctk.CTkLabel(
            container,
            text="Create an account to access the SIWES Management System.",
            font=ctk.CTkFont(
                size=13
            ),
            text_color=TEXT_LIGHT
        )

        description.pack(
            anchor="w",
            pady=(5, 20)
        )

        # ----------------------------------------------------
        # Full Name
        # ----------------------------------------------------

        self.signup_full_name = self.create_input(
            container,
            "Full Name",
            "Enter your full name"
        )

        # ----------------------------------------------------
        # Username
        # ----------------------------------------------------

        self.signup_username = self.create_input(
            container,
            "Username",
            "Choose a username"
        )

        # ----------------------------------------------------
        # Email
        # ----------------------------------------------------

        self.signup_email = self.create_input(
            container,
            "Email Address",
            "Enter your email address"
        )

        # ----------------------------------------------------
        # Password
        # ----------------------------------------------------

        self.signup_password = self.create_input(
            container,
            "Password",
            "Create a password",
            password=True
        )

        # ----------------------------------------------------
        # Confirm Password
        # ----------------------------------------------------

        self.signup_confirm = self.create_input(
            container,
            "Confirm Password",
            "Confirm your password",
            password=True
        )

        # ----------------------------------------------------
        # Status
        # ----------------------------------------------------

        self.signup_status = ctk.CTkLabel(
            container,
            text="",
            font=ctk.CTkFont(
                size=12
            ),
            text_color=ERROR
        )

        self.signup_status.pack(
            anchor="w",
            pady=(0, 5)
        )

        # ----------------------------------------------------
        # Create Account button
        # ----------------------------------------------------

        create_button = ctk.CTkButton(
            container,
            text="Create Account",
            height=48,
            corner_radius=8,
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            command=self.create_account
        )

        create_button.pack(
            fill="x",
            pady=(0, 15)
        )

        # ----------------------------------------------------
        # Back to Sign In
        # ----------------------------------------------------

        back_button = ctk.CTkButton(
            container,
            text="← Back to Sign In",
            height=40,
            fg_color="transparent",
            hover_color="#EAF1FB",
            text_color=BLUE,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=self.show_login
        )

        back_button.pack(
            pady=(0, 0)
        )

        # Enter key
        self.signup_confirm.bind(
            "<Return>",
            lambda event: self.create_account()
        )


    # ========================================================
    # INPUT CREATOR
    # ========================================================

    def create_input(
        self,
        parent,
        label_text,
        placeholder,
        password=False
    ):

        label = ctk.CTkLabel(
            parent,
            text=label_text,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=TEXT
        )

        label.pack(
            anchor="w"
        )

        entry = ctk.CTkEntry(
            parent,
            height=42,
            placeholder_text=placeholder,
            fg_color=INPUT_BG,
            border_color=BORDER,
            border_width=1,
            corner_radius=8,
            show="•" if password else None
        )

        entry.pack(
            fill="x",
            pady=(5, 11)
        )

        return entry


    # ========================================================
    # LOGIN PASSWORD TOGGLE
    # ========================================================

    def toggle_login_password(self):

        if self.login_password.cget("show") == "":

            self.login_password.configure(
                show="•"
            )

            self.login_password_button.configure(
                text="Show"
            )

        else:

            self.login_password.configure(
                show=""
            )

            self.login_password_button.configure(
                text="Hide"
            )


    # ========================================================
    # LOGIN
    # ========================================================

    def login(self):

        username_or_email = (
            self.login_username.get().strip()
        )

        password = self.login_password.get()

        # Validate fields
        if not username_or_email:

            self.login_status.configure(
                text="Please enter your username or email.",
                text_color=ERROR
            )

            return

        if not password:

            self.login_status.configure(
                text="Please enter your password.",
                text_color=ERROR
            )

            return

        connection = None

        try:

            connection = sqlite3.connect(
                DATABASE_PATH
            )

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    id,
                    username,
                    password_hash,
                    full_name,
                    role,
                    is_active
                FROM users
                WHERE username = ?
                   OR email = ?
                LIMIT 1
            """, (
                username_or_email,
                username_or_email
            ))

            user = cursor.fetchone()

            # User doesn't exist
            if user is None:

                self.login_status.configure(
                    text="Invalid username/email or password.",
                    text_color=ERROR
                )

                return

            user_id = user[0]
            username = user[1]
            stored_password = user[2]
            full_name = user[3]
            role = user[4]
            is_active = user[5]

            # Account disabled
            if not is_active:

                self.login_status.configure(
                    text="This account has been disabled.",
                    text_color=ERROR
                )

                return

            # Wrong password
            if not verify_password(
                password,
                stored_password
            ):

                self.login_status.configure(
                    text="Invalid username/email or password.",
                    text_color=ERROR
                )

                return

            # Successful login
            self.login_status.configure(
                text=f"Welcome, {full_name}!",
                text_color=SUCCESS
            )

            print(
                "LOGIN SUCCESSFUL"
            )

            print(
                f"User ID: {user_id}"
            )

            print(
                f"Username: {username}"
            )

            print(
                f"Role: {role}"
            )

            # Dashboard will be connected here next.

        except sqlite3.Error as error:

            self.login_status.configure(
                text="Database error. Please try again.",
                text_color=ERROR
            )

            print(
                f"Database error: {error}"
            )

        finally:

            if connection is not None:
                connection.close()


    # ========================================================
    # CREATE ACCOUNT
    # ========================================================

    def create_account(self):

        full_name = (
            self.signup_full_name.get().strip()
        )

        username = (
            self.signup_username.get().strip()
        )

        email = (
            self.signup_email.get().strip()
        )

        password = (
            self.signup_password.get()
        )

        confirm_password = (
            self.signup_confirm.get()
        )

        # ----------------------------------------------------
        # Required fields
        # ----------------------------------------------------

        if not full_name:

            self.signup_status.configure(
                text="Please enter your full name.",
                text_color=ERROR
            )

            return

        if not username:

            self.signup_status.configure(
                text="Please choose a username.",
                text_color=ERROR
            )

            return

        if not email:

            self.signup_status.configure(
                text="Please enter your email address.",
                text_color=ERROR
            )

            return

        if not password:

            self.signup_status.configure(
                text="Please create a password.",
                text_color=ERROR
            )

            return

        if not confirm_password:

            self.signup_status.configure(
                text="Please confirm your password.",
                text_color=ERROR
            )

            return

        # ----------------------------------------------------
        # Username validation
        # ----------------------------------------------------

        if len(username) < 3:

            self.signup_status.configure(
                text="Username must be at least 3 characters.",
                text_color=ERROR
            )

            return

        if " " in username:

            self.signup_status.configure(
                text="Username cannot contain spaces.",
                text_color=ERROR
            )

            return

        # ----------------------------------------------------
        # Email validation
        # ----------------------------------------------------

        email_pattern = (
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        )

        if not re.match(
            email_pattern,
            email
        ):

            self.signup_status.configure(
                text="Please enter a valid email address.",
                text_color=ERROR
            )

            return

        # ----------------------------------------------------
        # Password validation
        # ----------------------------------------------------

        if len(password) < 6:

            self.signup_status.configure(
                text="Password must be at least 6 characters.",
                text_color=ERROR
            )

            return

        # ----------------------------------------------------
        # Confirm password
        # ----------------------------------------------------

        if password != confirm_password:

            self.signup_status.configure(
                text="Passwords do not match.",
                text_color=ERROR
            )

            return

        connection = None

        try:

            connection = sqlite3.connect(
                DATABASE_PATH
            )

            cursor = connection.cursor()

            # ------------------------------------------------
            # Check username
            # ------------------------------------------------

            cursor.execute("""
                SELECT id
                FROM users
                WHERE username = ?
                LIMIT 1
            """, (username,))

            existing_username = cursor.fetchone()

            if existing_username is not None:

                self.signup_status.configure(
                    text="That username is already taken.",
                    text_color=ERROR
                )

                return

            # ------------------------------------------------
            # Check email
            # ------------------------------------------------

            cursor.execute("""
                SELECT id
                FROM users
                WHERE email = ?
                LIMIT 1
            """, (email,))

            existing_email = cursor.fetchone()

            if existing_email is not None:

                self.signup_status.configure(
                    text="That email is already registered.",
                    text_color=ERROR
                )

                return

            # ------------------------------------------------
            # Hash password
            # ------------------------------------------------

            password_hash = hash_password(
                password
            )

            # ------------------------------------------------
            # Create account
            # ------------------------------------------------

            cursor.execute("""
                INSERT INTO users (
                    username,
                    password_hash,
                    full_name,
                    email,
                    role,
                    is_active
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                username,
                password_hash,
                full_name,
                email,
                "student",
                1
            ))

            connection.commit()

            # ------------------------------------------------
            # Success
            # ------------------------------------------------

            self.signup_status.configure(
                text="Account created successfully! You can now sign in.",
                text_color=SUCCESS
            )

            # Clear fields
            self.signup_full_name.delete(
                0,
                "end"
            )

            self.signup_username.delete(
                0,
                "end"
            )

            self.signup_email.delete(
                0,
                "end"
            )

            self.signup_password.delete(
                0,
                "end"
            )

            self.signup_confirm.delete(
                0,
                "end"
            )

            print(
                "ACCOUNT CREATED SUCCESSFULLY"
            )

        except sqlite3.IntegrityError:

            self.signup_status.configure(
                text="Username or email already exists.",
                text_color=ERROR
            )

        except sqlite3.Error as error:

            self.signup_status.configure(
                text="Database error. Please try again.",
                text_color=ERROR
            )

            print(
                f"Database error: {error}"
            )

        finally:

            if connection is not None:
                connection.close()


# ============================================================
# START AUTHENTICATION
# ============================================================

def start_auth():

    AuthWindow()


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    start_auth()