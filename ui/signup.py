import customtkinter as ctk
import subprocess
import sys
from pathlib import Path


# ============================================================
# COLORS
# ============================================================

NAVY = "#102F4F"
NAVY_DARK = "#08233D"
NAVY_LIGHT = "#163D62"

BLUE = "#2F7DF6"
BLUE_HOVER = "#2469D8"

WHITE = "#FFFFFF"
TEXT = "#102F4F"
TEXT_LIGHT = "#64748B"

INPUT_BG = "#F4F7FB"
BORDER = "#DCE4EE"

LIGHT_BLUE = "#DCEBFF"
ERROR = "#D9534F"


# ============================================================
# APPEARANCE
# ============================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# ============================================================
# NAVIGATION
# ============================================================

def open_login():
    """Open the login page and close signup."""

    login_file = Path(__file__).resolve().parent / "login.py"

    subprocess.Popen([
        sys.executable,
        str(login_file)
    ])

    app.destroy()


# ============================================================
# PASSWORD VISIBILITY
# ============================================================

def toggle_password():

    if password_entry.cget("show") == "":
        password_entry.configure(show="●")
        password_toggle.configure(text="◉")
    else:
        password_entry.configure(show="")
        password_toggle.configure(text="○")


def toggle_confirm_password():

    if confirm_entry.cget("show") == "":
        confirm_entry.configure(show="●")
        confirm_toggle.configure(text="◉")
    else:
        confirm_entry.configure(show="")
        confirm_toggle.configure(text="○")


# ============================================================
# MAIN WINDOW
# ============================================================

app = ctk.CTk()

app.title("SIWES Management System")

app.geometry("1200x700")

app.minsize(1000, 620)

app.configure(
    fg_color=WHITE
)


# ============================================================
# LEFT BRANDING PANEL
# ============================================================

left_panel = ctk.CTkFrame(
    app,
    width=450,
    corner_radius=0,
    fg_color=NAVY
)

left_panel.pack(
    side="left",
    fill="y"
)

left_panel.pack_propagate(False)


# ============================================================
# DECORATIVE CIRCLES
# ============================================================

circle_top = ctk.CTkFrame(
    left_panel,
    width=250,
    height=250,
    corner_radius=125,
    fg_color=NAVY_LIGHT
)

circle_top.place(
    x=-150,
    y=-150
)


circle_bottom = ctk.CTkFrame(
    left_panel,
    width=230,
    height=230,
    corner_radius=115,
    fg_color=NAVY_LIGHT
)

circle_bottom.place(
    x=300,
    y=535
)


# ============================================================
# LOGO AREA
# ============================================================

logo_canvas = ctk.CTkCanvas(
    left_panel,
    width=150,
    height=125,
    bg=NAVY,
    highlightthickness=0
)

logo_canvas.place(
    x=55,
    y=60
)


# Logo: graduation cap

logo_canvas.create_polygon(
    20, 42,
    75, 15,
    130, 42,
    75, 69,
    fill=WHITE,
    outline=WHITE
)

# Cap base

logo_canvas.create_polygon(
    45, 55,
    105, 55,
    105, 82,
    75, 98,
    45, 82,
    fill=WHITE,
    outline=WHITE
)

# Cap tassel

logo_canvas.create_line(
    130, 42,
    130, 78,
    fill=WHITE,
    width=3
)

logo_canvas.create_oval(
    126, 76,
    134, 84,
    fill=BLUE,
    outline=BLUE
)

# Small blue diamond

logo_canvas.create_polygon(
    75, 30,
    86, 42,
    75, 54,
    64, 42,
    fill=BLUE,
    outline=BLUE
)


# ============================================================
# BRAND TITLE
# ============================================================

brand_title = ctk.CTkLabel(
    left_panel,
    text="SIWES",
    text_color=WHITE,
    font=("Poppins", 39, "bold")
)

brand_title.place(
    x=45,
    y=185
)


brand_subtitle = ctk.CTkLabel(
    left_panel,
    text="Management System",
    text_color=WHITE,
    font=("Poppins", 25, "bold")
)

brand_subtitle.place(
    x=45,
    y=235
)


# ============================================================
# BLUE DIVIDER
# ============================================================

divider = ctk.CTkFrame(
    left_panel,
    width=320,
    height=2,
    fg_color="#42698F"
)

divider.place(
    x=45,
    y=290
)


divider_blue = ctk.CTkFrame(
    left_panel,
    width=75,
    height=4,
    fg_color=BLUE
)

divider_blue.place(
    x=165,
    y=289
)


# ============================================================
# MOTTO
# ============================================================

motto = ctk.CTkLabel(
    left_panel,
    text="...Connecting students,\nsupervisors and institutions\nfor a brighter future.",
    text_color="#E2ECF5",
    justify="center",
    font=("Inter", 15)
)

motto.place(
    relx=0.5,
    y=325,
    anchor="n"
)


# ============================================================
# THREE SERVICE AREAS
# ============================================================

# Students

student_icon = ctk.CTkLabel(
    left_panel,
    text="♙",
    text_color=WHITE,
    font=("Arial", 28)
)

student_icon.place(
    x=72,
    y=440
)

student_title = ctk.CTkLabel(
    left_panel,
    text="Students",
    text_color=WHITE,
    font=("Poppins", 12, "bold")
)

student_title.place(
    x=62,
    y=480
)

student_subtitle = ctk.CTkLabel(
    left_panel,
    text="Learn",
    text_color="#9EB6CC",
    font=("Inter", 11)
)

student_subtitle.place(
    x=76,
    y=505
)


# Separator

separator1 = ctk.CTkFrame(
    left_panel,
    width=1,
    height=80,
    fg_color="#42698F"
)

separator1.place(
    x=150,
    y=435
)


# Supervisors

supervisor_icon = ctk.CTkLabel(
    left_panel,
    text="♢",
    text_color=WHITE,
    font=("Arial", 32, "bold")
)

supervisor_icon.place(
    x=215,
    y=438
)

supervisor_title = ctk.CTkLabel(
    left_panel,
    text="Supervisors",
    text_color=WHITE,
    font=("Poppins", 12, "bold")
)

supervisor_title.place(
    x=195,
    y=480
)

supervisor_subtitle = ctk.CTkLabel(
    left_panel,
    text="Guide",
    text_color="#9EB6CC",
    font=("Inter", 11)
)

supervisor_subtitle.place(
    x=225,
    y=505
)


# Separator

separator2 = ctk.CTkFrame(
    left_panel,
    width=1,
    height=80,
    fg_color="#42698F"
)

separator2.place(
    x=300,
    y=435
)


# Institutions

institution_icon = ctk.CTkLabel(
    left_panel,
    text="⌂",
    text_color=WHITE,
    font=("Arial", 31, "bold")
)

institution_icon.place(
    x=355,
    y=438
)

institution_title = ctk.CTkLabel(
    left_panel,
    text="Institutions",
    text_color=WHITE,
    font=("Poppins", 12, "bold")
)

institution_title.place(
    x=335,
    y=480
)

institution_subtitle = ctk.CTkLabel(
    left_panel,
    text="Grow",
    text_color="#9EB6CC",
    font=("Inter", 11)
)

institution_subtitle.place(
    x=360,
    y=505
)


# ============================================================
# BOTTOM MESSAGE
# ============================================================

bottom_line = ctk.CTkFrame(
    left_panel,
    width=35,
    height=3,
    fg_color=BLUE
)

bottom_line.place(
    x=45,
    y=585
)


bottom_text = ctk.CTkLabel(
    left_panel,
    text="PRACTICAL EXPERIENCE.\nREAL OPPORTUNITIES.",
    text_color="#D8E4F0",
    justify="left",
    font=("Inter", 10, "bold")
)

bottom_text.place(
    x=95,
    y=575
)


# ============================================================
# RIGHT PANEL
# ============================================================

right_panel = ctk.CTkFrame(
    app,
    corner_radius=0,
    fg_color=WHITE
)

right_panel.pack(
    side="right",
    fill="both",
    expand=True
)


# ============================================================
# FORM
# ============================================================

form = ctk.CTkFrame(
    right_panel,
    fg_color=WHITE
)

form.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)


# ============================================================
# HEADING
# ============================================================

heading = ctk.CTkLabel(
    form,
    text="Create Your Account",
    text_color=TEXT,
    font=("Poppins", 27, "bold")
)

heading.pack(
    anchor="w"
)


subtitle = ctk.CTkLabel(
    form,
    text="Join the SIWES Management System and be part of a connected learning experience.",
    text_color=TEXT_LIGHT,
    font=("Inter", 12)
)

subtitle.pack(
    anchor="w",
    pady=(5, 20)
)


# ============================================================
# FULL NAME
# ============================================================

name_label = ctk.CTkLabel(
    form,
    text="Full Name",
    text_color=TEXT,
    font=("Inter", 13, "bold")
)

name_label.pack(
    anchor="w",
    pady=(0, 5)
)


name_entry = ctk.CTkEntry(
    form,
    width=500,
    height=43,
    placeholder_text="Enter your full name",
    fg_color=INPUT_BG,
    border_color=BORDER,
    text_color=TEXT,
    corner_radius=8
)

name_entry.pack(
    pady=(0, 12)
)


# ============================================================
# USERNAME
# ============================================================

username_label = ctk.CTkLabel(
    form,
    text="Username",
    text_color=TEXT,
    font=("Inter", 13, "bold")
)

username_label.pack(
    anchor="w",
    pady=(0, 5)
)


username_entry = ctk.CTkEntry(
    form,
    width=500,
    height=43,
    placeholder_text="Choose a username",
    fg_color=INPUT_BG,
    border_color=BORDER,
    text_color=TEXT,
    corner_radius=8
)

username_entry.pack(
    pady=(0, 12)
)


# ============================================================
# EMAIL
# ============================================================

email_label = ctk.CTkLabel(
    form,
    text="Email Address",
    text_color=TEXT,
    font=("Inter", 13, "bold")
)

email_label.pack(
    anchor="w",
    pady=(0, 5)
)


email_entry = ctk.CTkEntry(
    form,
    width=500,
    height=43,
    placeholder_text="Enter your email address",
    fg_color=INPUT_BG,
    border_color=BORDER,
    text_color=TEXT,
    corner_radius=8
)

email_entry.pack(
    pady=(0, 12)
)


# ============================================================
# PASSWORD
# ============================================================

password_label = ctk.CTkLabel(
    form,
    text="Password",
    text_color=TEXT,
    font=("Inter", 13, "bold")
)

password_label.pack(
    anchor="w",
    pady=(0, 5)
)


password_frame = ctk.CTkFrame(
    form,
    width=500,
    height=43,
    fg_color=INPUT_BG,
    border_color=BORDER,
    border_width=1,
    corner_radius=8
)

password_frame.pack(
    pady=(0, 12)
)

password_frame.pack_propagate(False)


password_entry = ctk.CTkEntry(
    password_frame,
    width=440,
    height=40,
    placeholder_text="Create a password",
    show="●",
    fg_color="transparent",
    border_width=0,
    text_color=TEXT
)

password_entry.pack(
    side="left",
    padx=(8, 0)
)


password_toggle = ctk.CTkButton(
    password_frame,
    text="◉",
    width=35,
    height=35,
    fg_color="transparent",
    hover_color="#E8EEF7",
    text_color=TEXT_LIGHT,
    command=toggle_password
)

password_toggle.pack(
    side="right",
    padx=3
)


# ============================================================
# CONFIRM PASSWORD
# ============================================================

confirm_label = ctk.CTkLabel(
    form,
    text="Confirm Password",
    text_color=TEXT,
    font=("Inter", 13, "bold")
)

confirm_label.pack(
    anchor="w",
    pady=(0, 5)
)


confirm_frame = ctk.CTkFrame(
    form,
    width=500,
    height=43,
    fg_color=INPUT_BG,
    border_color=BORDER,
    border_width=1,
    corner_radius=8
)

confirm_frame.pack(
    pady=(0, 18)
)

confirm_frame.pack_propagate(False)


confirm_entry = ctk.CTkEntry(
    confirm_frame,
    width=440,
    height=40,
    placeholder_text="Confirm your password",
    show="●",
    fg_color="transparent",
    border_width=0,
    text_color=TEXT
)

confirm_entry.pack(
    side="left",
    padx=(8, 0)
)


confirm_toggle = ctk.CTkButton(
    confirm_frame,
    text="◉",
    width=35,
    height=35,
    fg_color="transparent",
    hover_color="#E8EEF7",
    text_color=TEXT_LIGHT,
    command=toggle_confirm_password
)

confirm_toggle.pack(
    side="right",
    padx=3
)


# ============================================================
# CREATE ACCOUNT
# ============================================================

create_button = ctk.CTkButton(
    form,
    text="Create Account     →",
    width=500,
    height=48,
    corner_radius=8,
    fg_color=BLUE,
    hover_color=BLUE_HOVER,
    font=("Poppins", 14, "bold")
)

create_button.pack()


# ============================================================
# SIGN IN
# ============================================================

signin_frame = ctk.CTkFrame(
    form,
    fg_color="transparent"
)

signin_frame.pack(
    pady=(15, 0)
)


signin_text = ctk.CTkLabel(
    signin_frame,
    text="Already have an account?",
    text_color=TEXT_LIGHT,
    font=("Inter", 12)
)

signin_text.pack(
    side="left"
)


signin_button = ctk.CTkButton(
    signin_frame,
    text="Sign In",
    width=60,
    height=25,
    fg_color="transparent",
    hover_color="#EAF2FF",
    text_color=BLUE,
    font=("Inter", 12, "bold"),
    command=open_login
)

signin_button.pack(
    side="left",
    padx=(4, 0)
)


# ============================================================
# STATUS
# ============================================================

status_label = ctk.CTkLabel(
    form,
    text="",
    text_color=ERROR,
    font=("Inter", 11)
)

status_label.pack(
    pady=(5, 0)
)


# ============================================================
# START
# ============================================================

app.mainloop()