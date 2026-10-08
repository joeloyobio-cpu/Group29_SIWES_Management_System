import customtkinter as ctk
import hashlib
import os

from database.database import get_connection, setup_database
from ui.dashboard import Dashboard


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
    salt = os.urandom(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000
    )

    return salt.hex() + ":" + password_hash.hex()


def verify_password(password, stored_password):
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
# AUTH WINDOW
# ============================================================

class AuthWindow:

    def __init__(self):

        setup_database()

        self.app = ctk.CTk()

        self.app.title("SIWES Management System")
        self.app.geometry("1200x700")
        self.app.minsize(1000, 620)
        self.app.configure(
            fg_color=WHITE
        )

        self.branding_frame = None
        self.form_frame = None
        self.current_dashboard = None

        self.show_login()

        self.app.mainloop()

    # ========================================================
    # BRANDING
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

        cap = ctk.CTkLabel(
            content,
            text="🎓",
            font=ctk.CTkFont(size=58)
        )

        cap.pack(
            anchor="w",
            pady=(10, 20)
        )

        ctk.CTkLabel(
            content,
            text="SIWES",
            font=ctk.CTkFont(
                size=38,
                weight="bold"
            ),
            text_color=WHITE
        ).pack(anchor="w")

        ctk.CTkLabel(
            content,
            text="Management System",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            ),
            text_color=WHITE
        ).pack(
            anchor="w",
            pady=(0, 20)
        )

        ctk.CTkLabel(
            content,
            text=(
                "Connecting students,\n"
                "supervisors and institutions\n"
                "for a brighter future."
            ),
            font=ctk.CTkFont(size=16),
            text_color="#D7E5F5",
            justify="left"
        ).pack(
            anchor="w",
            pady=(0, 40)
        )

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
                "ADMINISTRATORS",
                "Manage the entire SIWES system"
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

            ctk.CTkLabel(
                service,
                text=heading,
                font=ctk.CTkFont(
                    size=13,
                    weight="bold"
                ),
                text_color=WHITE
            ).pack(anchor="w")

            ctk.CTkLabel(
                service,
                text=description,
                font=ctk.CTkFont(size=12),
                text_color="#B8CCE2"
            ).pack(
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
    # CLEAR
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
            pady=45,
            fill="both",
            expand=True
        )

        ctk.CTkLabel(
            container,
            text="Welcome Back",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            ),
            text_color=TEXT
        ).pack(anchor="w")

        ctk.CTkLabel(
            container,
            text="Select your role and sign in to your SIWES account.",
            font=ctk.CTkFont(size=14),
            text_color=TEXT_LIGHT
        ).pack(
            anchor="w",
            pady=(5, 25)
        )

        # ----------------------------------------------------
        # ROLE
        # ----------------------------------------------------

        ctk.CTkLabel(
            container,
            text="Login As",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=TEXT
        ).pack(anchor="w")

        self.login_role = ctk.CTkComboBox(
            container,
            values=[
                "Student",
                "Supervisor",
                "Admin"
            ],
            height=48,
            fg_color=INPUT_BG,
            text_color=TEXT,
            border_color=BORDER,
            border_width=1,
            corner_radius=8,
            state="readonly"
        )

        self.login_role.set("Student")

        self.login_role.pack(
            fill="x",
            pady=(7, 18)
        )

        # ----------------------------------------------------
        # USERNAME
        # ----------------------------------------------------

        ctk.CTkLabel(
            container,
            text="Username or Email",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=TEXT
        ).pack(anchor="w")

        self.login_username = ctk.CTkEntry(
            container,
            height=48,
            placeholder_text="Enter your username or email",
            fg_color=INPUT_BG,
            text_color=TEXT,
            placeholder_text_color="#94A3B8",
            border_color=BORDER,
            border_width=1,
            corner_radius=8
        )

        self.login_username.pack(
            fill="x",
            pady=(7, 18)
        )

        # ----------------------------------------------------
        # PASSWORD
        # ----------------------------------------------------

        ctk.CTkLabel(
            container,
            text="Password",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=TEXT
        ).pack(anchor="w")

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
            text_color=TEXT,
            placeholder_text_color="#94A3B8",
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
        # STATUS
        # ----------------------------------------------------

        self.login_status = ctk.CTkLabel(
            container,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=ERROR
        )

        self.login_status.pack(
            anchor="w",
            pady=(0, 8)
        )

        # ----------------------------------------------------
        # LOGIN BUTTON
        # ----------------------------------------------------

        ctk.CTkButton(
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
        ).pack(
            fill="x",
            pady=(0, 25)
        )

        # ----------------------------------------------------
        # SIGNUP
        # ----------------------------------------------------

        bottom = ctk.CTkFrame(
            container,
            fg_color="transparent"
        )

        bottom.pack()

        ctk.CTkLabel(
            bottom,
            text="Don't have an account?",
            font=ctk.CTkFont(size=13),
            text_color=TEXT_LIGHT
        ).pack(side="left")

        ctk.CTkButton(
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
        ).pack(
            side="left",
            padx=(5, 0)
        )

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

        ctk.CTkLabel(
            container,
            text="Create Your Account",
            font=ctk.CTkFont(
                size=29,
                weight="bold"
            ),
            text_color=TEXT
        ).pack(anchor="w")

        ctk.CTkLabel(
            container,
            text="Create a student account to access SIWES.",
            font=ctk.CTkFont(size=13),
            text_color=TEXT_LIGHT
        ).pack(
            anchor="w",
            pady=(5, 20)
        )

        self.signup_full_name = self.create_input(
            container,
            "Full Name",
            "Enter your full name"
        )

        self.signup_username = self.create_input(
            container,
            "Username",
            "Choose a username"
        )

        self.signup_email = self.create_input(
            container,
            "Email Address",
            "Enter your email address"
        )

        self.signup_password = self.create_input(
            container,
            "Password",
            "Create a password",
            password=True
        )

        self.signup_confirm = self.create_input(
            container,
            "Confirm Password",
            "Confirm your password",
            password=True
        )

        self.signup_status = ctk.CTkLabel(
            container,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=ERROR
        )

        self.signup_status.pack(
            anchor="w",
            pady=(0, 5)
        )

        ctk.CTkButton(
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
        ).pack(
            fill="x",
            pady=(0, 15)
        )

        ctk.CTkButton(
            container,
            text="← Back to Login",
            fg_color="transparent",
            hover_color="#EAF1FB",
            text_color=BLUE,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=self.show_login
        ).pack()

    # ========================================================
    # INPUT HELPER
    # ========================================================

    def create_input(
        self,
        parent,
        label,
        placeholder,
        password=False
    ):

        ctk.CTkLabel(
            parent,
            text=label,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=TEXT
        ).pack(anchor="w")

        entry = ctk.CTkEntry(
            parent,
            height=42,
            placeholder_text=placeholder,
            fg_color=INPUT_BG,
            text_color=TEXT,
            placeholder_text_color="#94A3B8",
            border_color=BORDER,
            border_width=1,
            corner_radius=8,
            show="•" if password else ""
        )

        entry.pack(
            fill="x",
            pady=(5, 12)
        )

        return entry

    # ========================================================
    # PASSWORD TOGGLE
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

        username_or_email = self.login_username.get().strip()
        password = self.login_password.get()
        selected_role = self.login_role.get().strip().lower()

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

        if not selected_role:
            self.login_status.configure(
                text="Please select your role.",
                text_color=ERROR
            )
            return

        connection = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    username,
                    password_hash,
                    full_name,
                    email,
                    role,
                    is_active
                FROM users
                WHERE (LOWER(username) = LOWER(?) OR LOWER(email) = LOWER(?))
                  AND LOWER(role) = ?
                LIMIT 1
                """,
                (
                    username_or_email,
                    username_or_email,
                    selected_role
                )
            )

            user = cursor.fetchone()

            if user is None:
                self.login_status.configure(
                    text="Invalid credentials or incorrect account type.",
                    text_color=ERROR
                )
                return

            (
                user_id,
                username,
                stored_password,
                full_name,
                email,
                role,
                is_active
            ) = user

            if not is_active:
                self.login_status.configure(
                    text="This account has been disabled.",
                    text_color=ERROR
                )
                return

            if not verify_password(password, stored_password):
                self.login_status.configure(
                    text="Invalid username/email or password.",
                    text_color=ERROR
                )
                return

            user_data = {
                "id": user_id,
                "username": username,
                "full_name": full_name,
                "email": email,
                "role": role
            }

            # ------------------------------------------------
            # OPEN THE CORRECT DASHBOARD
            #
            # IMPORTANT:
            # Do NOT withdraw the login window until the
            # dashboard has been created successfully.
            # ------------------------------------------------

            self.current_dashboard = None

            if role.lower() == "student":

                self.current_dashboard = Dashboard(
                    user=user_data,
                    logout_callback=self.logout
                )

            elif role.lower() == "supervisor":

                from ui.supervisors_dashboard import SupervisorsDashboard

                self.current_dashboard = SupervisorsDashboard(
                    user=user_data,
                    logout_callback=self.logout
                )

            elif role.lower() == "admin":

                from ui.admin_dashboard import AdminDashboard

                self.current_dashboard = AdminDashboard(
                    user=user_data,
                    logout_callback=self.logout
                )

            else:
                self.login_status.configure(
                    text="Unknown account role.",
                    text_color=ERROR
                )
                return

            # ------------------------------------------------
            # DASHBOARD WAS CREATED SUCCESSFULLY
            # Now hide the login window.
            # ------------------------------------------------

            self.app.withdraw()

            # Some dashboards expose their actual CTk window
            # through `.window`. Make sure it is visible.
            dashboard_window = getattr(
                self.current_dashboard,
                "window",
                None
            )

            if dashboard_window is not None:
                try:
                    dashboard_window.deiconify()
                    dashboard_window.lift()
                    dashboard_window.focus_force()
                except Exception:
                    pass

        except Exception as error:

            # Never leave the user with a vanished login window.
            self.app.deiconify()
            self.app.lift()
            self.app.focus_force()

            self.login_status.configure(
                text=f"Unable to open dashboard: {error}",
                text_color=ERROR
            )

            print("=" * 60)
            print("LOGIN / DASHBOARD ERROR")
            print(repr(error))
            print("=" * 60)

        finally:

            if connection is not None:
                connection.close()

    # ========================================================
    # LOGOUT
    # ========================================================

    def logout(self):

        dashboard = self.current_dashboard

        try:
            if dashboard is not None:
                dashboard.destroy()
        except Exception:
            pass

        try:
            dashboard_window = getattr(
                dashboard,
                "window",
                None
            )

            if dashboard_window is not None:
                try:
                    dashboard_window.destroy()
                except Exception:
                    pass
        except Exception:
            pass

        self.current_dashboard = None

        try:
            self.app.deiconify()
            self.app.lift()
            self.app.focus_force()
        except Exception:
            pass

        self.show_login()

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
        # VALIDATION
        # ----------------------------------------------------

        if not full_name:

            self.signup_status.configure(
                text="Please enter your full name.",
                text_color=ERROR
            )
            return

        if not username:

            self.signup_status.configure(
                text="Please enter a username.",
                text_color=ERROR
            )
            return

        if not email:

            self.signup_status.configure(
                text="Please enter your email.",
                text_color=ERROR
            )
            return

        if not password:

            self.signup_status.configure(
                text="Please enter a password.",
                text_color=ERROR
            )
            return

        if password != confirm_password:

            self.signup_status.configure(
                text="Passwords do not match.",
                text_color=ERROR
            )
            return

        if len(password) < 6:

            self.signup_status.configure(
                text="Password must be at least 6 characters.",
                text_color=ERROR
            )
            return

        connection = None

        try:

            connection = get_connection()

            cursor = connection.cursor()

            # ------------------------------------------------
            # CHECK USERNAME
            # ------------------------------------------------

            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE username = ?
                LIMIT 1
                """,
                (username,)
            )

            if cursor.fetchone() is not None:

                self.signup_status.configure(
                    text="That username is already taken.",
                    text_color=ERROR
                )
                return

            # ------------------------------------------------
            # CHECK EMAIL
            # ------------------------------------------------

            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE email = ?
                LIMIT 1
                """,
                (email,)
            )

            if cursor.fetchone() is not None:

                self.signup_status.configure(
                    text="That email is already registered.",
                    text_color=ERROR
                )
                return

            # ------------------------------------------------
            # CREATE STUDENT ACCOUNT
            # ------------------------------------------------

            password_hash = hash_password(
                password
            )

            cursor.execute(
                """
                INSERT INTO users (
                    username,
                    password_hash,
                    full_name,
                    email,
                    role,
                    is_active
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    username,
                    password_hash,
                    full_name,
                    email,
                    "student",
                    1
                )
            )

            connection.commit()

            self.signup_status.configure(
                text=(
                    "Account created successfully! "
                    "You can now sign in as a Student."
                ),
                text_color=SUCCESS
            )

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

        except Exception as error:

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
# START APPLICATION
# ============================================================

if __name__ == "__main__":
    AuthWindow()