import customtkinter as ctk


# ============================================================
# APPLICATION SETTINGS
# ============================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


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


# ============================================================
# LOGIN WINDOW
# ============================================================

app = ctk.CTk()

app.title("SIWES Management System")

app.geometry("1200x700")
app.minsize(1000, 620)

app.configure(fg_color=WHITE)


# ============================================================
# MAIN LAYOUT
# ============================================================

app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)


# ============================================================
# LEFT BRANDING PANEL
# ============================================================

left_panel = ctk.CTkFrame(
    app,
    fg_color=NAVY,
    corner_radius=0
)

left_panel.grid(
    row=0,
    column=0,
    sticky="nsew"
)


# ------------------------------------------------------------
# Decorative background shapes
# ------------------------------------------------------------

circle_top = ctk.CTkFrame(
    left_panel,
    width=300,
    height=300,
    corner_radius=150,
    fg_color=NAVY_LIGHT
)

circle_top.place(
    x=-130,
    y=-120
)


circle_bottom = ctk.CTkFrame(
    left_panel,
    width=260,
    height=260,
    corner_radius=130,
    fg_color=NAVY_LIGHT
)

circle_bottom.place(
    x=-90,
    rely=0.68
)


# ============================================================
# BRAND CONTENT
# ============================================================

brand_container = ctk.CTkFrame(
    left_panel,
    fg_color="transparent"
)

brand_container.place(
    relx=0.5,
    rely=0.48,
    anchor="center"
)


# ------------------------------------------------------------
# SIWES icon
# ------------------------------------------------------------

icon = ctk.CTkLabel(
    brand_container,
    text="◆",
    text_color=BLUE,
    font=("Poppins", 46, "bold")
)

icon.pack(pady=(0, 12))


# ------------------------------------------------------------
# Main title
# ------------------------------------------------------------

brand_title = ctk.CTkLabel(
    brand_container,
    text="SIWES\nManagement System",
    text_color=WHITE,
    font=("Poppins", 30, "bold"),
    justify="center"
)

brand_title.pack()


# ------------------------------------------------------------
# Description
# ------------------------------------------------------------

brand_description = ctk.CTkLabel(
    brand_container,
    text="Connecting Students,\nSupervisors and Institutions",
    text_color="#D7E3F0",
    font=("Inter", 16),
    justify="center"
)

brand_description.pack(pady=(18, 0))


# ============================================================
# GROUP 29 BRANDING
# ============================================================

group_label = ctk.CTkLabel(
    left_panel,
    text="Group 29",
    text_color=WHITE,
    font=("Poppins", 15, "bold")
)

group_label.place(
    relx=0.08,
    rely=0.93
)


# ============================================================
# RIGHT LOGIN PANEL
# ============================================================

right_panel = ctk.CTkFrame(
    app,
    fg_color=WHITE,
    corner_radius=0
)

right_panel.grid(
    row=0,
    column=1,
    sticky="nsew"
)


# ============================================================
# LOGIN CONTENT
# ============================================================

login_container = ctk.CTkFrame(
    right_panel,
    fg_color="transparent"
)

login_container.place(
    relx=0.5,
    rely=0.50,
    anchor="center"
)


# ============================================================
# HEADING
# ============================================================

welcome_label = ctk.CTkLabel(
    login_container,
    text="Welcome Back",
    text_color=TEXT,
    font=("Poppins", 32, "bold")
)

welcome_label.pack(
    anchor="w"
)


subtitle_label = ctk.CTkLabel(
    login_container,
    text="Sign in to your account",
    text_color=TEXT_LIGHT,
    font=("Inter", 16)
)

subtitle_label.pack(
    anchor="w",
    pady=(4, 38)
)


# ============================================================
# USERNAME LABEL
# ============================================================

username_label = ctk.CTkLabel(
    login_container,
    text="Username or Email",
    text_color=TEXT,
    font=("Inter", 15, "bold")
)

username_label.pack(
    anchor="w"
)


# ============================================================
# USERNAME INPUT
# ============================================================

username_entry = ctk.CTkEntry(
    login_container,
    width=500,
    height=58,
    placeholder_text="Enter your username or email",
    placeholder_text_color="#94A3B8",
    fg_color=INPUT_BG,
    border_color=BORDER,
    border_width=1,
    corner_radius=10,
    text_color=TEXT,
    font=("Inter", 15)
)

username_entry.pack(
    pady=(9, 25)
)


# ============================================================
# PASSWORD LABEL
# ============================================================

password_label = ctk.CTkLabel(
    login_container,
    text="Password",
    text_color=TEXT,
    font=("Inter", 15, "bold")
)

password_label.pack(
    anchor="w"
)


# ============================================================
# PASSWORD FRAME
# ============================================================

password_frame = ctk.CTkFrame(
    login_container,
    width=500,
    height=58,
    fg_color=INPUT_BG,
    corner_radius=10,
    border_width=1,
    border_color=BORDER
)

password_frame.pack(
    pady=(9, 18)
)

password_frame.pack_propagate(False)


# ============================================================
# PASSWORD ENTRY
# ============================================================

password_entry = ctk.CTkEntry(
    password_frame,
    placeholder_text="Enter your password",
    show="•",
    fg_color="transparent",
    border_width=0,
    text_color=TEXT,
    placeholder_text_color="#94A3B8",
    font=("Inter", 15)
)

password_entry.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(14, 5)
)


# ============================================================
# PASSWORD VISIBILITY
# ============================================================

password_visible = False


def toggle_password():
    global password_visible

    if password_visible:
        password_entry.configure(show="•")
        eye_button.configure(text="◉")
        password_visible = False

    else:
        password_entry.configure(show="")
        eye_button.configure(text="◉")
        password_visible = True


eye_button = ctk.CTkButton(
    password_frame,
    text="◉",
    width=45,
    height=40,
    fg_color="transparent",
    hover_color="#E8EEF6",
    text_color=TEXT_LIGHT,
    font=("Inter", 15),
    command=toggle_password
)

eye_button.pack(
    side="right",
    padx=5
)


# ============================================================
# OPTIONS ROW
# ============================================================

options_frame = ctk.CTkFrame(
    login_container,
    fg_color="transparent"
)

options_frame.pack(
    fill="x",
    pady=(0, 35)
)


# ------------------------------------------------------------
# Remember me
# ------------------------------------------------------------

remember_var = ctk.BooleanVar(value=False)

remember_checkbox = ctk.CTkCheckBox(
    options_frame,
    text="Remember me",
    variable=remember_var,
    text_color=TEXT_LIGHT,
    fg_color=BLUE,
    hover_color=BLUE_HOVER,
    border_color="#AAB7C6",
    font=("Inter", 14)
)

remember_checkbox.pack(
    side="left"
)


# ------------------------------------------------------------
# Forgot password
# ------------------------------------------------------------

def forgot_password():
    status_label.configure(
        text="Please contact the administrator to reset your password.",
        text_color=TEXT_LIGHT
    )


forgot_button = ctk.CTkButton(
    options_frame,
    text="Forgot password?",
    width=130,
    fg_color="transparent",
    hover_color="#EEF4FC",
    text_color=BLUE,
    font=("Inter", 14, "bold"),
    command=forgot_password
)

forgot_button.pack(
    side="right"
)


# ============================================================
# LOGIN BUTTON
# ============================================================

def login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:

        status_label.configure(
            text="Please enter your username/email and password.",
            text_color="#D14343"
        )

        return

    status_label.configure(
        text="Login system is ready for database authentication.",
        text_color="#2E8B57"
    )


login_button = ctk.CTkButton(
    login_container,
    text="Sign In",
    width=500,
    height=58,
    corner_radius=10,
    fg_color=BLUE,
    hover_color=BLUE_HOVER,
    text_color=WHITE,
    font=("Poppins", 16, "bold"),
    command=login
)

login_button.pack()


# ============================================================
# STATUS MESSAGE
# ============================================================

status_label = ctk.CTkLabel(
    login_container,
    text="",
    text_color=TEXT_LIGHT,
    font=("Inter", 13),
    wraplength=480
)

status_label.pack(
    pady=(18, 0)
)


# ============================================================
# KEYBOARD SUPPORT
# ============================================================

password_entry.bind(
    "<Return>",
    lambda event: login()
)

username_entry.bind(
    "<Return>",
    lambda event: password_entry.focus()
)


# ============================================================
# START APPLICATION
# ============================================================

app.mainloop()