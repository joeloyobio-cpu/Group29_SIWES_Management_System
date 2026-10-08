import customtkinter as ctk

from database.database import setup_database

from ui.animations import (
    animate_width,
    add_hover_effect,
    add_press_effect
)

from ui.pages.student_info import StudentInfoPage
from ui.pages.logbook import LogbookPage
from ui.pages.attendance import AttendancePage
from ui.pages.placement import PlacementPage
from ui.pages.evaluation import EvaluationPage


# ============================================================
# COLORS
# ============================================================

NAVY = "#102F4F"
NAVY_LIGHT = "#163D62"

BLUE = "#2F7DF6"
BLUE_HOVER = "#2469D8"

WHITE = "#FFFFFF"

BACKGROUND = "#F4F7FB"

TEXT = "#102F4F"
TEXT_LIGHT = "#64748B"

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

        self.app.configure(
            fg_color=BACKGROUND
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

        self.sidebar.configure(
            width=0
        )

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
            height=40,
            fg_color=ERROR,
            hover_color="#B91C1C",
            text_color=WHITE,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=self.logout
        )

        logout_button.pack(
            side="bottom",
            padx=20,
            pady=25,
            fill="x"
        )

        add_press_effect(
            logout_button,
            ERROR,
            "#991B1B"
        )

        self.app.after(
            100,
            lambda: animate_width(
                self.sidebar,
                0,
                240,
                duration=500,
                steps=28
            )
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
                text_color=WHITE,
                anchor="w",
                font=ctk.CTkFont(
                    size=13
                ),
                command=lambda name=item:
                    self.show_page(name)
            )

            button.pack(
                padx=15,
                pady=3,
                fill="x"
            )

            add_hover_effect(
                button,
                "transparent",
                NAVY_LIGHT
            )

    # ========================================================
    # MAIN AREA
    # ========================================================

    def create_main_area(self):

        self.main_area = ctk.CTkFrame(
            self.app,
            fg_color=BACKGROUND,
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

        # ----------------------------------------------------
        # STUDENT INFORMATION
        # ----------------------------------------------------

        if page_name == "My Information":

            page = StudentInfoPage(
                self.main_area,
                self.user
            )

            page.pack(
                fill="both",
                expand=True
            )

            return

        # ----------------------------------------------------
        # PLACEMENT
        # ----------------------------------------------------

        if page_name == "Placement":

            page = PlacementPage(
                self.main_area,
                self.user
            )

            page.pack(
                fill="both",
                expand=True
            )

            return

        # ----------------------------------------------------
        # DIGITAL LOGBOOK
        # ----------------------------------------------------

        if page_name == "Digital Logbook":

            page = LogbookPage(
                self.main_area,
                self.user
            )

            page.pack(
                fill="both",
                expand=True
            )

            return

        # ----------------------------------------------------
        # ATTENDANCE
        # ----------------------------------------------------

        if page_name == "Attendance":

            page = AttendancePage(
                self.main_area,
                self.user
            )

            page.pack(
                fill="both",
                expand=True
            )

            return

        # ----------------------------------------------------
        # EVALUATION / SUPERVISOR FEEDBACK
        # ----------------------------------------------------

        if page_name == "Evaluation":

            page = EvaluationPage(
                self.main_area,
                self.user
            )

            page.pack(
                fill="both",
                expand=True
            )

            return

        # ----------------------------------------------------
        # DASHBOARD
        # ----------------------------------------------------

        if page_name == "Dashboard":

            self.show_dashboard_home()

            return

        # ----------------------------------------------------
        # OTHER MODULES
        # ----------------------------------------------------

        self.show_placeholder(
            page_name
        )

    # ========================================================
    # DASHBOARD HOME
    # ========================================================

    def show_dashboard_home(self):

        header = ctk.CTkFrame(
            self.main_area,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=40,
            pady=(35, 20)
        )

        title = ctk.CTkLabel(
            header,
            text="Dashboard",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            ),
            text_color=TEXT
        )

        title.pack(
            anchor="w"
        )

        welcome = ctk.CTkLabel(
            header,
            text=(
                f"Welcome back, "
                f"{self.user.get('full_name', 'User')}!"
            ),
            font=ctk.CTkFont(
                size=15
            ),
            text_color=TEXT_LIGHT
        )

        welcome.pack(
            anchor="w",
            pady=(5, 0)
        )

        stats = ctk.CTkFrame(
            self.main_area,
            fg_color="transparent"
        )

        stats.pack(
            fill="x",
            padx=40,
            pady=(0, 20)
        )

        for column in range(3):

            stats.grid_columnconfigure(
                column,
                weight=1
            )

        self.create_stat_card(
            stats,
            0,
            "SIWES Status",
            "Active",
            SUCCESS
        )

        self.create_stat_card(
            stats,
            1,
            "Attendance",
            "—",
            BLUE
        )

        self.create_stat_card(
            stats,
            2,
            "Logbook",
            "—",
            "#8B5CF6"
        )

        card = ctk.CTkFrame(
            self.main_area,
            fg_color=WHITE,
            corner_radius=12,
            border_width=1,
            border_color=BORDER
        )

        card.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=(0, 40)
        )

        card_title = ctk.CTkLabel(
            card,
            text="SIWES Management System",
            font=ctk.CTkFont(
                size=21,
                weight="bold"
            ),
            text_color=TEXT
        )

        card_title.pack(
            anchor="w",
            padx=30,
            pady=(30, 5)
        )

        card_description = ctk.CTkLabel(
            card,
            text=(
                "Use the navigation menu to manage "
                "your SIWES activities, placement, "
                "attendance, logbook and evaluation."
            ),
            font=ctk.CTkFont(
                size=14
            ),
            text_color=TEXT_LIGHT,
            justify="left"
        )

        card_description.pack(
            anchor="w",
            padx=30,
            pady=(0, 25)
        )

        actions = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        actions.pack(
            fill="x",
            padx=30
        )

        role = str(
            self.user.get(
                "role",
                "student"
            )
        ).lower()

        if role == "student":

            self.create_action_button(
                actions,
                "My Information",
                lambda: self.show_page(
                    "My Information"
                )
            )

            self.create_action_button(
                actions,
                "Placement",
                lambda: self.show_page(
                    "Placement"
                )
            )

            self.create_action_button(
                actions,
                "Attendance",
                lambda: self.show_page(
                    "Attendance"
                )
            )

            self.create_action_button(
                actions,
                "Digital Logbook",
                lambda: self.show_page(
                    "Digital Logbook"
                )
            )

            self.create_action_button(
                actions,
                "Evaluation",
                lambda: self.show_page(
                    "Evaluation"
                )
            )

    # ========================================================
    # STAT CARD
    # ========================================================

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
            padx=6
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=TEXT_LIGHT
        )

        title_label.pack(
            anchor="w",
            padx=20,
            pady=(18, 2)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            ),
            text_color=value_color
        )

        value_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 18)
        )

    # ========================================================
    # QUICK ACTION BUTTON
    # ========================================================

    def create_action_button(
        self,
        parent,
        text,
        command
    ):

        button = ctk.CTkButton(
            parent,
            text=text,
            width=160,
            height=42,
            corner_radius=8,
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
            text_color=WHITE,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=command
        )

        button.pack(
            side="left",
            padx=(0, 10)
        )

        add_press_effect(
            button,
            BLUE,
            "#1D4ED8"
        )

    # ========================================================
    # PLACEHOLDER
    # ========================================================

    def show_placeholder(
        self,
        page_name
    ):

        header = ctk.CTkFrame(
            self.main_area,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=40,
            pady=(35, 20)
        )

        title = ctk.CTkLabel(
            header,
            text=page_name,
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            ),
            text_color=TEXT
        )

        title.pack(
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            header,
            text=(
                f"{page_name} management module."
            ),
            font=ctk.CTkFont(
                size=14
            ),
            text_color=TEXT_LIGHT
        )

        subtitle.pack(
            anchor="w",
            pady=(5, 0)
        )

        card = ctk.CTkFrame(
            self.main_area,
            fg_color=WHITE,
            corner_radius=12,
            border_width=1,
            border_color=BORDER
        )

        card.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=(0, 40)
        )

        icon = ctk.CTkLabel(
            card,
            text="⚙",
            font=ctk.CTkFont(
                size=42
            ),
            text_color=BLUE
        )

        icon.pack(
            pady=(80, 15)
        )

        message = ctk.CTkLabel(
            card,
            text=(
                f"{page_name} module "
                "is ready to be connected."
            ),
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color=TEXT
        )

        message.pack(
            pady=5
        )

        description = ctk.CTkLabel(
            card,
            text=(
                "This page will be connected "
                "to the corresponding module."
            ),
            font=ctk.CTkFont(
                size=13
            ),
            text_color=TEXT_LIGHT
        )

        description.pack(
            pady=5
        )

    # ========================================================
    # LOGOUT
    # ========================================================

    def logout(self):

        if self.app.winfo_exists():

            self.app.destroy()

        if self.logout_callback:

            self.logout_callback()


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_user = {
        "id": 1,
        "username": "test",
        "full_name": "Test Student",
        "role": "student",
        "email": "student@test.com"
    }

    dashboard = Dashboard(
        test_user
    )

    dashboard.app.mainloop()