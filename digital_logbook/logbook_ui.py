import sys
from pathlib import Path
from datetime import datetime

import customtkinter as ctk
from tkinter import ttk, messagebox


# ---------------------------------------------------------
# Make the teammate's existing digital_logbook modules
# importable without changing his database.py yet.
# ---------------------------------------------------------
PACKAGE_DIR = Path(__file__).resolve().parent

if str(PACKAGE_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGE_DIR))

from .logbook import LogbookEntry

from .database import (
    save_entry,
    entry_exists,
    get_entries,
    search_entries,
    filter_entries,
    update_entry,
    delete_entry,
    update_entry_status
)


# ---------------------------------------------------------
# THEME
# ---------------------------------------------------------

NAVY = "#0F172A"
BLUE = "#2563EB"
BLUE_HOVER = "#1D4ED8"
LIGHT_BLUE = "#EFF6FF"

WHITE = "#FFFFFF"
BACKGROUND = "#F8FAFC"
CARD = "#FFFFFF"
BORDER = "#E2E8F0"

TEXT = "#0F172A"
MUTED = "#64748B"

GREEN = "#16A34A"
GREEN_BG = "#DCFCE7"

ORANGE = "#D97706"
ORANGE_BG = "#FEF3C7"

RED = "#DC2626"
RED_BG = "#FEE2E2"

PURPLE = "#7C3AED"
PURPLE_BG = "#EDE9FE"


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class DigitalLogbook(ctk.CTkFrame):
    """
    Modern Digital Logbook UI.

    The existing teammate database functions are intentionally reused.
    This file only replaces the presentation/UI layer.

    student_id can be supplied by the main dashboard later.
    """

    def __init__(self, parent, student_id=1023, **kwargs):
        super().__init__(
            parent,
            fg_color=BACKGROUND,
            **kwargs
        )

        self.student_id = student_id
        self.editing_entry = None

        self.build_ui()
        self.load_entries()

    # =====================================================
    # MAIN UI
    # =====================================================

    def build_ui(self):
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.build_header()
        self.build_summary_cards()
        self.build_content()

    # =====================================================
    # HEADER
    # =====================================================

    def build_header(self):
        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=28,
            pady=(24, 10)
        )

        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header,
            text="Digital Logbook",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            ),
            text_color=TEXT
        )

        title.grid(
            row=0,
            column=0,
            sticky="w"
        )

        subtitle = ctk.CTkLabel(
            header,
            text="Record and manage your daily SIWES activities and learning progress.",
            font=ctk.CTkFont(size=13),
            text_color=MUTED
        )

        subtitle.grid(
            row=1,
            column=0,
            sticky="w",
            pady=(4, 0)
        )

        new_button = ctk.CTkButton(
            header,
            text="+  New Entry",
            width=145,
            height=42,
            corner_radius=8,
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=self.reset_form
        )

        new_button.grid(
            row=0,
            column=1,
            rowspan=2,
            padx=(20, 0)
        )

    # =====================================================
    # SUMMARY CARDS
    # =====================================================

    def build_summary_cards(self):
        cards = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        cards.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=28,
            pady=(5, 18)
        )

        for i in range(4):
            cards.grid_columnconfigure(
                i,
                weight=1
            )

        self.total_value = self.create_summary_card(
            cards,
            0,
            "Total Entries",
            "0",
            BLUE,
            LIGHT_BLUE
        )

        self.pending_value = self.create_summary_card(
            cards,
            1,
            "Pending",
            "0",
            ORANGE,
            ORANGE_BG
        )

        self.approved_value = self.create_summary_card(
            cards,
            2,
            "Approved",
            "0",
            GREEN,
            GREEN_BG
        )

        self.rejected_value = self.create_summary_card(
            cards,
            3,
            "Rejected",
            "0",
            RED,
            RED_BG
        )

    def create_summary_card(
        self,
        parent,
        column,
        title,
        value,
        accent,
        background
    ):
        card = ctk.CTkFrame(
            parent,
            fg_color=CARD,
            border_width=1,
            border_color=BORDER,
            corner_radius=12
        )

        card.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=5
        )

        card.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=12),
            text_color=MUTED
        )

        title_label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=18,
            pady=(15, 0)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            ),
            text_color=accent
        )

        value_label.grid(
            row=1,
            column=0,
            sticky="w",
            padx=18,
            pady=(2, 15)
        )

        return value_label

    # =====================================================
    # CONTENT
    # =====================================================

    def build_content(self):
        content = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color="#CBD5E1",
            scrollbar_button_hover_color="#94A3B8"
        )

        content.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=28,
            pady=(0, 25)
        )

        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)

        # Main card
        card = ctk.CTkFrame(
            content,
            fg_color=CARD,
            border_width=1,
            border_color=BORDER,
            corner_radius=12
        )

        card.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        card.grid_rowconfigure(2, weight=1)
        card.grid_columnconfigure(0, weight=1)

        self.build_form(card)
        self.build_filters(card)
        self.build_table(card)
        self.build_actions(card)

    # =====================================================
    # FORM
    # =====================================================

    def build_form(self, parent):
        form = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        form.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=22,
            pady=(20, 12)
        )

        form.grid_columnconfigure(0, weight=1)
        form.grid_columnconfigure(1, weight=1)

        self.form_title = ctk.CTkLabel(
            form,
            text="New Logbook Entry",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color=TEXT
        )

        self.form_title.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w"
        )

        self.form_subtitle = ctk.CTkLabel(
            form,
            text="Record your daily SIWES activities and learning progress.",
            font=ctk.CTkFont(size=12),
            text_color=MUTED
        )

        self.form_subtitle.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(3, 15)
        )

        # Date
        date_label = ctk.CTkLabel(
            form,
            text="Date",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=TEXT
        )

        date_label.grid(
            row=2,
            column=0,
            sticky="w",
            pady=(0, 5)
        )

        self.date_entry = ctk.CTkEntry(
            form,
            height=40,
            placeholder_text="DD/MM/YYYY",
            fg_color=WHITE,
            text_color=TEXT,
            placeholder_text_color="#94A3B8",
            border_color=BORDER,
            border_width=1,
            corner_radius=8
        )

        self.date_entry.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=(0, 8)
        )

        today_button = ctk.CTkButton(
            form,
            text="Today",
            width=70,
            height=40,
            corner_radius=8,
            fg_color="#64748B",
            hover_color="#475569",
            command=self.set_today
        )

        today_button.grid(
            row=3,
            column=0,
            sticky="e",
            padx=(0, 12)
        )

        # Week
        week_label = ctk.CTkLabel(
            form,
            text="Week Number",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=TEXT
        )

        week_label.grid(
            row=2,
            column=1,
            sticky="w",
            pady=(0, 5),
            padx=(8, 0)
        )

        self.week_entry = ctk.CTkEntry(
            form,
            height=40,
            placeholder_text="e.g. 1",
            fg_color=WHITE,
            text_color=TEXT,
            placeholder_text_color="#94A3B8",
            border_color=BORDER,
            border_width=1,
            corner_radius=8
        )

        self.week_entry.grid(
            row=3,
            column=1,
            sticky="ew",
            padx=(8, 0)
        )

        # Activities
        activities_label = ctk.CTkLabel(
            form,
            text="Activities",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=TEXT
        )

        activities_label.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(15, 5)
        )

        self.activities_text = ctk.CTkTextbox(
            form,
            height=85,
            fg_color=WHITE,
            text_color=TEXT,
            border_color=BORDER,
            border_width=1,
            corner_radius=8
        )

        self.activities_text.grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        # Skills
        skills_label = ctk.CTkLabel(
            form,
            text="Skills Learned",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=TEXT
        )

        skills_label.grid(
            row=6,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(12, 5)
        )

        self.skills_entry = ctk.CTkEntry(
            form,
            height=40,
            placeholder_text="What did you learn today?",
            fg_color=WHITE,
            text_color=TEXT,
            placeholder_text_color="#94A3B8",
            border_color=BORDER,
            border_width=1,
            corner_radius=8
        )

        self.skills_entry.grid(
            row=7,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        # Challenges
        challenges_label = ctk.CTkLabel(
            form,
            text="Challenges",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=TEXT
        )

        challenges_label.grid(
            row=8,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(12, 5)
        )

        self.challenges_text = ctk.CTkTextbox(
            form,
            height=70,
            fg_color=WHITE,
            text_color=TEXT,
            border_color=BORDER,
            border_width=1,
            corner_radius=8
        )

        self.challenges_text.grid(
            row=9,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        # Form buttons
        buttons = ctk.CTkFrame(
            form,
            fg_color="transparent"
        )

        buttons.grid(
            row=10,
            column=0,
            columnspan=2,
            sticky="e",
            pady=(14, 0)
        )

        self.save_button = ctk.CTkButton(
            buttons,
            text="Save Entry",
            width=125,
            height=40,
            corner_radius=8,
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            command=self.save_logbook_entry
        )

        self.save_button.pack(
            side="left",
            padx=(0, 8)
        )

        self.new_button = ctk.CTkButton(
            buttons,
            text="Clear",
            width=100,
            height=40,
            corner_radius=8,
            fg_color="#64748B",
            hover_color="#475569",
            command=self.reset_form
        )

        self.new_button.pack(
            side="left"
        )

    # =====================================================
    # FILTERS
    # =====================================================

    def build_filters(self, parent):
        filters = ctk.CTkFrame(
            parent,
            fg_color=BACKGROUND,
            corner_radius=10
        )

        filters.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=22,
            pady=(8, 12)
        )

        filters.grid_columnconfigure(
            0,
            weight=1
        )

        self.search_entry = ctk.CTkEntry(
            filters,
            height=38,
            placeholder_text="Search activities, skills or challenges...",
            fg_color=WHITE,
            text_color=TEXT,
            placeholder_text_color="#94A3B8",
            border_color=BORDER,
            border_width=1,
            corner_radius=8
        )

        self.search_entry.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=10
        )

        self.week_filter = ctk.CTkComboBox(
            filters,
            values=["All"],
            width=120,
            height=38,
            state="readonly",
            fg_color=WHITE,
            border_color=BORDER,
            button_color=BLUE,
            button_hover_color=BLUE_HOVER,
            text_color=TEXT
        )

        self.week_filter.set("All")

        self.week_filter.grid(
            row=0,
            column=1,
            padx=5
        )

        self.status_filter = ctk.CTkComboBox(
            filters,
            values=[
                "All",
                "Pending",
                "Approved",
                "Rejected"
            ],
            width=130,
            height=38,
            state="readonly",
            fg_color=WHITE,
            border_color=BORDER,
            button_color=BLUE,
            button_hover_color=BLUE_HOVER,
            text_color=TEXT
        )

        self.status_filter.set("All")

        self.status_filter.grid(
            row=0,
            column=2,
            padx=5
        )

        search_button = ctk.CTkButton(
            filters,
            text="Search",
            width=90,
            height=38,
            corner_radius=8,
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
            command=self.search_logbook
        )

        search_button.grid(
            row=0,
            column=3,
            padx=(5, 10)
        )

        self.refresh_filters()

    # =====================================================
    # TABLE
    # =====================================================

    def build_table(self, parent):
        table_container = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        table_container.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=22
        )

        table_container.grid_rowconfigure(
            0,
            weight=1
        )

        table_container.grid_columnconfigure(
            0,
            weight=1
        )

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Logbook.Treeview",
            background=WHITE,
            foreground=TEXT,
            rowheight=38,
            fieldbackground=WHITE,
            font=("Segoe UI", 10),
            borderwidth=0
        )

        style.configure(
            "Logbook.Treeview.Heading",
            background="#F1F5F9",
            foreground=TEXT,
            font=("Segoe UI", 10, "bold"),
            relief="flat"
        )

        style.map(
            "Logbook.Treeview",
            background=[
                ("selected", "#DBEAFE")
            ],
            foreground=[
                ("selected", "#1E3A8A")
            ]
        )

        columns = (
            "id",
            "date",
            "week",
            "activities",
            "status"
        )

        self.entry_table = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            style="Logbook.Treeview",
            selectmode="browse"
        )

        self.entry_table.heading(
            "id",
            text="ID"
        )

        self.entry_table.heading(
            "date",
            text="Date"
        )

        self.entry_table.heading(
            "week",
            text="Week"
        )

        self.entry_table.heading(
            "activities",
            text="Activities"
        )

        self.entry_table.heading(
            "status",
            text="Status"
        )

        self.entry_table.column(
            "id",
            width=60,
            anchor="center"
        )

        self.entry_table.column(
            "date",
            width=110,
            anchor="center"
        )

        self.entry_table.column(
            "week",
            width=80,
            anchor="center"
        )

        self.entry_table.column(
            "activities",
            width=500,
            anchor="w"
        )

        self.entry_table.column(
            "status",
            width=110,
            anchor="center"
        )

        self.entry_table.tag_configure(
            "Pending",
            foreground=ORANGE
        )

        self.entry_table.tag_configure(
            "Approved",
            foreground=GREEN
        )

        self.entry_table.tag_configure(
            "Rejected",
            foreground=RED
        )

        scrollbar = ttk.Scrollbar(
            table_container,
            orient="vertical",
            command=self.entry_table.yview
        )

        self.entry_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.entry_table.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.entry_table.bind(
            "<Double-1>",
            lambda event: self.view_selected_entry()
        )

    # =====================================================
    # ACTION BUTTONS
    # =====================================================

    def build_actions(self, parent):
        actions = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        actions.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=22,
            pady=(12, 20)
        )

        self.create_action_button(
            actions,
            "View",
            self.view_selected_entry,
            "#475569"
        )

        self.create_action_button(
            actions,
            "Edit",
            self.edit_selected_entry,
            BLUE
        )

        self.create_action_button(
            actions,
            "Update Status",
            self.update_selected_status,
            PURPLE
        )

        self.create_action_button(
            actions,
            "Delete",
            self.delete_selected_entry,
            RED
        )

    def create_action_button(
        self,
        parent,
        text,
        command,
        color
    ):
        button = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            width=110,
            height=38,
            corner_radius=8,
            fg_color=color,
            hover_color=color
        )

        button.pack(
            side="left",
            padx=(0, 8)
        )

    # =====================================================
    # DATA
    # =====================================================

    def load_entries(self):
        try:
            entries = get_entries(
                self.student_id
            )

            self.display_entries(entries)
            self.update_summary(entries)
            self.refresh_filters(entries)

        except Exception as error:
            messagebox.showerror(
                "Logbook Error",
                f"Could not load logbook entries.\n\n{error}"
            )

    def display_entries(self, entries):
        for item in self.entry_table.get_children():
            self.entry_table.delete(item)

        for entry in entries:
            activity = entry.activities or ""

            if len(activity) > 75:
                activity = activity[:75] + "..."

            self.entry_table.insert(
                "",
                "end",
                iid=str(entry.entry_id),
                values=(
                    entry.entry_id,
                    entry.date,
                    entry.week_number,
                    activity,
                    entry.status
                ),
                tags=(entry.status,)
            )

    def update_summary(self, entries):
        total = len(entries)

        pending = sum(
            1 for entry in entries
            if entry.status == "Pending"
        )

        approved = sum(
            1 for entry in entries
            if entry.status == "Approved"
        )

        rejected = sum(
            1 for entry in entries
            if entry.status == "Rejected"
        )

        self.total_value.configure(
            text=str(total)
        )

        self.pending_value.configure(
            text=str(pending)
        )

        self.approved_value.configure(
            text=str(approved)
        )

        self.rejected_value.configure(
            text=str(rejected)
        )

    def refresh_filters(self, entries=None):
        if entries is None:
            try:
                entries = get_entries(
                    self.student_id
                )
            except Exception:
                entries = []

        weeks = sorted(
            {
                str(entry.week_number)
                for entry in entries
            },
            key=lambda x: int(x)
        )

        self.week_filter.configure(
            values=["All"] + weeks
        )

    # =====================================================
    # FORM HELPERS
    # =====================================================

    def set_today(self):
        self.date_entry.delete(
            0,
            "end"
        )

        self.date_entry.insert(
            0,
            datetime.now().strftime("%d/%m/%Y")
        )

    def reset_form(self):
        self.editing_entry = None

        self.date_entry.delete(
            0,
            "end"
        )

        self.week_entry.delete(
            0,
            "end"
        )

        self.activities_text.delete(
            "1.0",
            "end"
        )

        self.skills_entry.delete(
            0,
            "end"
        )

        self.challenges_text.delete(
            "1.0",
            "end"
        )

        self.form_title.configure(
            text="New Logbook Entry"
        )

        self.form_subtitle.configure(
            text="Record your daily SIWES activities and learning progress."
        )

        self.save_button.configure(
            text="Save Entry"
        )

    def get_form_data(self):
        date = self.date_entry.get().strip()
        week_text = self.week_entry.get().strip()

        activities = self.activities_text.get(
            "1.0",
            "end"
        ).strip()

        skills = self.skills_entry.get().strip()

        challenges = self.challenges_text.get(
            "1.0",
            "end"
        ).strip()

        if not date:
            raise ValueError(
                "Date is required."
            )

        if not week_text:
            raise ValueError(
                "Week number is required."
            )

        try:
            week_number = int(
                week_text
            )
        except ValueError:
            raise ValueError(
                "Week number must be a number."
            )

        return (
            date,
            week_number,
            activities,
            skills,
            challenges
        )

    # =====================================================
    # SAVE / EDIT
    # =====================================================

    def save_logbook_entry(self):
        try:
            (
                date,
                week_number,
                activities,
                skills,
                challenges
            ) = self.get_form_data()

            if self.editing_entry is not None:
                self.update_existing_entry(
                    date,
                    week_number,
                    activities,
                    skills,
                    challenges
                )
            else:
                self.create_new_entry(
                    date,
                    week_number,
                    activities,
                    skills,
                    challenges
                )

            self.load_entries()
            self.reset_form()

        except ValueError as error:
            messagebox.showerror(
                "Invalid Entry",
                str(error)
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Something went wrong.\n\n{error}"
            )

    def create_new_entry(
        self,
        date,
        week_number,
        activities,
        skills,
        challenges
    ):
        if entry_exists(
            self.student_id,
            date
        ):
            raise ValueError(
                "A logbook entry already exists for this date."
            )

        entry = LogbookEntry(
            student_id=self.student_id,
            date=date,
            week_number=week_number,
            activities=activities,
            skills_learned=skills,
            challenges=challenges
        )

        saved = save_entry(entry)

        if saved is None:
            raise ValueError(
                "The logbook entry could not be saved."
            )

        messagebox.showinfo(
            "Success",
            "Logbook entry saved successfully."
        )

    def update_existing_entry(
        self,
        date,
        week_number,
        activities,
        skills,
        challenges
    ):
        entry = self.editing_entry

        if entry_exists(
            self.student_id,
            date,
            exclude_id=entry.entry_id
        ):
            raise ValueError(
                "Another logbook entry already exists for this date."
            )

        entry.date = date
        entry.week_number = week_number
        entry.activities = activities
        entry.skills_learned = skills
        entry.challenges = challenges

        entry.validate()

        update_entry(entry)

        messagebox.showinfo(
            "Success",
            "Logbook entry updated successfully."
        )

    # =====================================================
    # SELECTED ENTRY
    # =====================================================

    def get_selected_entry(self):
        selected = self.entry_table.selection()

        if not selected:
            messagebox.showwarning(
                "No Entry Selected",
                "Please select a logbook entry first."
            )
            return None

        entry_id = int(
            selected[0]
        )

        entries = get_entries(
            self.student_id
        )

        for entry in entries:
            if entry.entry_id == entry_id:
                return entry

        messagebox.showerror(
            "Error",
            "The selected entry could not be found."
        )

        return None

    # =====================================================
    # VIEW
    # =====================================================

    def view_selected_entry(self):
        entry = self.get_selected_entry()

        if entry is None:
            return

        self.show_entry_window(
            entry
        )

    def show_entry_window(self, entry):
        window = ctk.CTkToplevel(
            self
        )

        window.title(
            "Logbook Entry"
        )

        window.geometry(
            "700x720"
        )

        window.configure(
            fg_color=BACKGROUND
        )

        window.grab_set()

        header = ctk.CTkFrame(
            window,
            fg_color=NAVY,
            corner_radius=0
        )

        header.pack(
            fill="x"
        )

        ctk.CTkLabel(
            header,
            text="Logbook Entry",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            ),
            text_color=WHITE
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 2)
        )

        ctk.CTkLabel(
            header,
            text=f"{entry.date}  •  Week {entry.week_number}",
            font=ctk.CTkFont(size=12),
            text_color="#CBD5E1"
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 18)
        )

        body = ctk.CTkScrollableFrame(
            window,
            fg_color=BACKGROUND
        )

        body.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        self.add_view_section(
            body,
            "Status",
            entry.status
        )

        self.add_view_section(
            body,
            "Activities",
            entry.activities
        )

        self.add_view_section(
            body,
            "Skills Learned",
            entry.skills_learned or "None"
        )

        self.add_view_section(
            body,
            "Challenges",
            entry.challenges or "None"
        )

        self.add_view_section(
            body,
            "Supervisor Comment",
            entry.supervisor_comment or "No supervisor comment yet."
        )

        ctk.CTkButton(
            body,
            text="Close",
            width=110,
            height=38,
            corner_radius=8,
            fg_color="#64748B",
            hover_color="#475569",
            command=window.destroy
        ).pack(
            pady=15
        )

    def add_view_section(
        self,
        parent,
        title,
        content
    ):
        card = ctk.CTkFrame(
            parent,
            fg_color=CARD,
            border_width=1,
            border_color=BORDER,
            corner_radius=10
        )

        card.pack(
            fill="x",
            pady=6
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=BLUE
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 3)
        )

        ctk.CTkLabel(
            card,
            text=content,
            font=ctk.CTkFont(size=12),
            text_color=TEXT,
            justify="left",
            anchor="w",
            wraplength=600
        ).pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )

    # =====================================================
    # EDIT
    # =====================================================

    def edit_selected_entry(self):
        entry = self.get_selected_entry()

        if entry is None:
            return

        if entry.status == "Approved":
            messagebox.showwarning(
                "Cannot Edit",
                "Approved entries cannot be edited."
            )
            return

        self.editing_entry = entry

        self.form_title.configure(
            text="Edit Logbook Entry"
        )

        self.form_subtitle.configure(
            text="Update your SIWES activities and learning progress."
        )

        self.date_entry.delete(
            0,
            "end"
        )

        self.date_entry.insert(
            0,
            entry.date
        )

        self.week_entry.delete(
            0,
            "end"
        )

        self.week_entry.insert(
            0,
            str(entry.week_number)
        )

        self.activities_text.delete(
            "1.0",
            "end"
        )

        self.activities_text.insert(
            "1.0",
            entry.activities
        )

        self.skills_entry.delete(
            0,
            "end"
        )

        self.skills_entry.insert(
            0,
            entry.skills_learned or ""
        )

        self.challenges_text.delete(
            "1.0",
            "end"
        )

        self.challenges_text.insert(
            "1.0",
            entry.challenges or ""
        )

        self.save_button.configure(
            text="Save Changes"
        )

        self.after(
            100,
            lambda: self.date_entry.focus()
        )

    # =====================================================
    # DELETE
    # =====================================================

    def delete_selected_entry(self):
        entry = self.get_selected_entry()

        if entry is None:
            return

        if entry.status == "Approved":
            messagebox.showwarning(
                "Cannot Delete",
                "Approved entries cannot be deleted."
            )
            return

        confirm = messagebox.askyesno(
            "Delete Entry",
            "Are you sure you want to delete this logbook entry?"
        )

        if not confirm:
            return

        try:
            delete_entry(entry)

            messagebox.showinfo(
                "Deleted",
                "Logbook entry deleted successfully."
            )

            self.load_entries()

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Could not delete entry.\n\n{error}"
            )

    # =====================================================
    # STATUS
    # =====================================================

    def update_selected_status(self):
        entry = self.get_selected_entry()

        if entry is None:
            return

        if entry.status == "Approved":
            messagebox.showwarning(
                "Status Locked",
                "Approved entries cannot have their status changed."
            )
            return

        window = ctk.CTkToplevel(
            self
        )

        window.title(
            "Update Status"
        )

        window.geometry(
            "500x430"
        )

        window.configure(
            fg_color=BACKGROUND
        )

        window.grab_set()

        card = ctk.CTkFrame(
            window,
            fg_color=CARD,
            border_width=1,
            border_color=BORDER,
            corner_radius=12
        )

        card.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        ctk.CTkLabel(
            card,
            text="Update Logbook Status",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            ),
            text_color=TEXT
        ).pack(
            anchor="w",
            padx=22,
            pady=(22, 4)
        )

        ctk.CTkLabel(
            card,
            text=f"Entry #{entry.entry_id}",
            font=ctk.CTkFont(size=12),
            text_color=MUTED
        ).pack(
            anchor="w",
            padx=22
        )

        ctk.CTkLabel(
            card,
            text="Status",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=TEXT
        ).pack(
            anchor="w",
            padx=22,
            pady=(20, 5)
        )

        status_choice = ctk.CTkComboBox(
            card,
            values=[
                "Pending",
                "Approved",
                "Rejected"
            ],
            state="readonly",
            height=40,
            fg_color=WHITE,
            text_color=TEXT,
            border_color=BORDER,
            button_color=PURPLE,
            button_hover_color="#6D28D9"
        )

        status_choice.set(
            entry.status
        )

        status_choice.pack(
            fill="x",
            padx=22
        )

        ctk.CTkLabel(
            card,
            text="Supervisor Comment",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=TEXT
        ).pack(
            anchor="w",
            padx=22,
            pady=(15, 5)
        )

        comment = ctk.CTkTextbox(
            card,
            height=90,
            fg_color=WHITE,
            text_color=TEXT,
            border_color=BORDER,
            border_width=1,
            corner_radius=8
        )

        if entry.supervisor_comment:
            comment.insert(
                "1.0",
                entry.supervisor_comment
            )

        comment.pack(
            fill="x",
            padx=22
        )

        def save_status():
            try:
                update_entry_status(
                    entry.entry_id,
                    status_choice.get(),
                    comment.get(
                        "1.0",
                        "end"
                    ).strip()
                )

                messagebox.showinfo(
                    "Success",
                    "Logbook status updated successfully."
                )

                window.destroy()
                self.load_entries()

            except ValueError as error:
                messagebox.showerror(
                    "Invalid Status",
                    str(error)
                )

            except Exception as error:
                messagebox.showerror(
                    "Error",
                    str(error)
                )

        ctk.CTkButton(
            card,
            text="Save Status",
            height=40,
            corner_radius=8,
            fg_color=PURPLE,
            hover_color="#6D28D9",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            command=save_status
        ).pack(
            fill="x",
            padx=22,
            pady=18
        )

    # =====================================================
    # SEARCH
    # =====================================================

    def search_logbook(self):
        keyword = self.search_entry.get().strip()

        selected_week = self.week_filter.get()
        selected_status = self.status_filter.get()

        if selected_week == "All":
            week_number = None
        else:
            week_number = int(
                selected_week
            )

        if selected_status == "All":
            status = None
        else:
            status = selected_status

        try:
            entries = filter_entries(
                student_id=self.student_id,
                week_number=week_number,
                status=status,
                keyword=keyword
            )

            self.display_entries(
                entries
            )

        except Exception as error:
            messagebox.showerror(
                "Search Error",
                str(error)
            )


# =========================================================
# STANDALONE PREVIEW
# =========================================================

if __name__ == "__main__":
    root = ctk.CTk()

    root.title(
        "SIWES Management System - Digital Logbook"
    )

    root.geometry(
        "1250x850"
    )

    root.minsize(
        1050,
        700
    )

    root.configure(
        fg_color=BACKGROUND
    )

    logbook = DigitalLogbook(
        root,
        student_id=1023
    )

    logbook.pack(
        fill="both",
        expand=True
    )

    root.mainloop()