import customtkinter as ctk

from tkinter import messagebox

from datetime import datetime



from database.database import get_connection

from services.groq_services import GroqService

from ui.theme import (

    NAVY,

    NAVY_LIGHT,

    BLUE,

    BLUE_HOVER,

    WHITE,

    BACKGROUND,

    CARD,

    INPUT_BG,

    TEXT,

    TEXT_LIGHT,

    BORDER,

    SUCCESS,

    SUCCESS_HOVER,

    WARNING,

    WARNING_HOVER,

    ERROR,

    ERROR_HOVER,

    CORNER_RADIUS,

)





class LogbookPage(ctk.CTkFrame):

    """

    Digital Logbook page for the SIWES Management System.



    Features:

        - Create logbook entries

        - Edit entries

        - Delete entries

        - View full entries

        - Search entries

        - Filter by week

        - Filter by status

        - Supervisor/admin status updates

        - Supervisor comments

        - Duplicate-date prevention

        - Current logged-in student support

        - Central SIWES.db integration

    """



    def __init__(self, parent, user_data=None):

        super().__init__(

            parent,

            fg_color=BACKGROUND

        )



        self.user_data = user_data or {}

        self.student_id = None

        self.editing_entry_id = None



        self.build_ui()

        self.resolve_student()

        self.load_entries()



    # =========================================================

    # USER / STUDENT

    # =========================================================



    def resolve_student(self):

        """

        Find the student's database ID using the logged-in user's

        email, username, or ID.

        """



        try:

            conn = get_connection()

            cursor = conn.cursor()



            email = self.user_data.get("email")

            username = self.user_data.get("username")

            user_id = self.user_data.get("id")



            student = None



            # First try email.

            if email:

                cursor.execute(

                    """

                    SELECT *

                    FROM students

                    WHERE email = ?

                    LIMIT 1

                    """,

                    (email,)

                )

                student = cursor.fetchone()



            # Try username if email did not work.

            if student is None and username:

                cursor.execute(

                    """

                    SELECT *

                    FROM students

                    WHERE email = ?

                    LIMIT 1

                    """,

                    (username,)

                )

                student = cursor.fetchone()



            # Try user_id if the students table contains a user_id column.

            if student is None and user_id:

                try:

                    cursor.execute(

                        """

                        SELECT *

                        FROM students

                        WHERE user_id = ?

                        LIMIT 1

                        """,

                        (user_id,)

                    )

                    student = cursor.fetchone()

                except Exception:

                    pass



            if student:

                self.student_id = student["id"]



                full_name = student["full_name"] or self.user_data.get(

                    "full_name",

                    "Student"

                )



                self.student_name_label.configure(

                    text=f"Student: {full_name}"

                )



            else:

                self.student_id = None



                self.student_name_label.configure(

                    text="Student profile not found"

                )



            conn.close()



        except Exception as error:

            self.student_id = None



            if hasattr(self, "student_name_label"):

                self.student_name_label.configure(

                    text="Unable to load student profile"

                )



            print(f"Student lookup error: {error}")



    # =========================================================

    # UI

    # =========================================================



    def build_ui(self):



        # -----------------------------------------------------

        # Main scrollable container

        # -----------------------------------------------------



        self.scroll_frame = ctk.CTkScrollableFrame(

            self,

            fg_color=BACKGROUND,

            scrollbar_button_color=BORDER,

            scrollbar_button_hover_color=TEXT_LIGHT

        )



        self.scroll_frame.pack(

            fill="both",

            expand=True,

            padx=20,

            pady=20

        )



        # -----------------------------------------------------

        # Header

        # -----------------------------------------------------



        header_frame = ctk.CTkFrame(

            self.scroll_frame,

            fg_color="transparent"

        )



        header_frame.pack(

            fill="x",

            pady=(0, 20)

        )



        title_frame = ctk.CTkFrame(

            header_frame,

            fg_color="transparent"

        )



        title_frame.pack(

            side="left",

            fill="x",

            expand=True

        )



        ctk.CTkLabel(

            title_frame,

            text="Digital Logbook",

            font=("Arial", 26, "bold"),

            text_color=TEXT

        ).pack(

            anchor="w"

        )



        ctk.CTkLabel(

            title_frame,

            text="Record your daily SIWES activities and learning progress.",

            font=("Arial", 13),

            text_color=TEXT_LIGHT

        ).pack(

            anchor="w",

            pady=(4, 0)

        )



        self.student_name_label = ctk.CTkLabel(

            header_frame,

            text="Loading student...",

            font=("Arial", 12, "bold"),

            text_color=NAVY

        )



        self.student_name_label.pack(

            side="right",

            padx=10

        )



        # -----------------------------------------------------

        # Statistics

        # -----------------------------------------------------



        self.stats_frame = ctk.CTkFrame(

            self.scroll_frame,

            fg_color="transparent"

        )



        self.stats_frame.pack(

            fill="x",

            pady=(0, 20)

        )



        for column in range(4):

            self.stats_frame.grid_columnconfigure(

                column,

                weight=1

            )



        self.total_stat = self.create_stat_card(

            self.stats_frame,

            "Total Entries",

            "0",

            0

        )



        self.pending_stat = self.create_stat_card(

            self.stats_frame,

            "Pending",

            "0",

            1

        )



        self.approved_stat = self.create_stat_card(

            self.stats_frame,

            "Approved",

            "0",

            2

        )



        self.rejected_stat = self.create_stat_card(

            self.stats_frame,

            "Rejected",

            "0",

            3

        )



        # -----------------------------------------------------

        # Entry form

        # -----------------------------------------------------



        self.form_card = ctk.CTkFrame(

            self.scroll_frame,

            fg_color=CARD,

            corner_radius=CORNER_RADIUS,

            border_width=1,

            border_color=BORDER

        )



        self.form_card.pack(

            fill="x",

            pady=(0, 20)

        )



        # Form header



        form_header = ctk.CTkFrame(

            self.form_card,

            fg_color="transparent"

        )



        form_header.pack(

            fill="x",

            padx=20,

            pady=(18, 5)

        )



        self.form_title = ctk.CTkLabel(

            form_header,

            text="New Logbook Entry",

            font=("Arial", 18, "bold"),

            text_color=TEXT

        )



        self.form_title.pack(

            anchor="w"

        )



        self.form_subtitle = ctk.CTkLabel(

            form_header,

            text="Record your daily SIWES activities and learning progress.",

            font=("Arial", 12),

            text_color=TEXT_LIGHT

        )



        self.form_subtitle.pack(

            anchor="w",

            pady=(3, 0)

        )



        # -----------------------------------------------------

        # Date + Week

        # -----------------------------------------------------



        basic_frame = ctk.CTkFrame(

            self.form_card,

            fg_color="transparent"

        )



        basic_frame.pack(

            fill="x",

            padx=20,

            pady=(12, 5)

        )



        basic_frame.grid_columnconfigure(0, weight=1)

        basic_frame.grid_columnconfigure(1, weight=1)



        # Date



        date_container = ctk.CTkFrame(

            basic_frame,

            fg_color="transparent"

        )



        date_container.grid(

            row=0,

            column=0,

            sticky="ew",

            padx=(0, 8)

        )



        ctk.CTkLabel(

            date_container,

            text="Date",

            font=("Arial", 12, "bold"),

            text_color=TEXT

        ).pack(

            anchor="w",

            pady=(0, 5)

        )



        date_row = ctk.CTkFrame(

            date_container,

            fg_color="transparent"

        )



        date_row.pack(

            fill="x"

        )



        self.date_entry = ctk.CTkEntry(

            date_row,

            height=42,

            placeholder_text="DD/MM/YYYY",

            fg_color=INPUT_BG,

            border_color=BORDER,

            text_color=TEXT,

            corner_radius=8

        )



        self.date_entry.pack(

            side="left",

            fill="x",

            expand=True

        )



        ctk.CTkButton(

            date_row,

            text="Today",

            width=80,

            height=42,

            fg_color=NAVY_LIGHT,

            hover_color=NAVY,

            command=self.set_today,

            corner_radius=8

        ).pack(

            side="left",

            padx=(8, 0)

        )



        # Week



        week_container = ctk.CTkFrame(

            basic_frame,

            fg_color="transparent"

        )



        week_container.grid(

            row=0,

            column=1,

            sticky="ew",

            padx=(8, 0)

        )



        ctk.CTkLabel(

            week_container,

            text="Week Number",

            font=("Arial", 12, "bold"),

            text_color=TEXT

        ).pack(

            anchor="w",

            pady=(0, 5)

        )



        self.week_entry = ctk.CTkEntry(

            week_container,

            height=42,

            placeholder_text="e.g. 1",

            fg_color=INPUT_BG,

            border_color=BORDER,

            text_color=TEXT,

            corner_radius=8

        )



        self.week_entry.pack(

            fill="x"

        )



        # -----------------------------------------------------

        # Activities

        # -----------------------------------------------------



        self.create_text_field(

            self.form_card,

            "Activities",

            "Describe the activities you carried out today.",

            height=110

        )



        # The previous call creates self.activities_text.



        # -----------------------------------------------------

        # Skills

        # -----------------------------------------------------



        skills_container = ctk.CTkFrame(

            self.form_card,

            fg_color="transparent"

        )



        skills_container.pack(

            fill="x",

            padx=20,

            pady=8

        )



        ctk.CTkLabel(

            skills_container,

            text="Skills Learned",

            font=("Arial", 12, "bold"),

            text_color=TEXT

        ).pack(

            anchor="w",

            pady=(0, 5)

        )



        self.skills_entry = ctk.CTkEntry(

            skills_container,

            height=42,

            placeholder_text="Skills, technologies, or knowledge gained",

            fg_color=INPUT_BG,

            border_color=BORDER,

            text_color=TEXT,

            corner_radius=8

        )



        self.skills_entry.pack(

            fill="x"

        )



        # -----------------------------------------------------

        # Challenges

        # -----------------------------------------------------



        self.create_challenges_field()



        # -----------------------------------------------------

        # Form buttons

        # -----------------------------------------------------



        form_buttons = ctk.CTkFrame(

            self.form_card,

            fg_color="transparent"

        )



        form_buttons.pack(

            fill="x",

            padx=20,

            pady=(10, 20)

        )



        self.save_button = ctk.CTkButton(

            form_buttons,

            text="Save Entry",

            width=130,

            height=42,

            fg_color=BLUE,

            hover_color=BLUE_HOVER,

            command=self.save_logbook_entry,

            corner_radius=8

        )



        self.save_button.pack(

            side="left"

        )

        self.ai_button = ctk.CTkButton(

            form_buttons,

            text="🤖 AI Assist",

            width=120,

            height=42,

            fg_color="#7C3AED",

            hover_color="#6D28D9",

            command=self.ai_assist,

            corner_radius=8

        )

        self.ai_button.pack(

            side="left",

            padx=10

        )





        ctk.CTkButton(

            form_buttons,

            text="New Entry",

            width=120,

            height=42,

            fg_color=NAVY_LIGHT,

            hover_color=NAVY,

            command=self.reset_form,

            corner_radius=8

        ).pack(

            side="left",

            padx=10

        )



        # -----------------------------------------------------

        # Search / filters

        # -----------------------------------------------------



        search_card = ctk.CTkFrame(

            self.scroll_frame,

            fg_color=CARD,

            corner_radius=CORNER_RADIUS,

            border_width=1,

            border_color=BORDER

        )



        search_card.pack(

            fill="x",

            pady=(0, 12)

        )



        ctk.CTkLabel(

            search_card,

            text="Search & Filter",

            font=("Arial", 16, "bold"),

            text_color=TEXT

        ).pack(

            anchor="w",

            padx=20,

            pady=(15, 10)

        )



        filters_frame = ctk.CTkFrame(

            search_card,

            fg_color="transparent"

        )



        filters_frame.pack(

            fill="x",

            padx=20,

            pady=(0, 15)

        )



        filters_frame.grid_columnconfigure(

            0,

            weight=3

        )



        filters_frame.grid_columnconfigure(

            1,

            weight=1

        )



        filters_frame.grid_columnconfigure(

            2,

            weight=1

        )



        filters_frame.grid_columnconfigure(

            3,

            weight=0

        )



        filters_frame.grid_columnconfigure(

            4,

            weight=0

        )



        # Search



        search_container = ctk.CTkFrame(

            filters_frame,

            fg_color="transparent"

        )



        search_container.grid(

            row=0,

            column=0,

            sticky="ew",

            padx=(0, 8)

        )



        self.search_entry = ctk.CTkEntry(

            search_container,

            height=40,

            placeholder_text="Search activities, skills, challenges...",

            fg_color=INPUT_BG,

            border_color=BORDER,

            text_color=TEXT,

            corner_radius=8

        )



        self.search_entry.pack(

            fill="x"

        )



        # Week filter



        self.week_filter = ctk.CTkComboBox(

            filters_frame,

            values=[

                "All",

                "1",

                "2",

                "3",

                "4",

                "5",

                "6",

                "7",

                "8",

                "9",

                "10",

                "11",

                "12",

                "13",

                "14",

                "15",

                "16"

            ],

            height=40,

            fg_color=INPUT_BG,

            border_color=BORDER,

            button_color=NAVY_LIGHT,

            button_hover_color=NAVY,

            text_color=TEXT,

            corner_radius=8

        )



        self.week_filter.grid(

            row=0,

            column=1,

            sticky="ew",

            padx=8

        )



        self.week_filter.set("All")



        # Status filter



        self.status_filter = ctk.CTkComboBox(

            filters_frame,

            values=[

                "All",

                "Pending",

                "Approved",

                "Rejected"

            ],

            height=40,

            fg_color=INPUT_BG,

            border_color=BORDER,

            button_color=NAVY_LIGHT,

            button_hover_color=NAVY,

            text_color=TEXT,

            corner_radius=8

        )



        self.status_filter.grid(

            row=0,

            column=2,

            sticky="ew",

            padx=8

        )



        self.status_filter.set("All")



        # Search button



        ctk.CTkButton(

            filters_frame,

            text="Search",

            width=90,

            height=40,

            fg_color=BLUE,

            hover_color=BLUE_HOVER,

            command=self.search_logbook,

            corner_radius=8

        ).grid(

            row=0,

            column=3,

            padx=8

        )



        # Clear



        ctk.CTkButton(

            filters_frame,

            text="Clear",

            width=80,

            height=40,

            fg_color=NAVY_LIGHT,

            hover_color=NAVY,

            command=self.clear_filters,

            corner_radius=8

        ).grid(

            row=0,

            column=4,

            padx=(8, 0)

        )



        # -----------------------------------------------------

        # Entries card

        # -----------------------------------------------------



        entries_card = ctk.CTkFrame(

            self.scroll_frame,

            fg_color=CARD,

            corner_radius=CORNER_RADIUS,

            border_width=1,

            border_color=BORDER

        )



        entries_card.pack(

            fill="both",

            expand=True

        )



        entries_header = ctk.CTkFrame(

            entries_card,

            fg_color="transparent"

        )



        entries_header.pack(

            fill="x",

            padx=20,

            pady=(15, 10)

        )



        ctk.CTkLabel(

            entries_header,

            text="My Logbook Entries",

            font=("Arial", 17, "bold"),

            text_color=TEXT

        ).pack(

            side="left"

        )



        # -----------------------------------------------------

        # Entry list

        # -----------------------------------------------------



        self.entries_container = ctk.CTkFrame(

            entries_card,

            fg_color="transparent"

        )



        self.entries_container.pack(

            fill="x",

            padx=20,

            pady=(0, 20)

        )



        # Initial empty state.

        self.show_empty_state()



    # =========================================================

    # COMPONENT HELPERS

    # =========================================================



    def create_stat_card(

        self,

        parent,

        title,

        value,

        column

    ):



        card = ctk.CTkFrame(

            parent,

            fg_color=CARD,

            corner_radius=CORNER_RADIUS,

            border_width=1,

            border_color=BORDER

        )



        card.grid(

            row=0,

            column=column,

            sticky="ew",

            padx=5

        )



        ctk.CTkLabel(

            card,

            text=title,

            font=("Arial", 11),

            text_color=TEXT_LIGHT

        ).pack(

            anchor="w",

            padx=15,

            pady=(12, 2)

        )



        value_label = ctk.CTkLabel(

            card,

            text=value,

            font=("Arial", 24, "bold"),

            text_color=TEXT

        )



        value_label.pack(

            anchor="w",

            padx=15,

            pady=(0, 12)

        )



        return value_label



    def create_text_field(

        self,

        parent,

        title,

        placeholder,

        height=100

    ):



        container = ctk.CTkFrame(

            parent,

            fg_color="transparent"

        )



        container.pack(

            fill="x",

            padx=20,

            pady=8

        )



        ctk.CTkLabel(

            container,

            text=title,

            font=("Arial", 12, "bold"),

            text_color=TEXT

        ).pack(

            anchor="w",

            pady=(0, 5)

        )



        text_widget = ctk.CTkTextbox(

            container,

            height=height,

            fg_color=INPUT_BG,

            border_color=BORDER,

            border_width=1,

            text_color=TEXT,

            corner_radius=8,

            wrap="word"

        )



        text_widget.pack(

            fill="x"

        )



        text_widget.insert(

            "1.0",

            ""

        )



        if title == "Activities":

            self.activities_text = text_widget



        return text_widget



    def create_challenges_field(self):



        container = ctk.CTkFrame(

            self.form_card,

            fg_color="transparent"

        )



        container.pack(

            fill="x",

            padx=20,

            pady=8

        )



        ctk.CTkLabel(

            container,

            text="Challenges",

            font=("Arial", 12, "bold"),

            text_color=TEXT

        ).pack(

            anchor="w",

            pady=(0, 5)

        )



        self.challenges_text = ctk.CTkTextbox(

            container,

            height=100,

            fg_color=INPUT_BG,

            border_color=BORDER,

            border_width=1,

            text_color=TEXT,

            corner_radius=8,

            wrap="word"

        )



        self.challenges_text.pack(

            fill="x"

        )



    # =========================================================

    # DATE

    # =========================================================



    def set_today(self):



        today = datetime.now().strftime("%d/%m/%Y")



        self.date_entry.delete(0, "end")

        self.date_entry.insert(0, today)



    # =========================================================

    # DATABASE HELPERS

    # =========================================================



    def get_entries(self):



        if self.student_id is None:

            return []



        conn = get_connection()



        cursor = conn.cursor()



        cursor.execute(

            """

            SELECT

                id,

                student_id,

                date,

                week_number,

                activities,

                skills_learned,

                challenges,

                supervisor_comment,

                status

            FROM logbook_entries

            WHERE student_id = ?

            ORDER BY

                date DESC,

                id DESC

            """,

            (self.student_id,)

        )



        rows = cursor.fetchall()



        conn.close()



        return rows



    def get_filtered_entries(

        self,

        keyword="",

        week_number=None,

        status=None

    ):



        if self.student_id is None:

            return []



        conn = get_connection()



        cursor = conn.cursor()



        query = """

            SELECT

                id,

                student_id,

                date,

                week_number,

                activities,

                skills_learned,

                challenges,

                supervisor_comment,

                status

            FROM logbook_entries

            WHERE student_id = ?

        """



        params = [self.student_id]



        if week_number is not None:

            query += """

                AND week_number = ?

            """



            params.append(week_number)



        if status is not None:

            query += """

                AND status = ?

            """



            params.append(status)



        if keyword:

            query += """

                AND (

                    activities LIKE ?

                    OR skills_learned LIKE ?

                    OR challenges LIKE ?

                    OR supervisor_comment LIKE ?

                )

            """



            search_term = f"%{keyword}%"



            params.extend([

                search_term,

                search_term,

                search_term,

                search_term

            ])



        query += """

            ORDER BY date DESC, id DESC

        """



        cursor.execute(

            query,

            tuple(params)

        )



        rows = cursor.fetchall()



        conn.close()



        return rows



    def entry_exists(

        self,

        date_value,

        exclude_id=None

    ):



        if self.student_id is None:

            return False



        conn = get_connection()



        cursor = conn.cursor()



        if exclude_id is None:



            cursor.execute(

                """

                SELECT id

                FROM logbook_entries

                WHERE student_id = ?

                AND date = ?

                LIMIT 1

                """,

                (

                    self.student_id,

                    date_value

                )

            )



        else:



            cursor.execute(

                """

                SELECT id

                FROM logbook_entries

                WHERE student_id = ?

                AND date = ?

                AND id != ?

                LIMIT 1

                """,

                (

                    self.student_id,

                    date_value,

                    exclude_id

                )

            )



        result = cursor.fetchone()



        conn.close()



        return result is not None



    # =========================================================

    # SAVE / UPDATE

    # =========================================================



    def save_logbook_entry(self):



        if self.student_id is None:



            messagebox.showerror(

                "Student Profile Required",

                "Your student profile could not be found.\n\n"

                "Please complete My Information first."

            )



            return



        date_value = self.date_entry.get().strip()

        week_value = self.week_entry.get().strip()



        activities = self.activities_text.get(

            "1.0",

            "end"

        ).strip()



        skills = self.skills_entry.get().strip()



        challenges = self.challenges_text.get(

            "1.0",

            "end"

        ).strip()



        # -----------------------------------------------------

        # Validation

        # -----------------------------------------------------



        if not date_value:

            messagebox.showerror(

                "Invalid Entry",

                "Please enter the logbook date."

            )

            return



        try:

            datetime.strptime(

                date_value,

                "%d/%m/%Y"

            )



        except ValueError:

            messagebox.showerror(

                "Invalid Date",

                "Please enter the date in DD/MM/YYYY format."

            )

            return



        if not week_value:



            messagebox.showerror(

                "Invalid Entry",

                "Please enter the week number."

            )



            return



        try:

            week_number = int(week_value)



        except ValueError:



            messagebox.showerror(

                "Invalid Week",

                "Week number must be a number."

            )



            return



        if week_number < 1:



            messagebox.showerror(

                "Invalid Week",

                "Week number must be at least 1."

            )



            return



        if not activities:



            messagebox.showerror(

                "Invalid Entry",

                "Please describe the activities you carried out."

            )



            return



        # -----------------------------------------------------

        # Database date

        # -----------------------------------------------------



        try:



            parsed_date = datetime.strptime(

                date_value,

                "%d/%m/%Y"

            )



            database_date = parsed_date.strftime(

                "%Y-%m-%d"

            )



        except ValueError:



            messagebox.showerror(

                "Invalid Date",

                "Invalid date."

            )



            return



        # -----------------------------------------------------

        # Duplicate date

        # -----------------------------------------------------



        if self.entry_exists(

            database_date,

            exclude_id=self.editing_entry_id

        ):



            messagebox.showerror(

                "Duplicate Entry",

                "A logbook entry already exists for this date."

            )



            return



        # -----------------------------------------------------

        # Update existing

        # -----------------------------------------------------



        try:



            conn = get_connection()



            cursor = conn.cursor()



            if self.editing_entry_id is not None:



                cursor.execute(

                    """

                    UPDATE logbook_entries

                    SET

                        date = ?,

                        week_number = ?,

                        activities = ?,

                        skills_learned = ?,

                        challenges = ?

                    WHERE id = ?

                    AND student_id = ?

                    """,

                    (

                        database_date,

                        week_number,

                        activities,

                        skills,

                        challenges,

                        self.editing_entry_id,

                        self.student_id

                    )

                )



                conn.commit()



                conn.close()



                messagebox.showinfo(

                    "Success",

                    "Logbook entry updated successfully."

                )



            # -------------------------------------------------

            # Create new

            # -------------------------------------------------



            else:



                cursor.execute(

                    """

                    INSERT INTO logbook_entries (

                        student_id,

                        date,

                        week_number,

                        activities,

                        skills_learned,

                        challenges,

                        supervisor_comment,

                        status

                    )

                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)

                    """,

                    (

                        self.student_id,

                        database_date,

                        week_number,

                        activities,

                        skills,

                        challenges,

                        "",

                        "Pending"

                    )

                )



                conn.commit()



                conn.close()



                messagebox.showinfo(

                    "Success",

                    "Logbook entry saved successfully."

                )



            self.reset_form()

            self.load_entries()



        except Exception as error:



            messagebox.showerror(

                "Database Error",

                f"Could not save the logbook entry.\n\n{error}"

            )



    # =========================================================
    # AI ASSIST
    # =========================================================

    def ai_assist(self):
        """Use Groq AI to improve and populate the logbook form."""

        activities = self.activities_text.get("1.0", "end").strip()

        if not activities:
            messagebox.showwarning(
                "AI Assist",
                "Please enter your activities first."
            )
            return

        try:
            service = GroqService()
            result = service.generate_logbook_entry(activities)

            cleaned = result.replace("**", "").strip()

            ai_activities = activities
            ai_skills = ""
            ai_challenges = ""

            if "Activities:" in cleaned:
                after_activities = cleaned.split("Activities:", 1)[1]

                if "Skills Learned:" in after_activities:
                    ai_activities, remaining = after_activities.split(
                        "Skills Learned:", 1
                    )
                elif "Challenges:" in after_activities:
                    ai_activities, remaining = after_activities.split(
                        "Challenges:", 1
                    )
                else:
                    ai_activities = after_activities
                    remaining = ""

                if "Challenges:" in remaining:
                    ai_skills, ai_challenges = remaining.split(
                        "Challenges:", 1
                    )
                else:
                    ai_skills = remaining

            elif "Skills Learned:" in cleaned:
                ai_activities, remaining = cleaned.split(
                    "Skills Learned:", 1
                )

                if "Challenges:" in remaining:
                    ai_skills, ai_challenges = remaining.split(
                        "Challenges:", 1
                    )
                else:
                    ai_skills = remaining

            elif "Challenges:" in cleaned:
                ai_activities, ai_challenges = cleaned.split(
                    "Challenges:", 1
                )

            ai_activities = ai_activities.strip()
            ai_skills = ai_skills.strip()
            ai_challenges = ai_challenges.strip()

            self.activities_text.delete("1.0", "end")
            self.activities_text.insert("1.0", ai_activities)

            # The actual Skills Learned widget is self.skills_entry.
            self.skills_entry.delete(0, "end")
            self.skills_entry.insert(0, ai_skills)

            self.challenges_text.delete("1.0", "end")
            self.challenges_text.insert("1.0", ai_challenges)

            messagebox.showinfo(
                "AI Assist",
                "AI has generated and filled your logbook entry.\n\n"
                "Please review the content before saving."
            )

        except Exception as error:
            messagebox.showerror(
                "AI Error",
                f"Could not generate the AI-assisted entry.\n\n{error}"
            )

    def reset_form(self):



        self.editing_entry_id = None



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



    # =========================================================

    # LOAD ENTRIES

    # =========================================================



    def load_entries(self):



        rows = self.get_entries()



        self.display_entries(rows)



        self.update_statistics(rows)



    # =========================================================

    # DISPLAY ENTRIES

    # =========================================================



    def clear_entries_container(self):



        for widget in self.entries_container.winfo_children():

            widget.destroy()



    def show_empty_state(self):



        self.clear_entries_container()



        empty_card = ctk.CTkFrame(

            self.entries_container,

            fg_color=INPUT_BG,

            corner_radius=10,

            border_width=1,

            border_color=BORDER

        )



        empty_card.pack(

            fill="x",

            pady=5

        )



        ctk.CTkLabel(

            empty_card,

            text="No logbook entries found",

            font=("Arial", 16, "bold"),

            text_color=TEXT

        ).pack(

            pady=(25, 5)

        )



        ctk.CTkLabel(

            empty_card,

            text="Create your first SIWES logbook entry above.",

            font=("Arial", 12),

            text_color=TEXT_LIGHT

        ).pack(

            pady=(0, 25)

        )



    def display_entries(self, rows):



        self.clear_entries_container()



        if not rows:



            self.show_empty_state()

            return



        for row in rows:



            self.create_entry_card(row)



    def create_entry_card(self, row):



        (

            entry_id,

            student_id,

            database_date,

            week_number,

            activities,

            skills,

            challenges,

            supervisor_comment,

            status

        ) = row



        # Convert date to DD/MM/YYYY for display.



        try:



            display_date = datetime.strptime(

                database_date,

                "%Y-%m-%d"

            ).strftime(

                "%d/%m/%Y"

            )



        except ValueError:



            display_date = database_date



        card = ctk.CTkFrame(

            self.entries_container,

            fg_color=WHITE,

            corner_radius=10,

            border_width=1,

            border_color=BORDER

        )



        card.pack(

            fill="x",

            pady=6

        )



        # -----------------------------------------------------

        # Top row

        # -----------------------------------------------------



        top = ctk.CTkFrame(

            card,

            fg_color="transparent"

        )



        top.pack(

            fill="x",

            padx=15,

            pady=(12, 5)

        )



        ctk.CTkLabel(

            top,

            text=f"Week {week_number}",

            font=("Arial", 14, "bold"),

            text_color=NAVY

        ).pack(

            side="left"

        )



        ctk.CTkLabel(

            top,

            text=display_date,

            font=("Arial", 12),

            text_color=TEXT_LIGHT

        ).pack(

            side="left",

            padx=15

        )



        status_color = self.get_status_color(

            status

        )



        ctk.CTkLabel(

            top,

            text=status,

            font=("Arial", 11, "bold"),

            text_color=status_color,

            fg_color=self.get_status_background(status),

            corner_radius=8,

            padx=10,

            pady=4

        ).pack(

            side="right"

        )



        # -----------------------------------------------------

        # Activities preview

        # -----------------------------------------------------



        activity_text = activities or ""



        if len(activity_text) > 180:



            activity_text = (

                activity_text[:180].rstrip()

                + "..."

            )



        ctk.CTkLabel(

            card,

            text=activity_text,

            font=("Arial", 12),

            text_color=TEXT,

            justify="left",

            anchor="w",

            wraplength=900

        ).pack(

            fill="x",

            padx=15,

            pady=(5, 5)

        )



        # -----------------------------------------------------

        # Skills

        # -----------------------------------------------------



        if skills:



            skills_preview = skills



            if len(skills_preview) > 140:



                skills_preview = (

                    skills_preview[:140].rstrip()

                    + "..."

                )



            ctk.CTkLabel(

                card,

                text=f"Skills: {skills_preview}",

                font=("Arial", 11),

                text_color=TEXT_LIGHT,

                justify="left",

                anchor="w",

                wraplength=900

            ).pack(

                fill="x",

                padx=15,

                pady=(0, 5)

            )



        # -----------------------------------------------------

        # Supervisor comment

        # -----------------------------------------------------



        if supervisor_comment:



            ctk.CTkLabel(

                card,

                text=f"Supervisor: {supervisor_comment}",

                font=("Arial", 11),

                text_color=TEXT_LIGHT,

                justify="left",

                anchor="w",

                wraplength=900

            ).pack(

                fill="x",

                padx=15,

                pady=(0, 5)

            )



        # -----------------------------------------------------

        # Actions

        # -----------------------------------------------------



        actions = ctk.CTkFrame(

            card,

            fg_color="transparent"

        )



        actions.pack(

            fill="x",

            padx=15,

            pady=(5, 12)

        )



        ctk.CTkButton(

            actions,

            text="View",

            width=85,

            height=34,

            fg_color=NAVY_LIGHT,

            hover_color=NAVY,

            command=lambda rid=entry_id: self.view_entry(rid),

            corner_radius=7

        ).pack(

            side="left",

            padx=(0, 6)

        )



        if status != "Approved":



            ctk.CTkButton(

                actions,

                text="Edit",

                width=85,

                height=34,

                fg_color=BLUE,

                hover_color=BLUE_HOVER,

                command=lambda rid=entry_id: self.start_edit_entry(rid),

                corner_radius=7

            ).pack(

                side="left",

                padx=6

            )



            ctk.CTkButton(

                actions,

                text="Delete",

                width=85,

                height=34,

                fg_color=ERROR,

                hover_color=ERROR_HOVER,

                command=lambda rid=entry_id: self.delete_entry(rid),

                corner_radius=7

            ).pack(

                side="left",

                padx=6

            )



        # Supervisor/admin action



        role = self.user_data.get(

            "role",

            "student"

        )



        if role in (

            "supervisor",

            "admin"

        ):



            ctk.CTkButton(

                actions,

                text="Update Status",

                width=120,

                height=34,

                fg_color="#7C3AED",

                hover_color="#6D28D9",

                command=lambda rid=entry_id: self.update_status(rid),

                corner_radius=7

            ).pack(

                side="right"

            )



    # =========================================================

    # STATISTICS

    # =========================================================



    def update_statistics(self, rows):



        total = len(rows)



        pending = sum(

            1 for row in rows

            if row[8] == "Pending"

        )



        approved = sum(

            1 for row in rows

            if row[8] == "Approved"

        )



        rejected = sum(

            1 for row in rows

            if row[8] == "Rejected"

        )



        self.total_stat.configure(

            text=str(total)

        )



        self.pending_stat.configure(

            text=str(pending)

        )



        self.approved_stat.configure(

            text=str(approved)

        )



        self.rejected_stat.configure(

            text=str(rejected)

        )



    # =========================================================

    # SEARCH

    # =========================================================



    def search_logbook(self):



        keyword = self.search_entry.get().strip()



        selected_week = self.week_filter.get()



        selected_status = self.status_filter.get()



        if selected_week == "All":



            week_number = None



        else:



            try:

                week_number = int(

                    selected_week

                )



            except ValueError:

                week_number = None



        if selected_status == "All":



            status = None



        else:



            status = selected_status



        rows = self.get_filtered_entries(

            keyword=keyword,

            week_number=week_number,

            status=status

        )



        self.display_entries(rows)



    def clear_filters(self):



        self.search_entry.delete(

            0,

            "end"

        )



        self.week_filter.set(

            "All"

        )



        self.status_filter.set(

            "All"

        )



        self.load_entries()



    # =========================================================

    # VIEW

    # =========================================================



    def get_entry(self, entry_id):



        conn = get_connection()



        cursor = conn.cursor()



        cursor.execute(

            """

            SELECT

                id,

                student_id,

                date,

                week_number,

                activities,

                skills_learned,

                challenges,

                supervisor_comment,

                status

            FROM logbook_entries

            WHERE id = ?

            AND student_id = ?

            LIMIT 1

            """,

            (

                entry_id,

                self.student_id

            )

        )



        row = cursor.fetchone()



        conn.close()



        return row



    def view_entry(self, entry_id):



        row = self.get_entry(

            entry_id

        )



        if row is None:



            messagebox.showerror(

                "Entry Not Found",

                "The selected logbook entry could not be found."

            )



            return



        (

            entry_id,

            student_id,

            database_date,

            week_number,

            activities,

            skills,

            challenges,

            supervisor_comment,

            status

        ) = row



        try:



            display_date = datetime.strptime(

                database_date,

                "%Y-%m-%d"

            ).strftime(

                "%d/%m/%Y"

            )



        except ValueError:



            display_date = database_date



        dialog = ctk.CTkToplevel(

            self

        )



        dialog.title(

            "View Logbook Entry"

        )



        dialog.geometry(

            "720x720"

        )



        dialog.minsize(

            600,

            600

        )



        dialog.configure(

            fg_color=BACKGROUND

        )



        dialog.transient(

            self.winfo_toplevel()

        )



        dialog.grab_set()



        scroll = ctk.CTkScrollableFrame(

            dialog,

            fg_color=BACKGROUND

        )



        scroll.pack(

            fill="both",

            expand=True,

            padx=20,

            pady=20

        )



        card = ctk.CTkFrame(

            scroll,

            fg_color=CARD,

            corner_radius=CORNER_RADIUS,

            border_width=1,

            border_color=BORDER

        )



        card.pack(

            fill="x"

        )



        ctk.CTkLabel(

            card,

            text="Logbook Entry",

            font=("Arial", 22, "bold"),

            text_color=TEXT

        ).pack(

            anchor="w",

            padx=20,

            pady=(20, 5)

        )



        ctk.CTkLabel(

            card,

            text=f"Date: {display_date}     •     Week: {week_number}",

            font=("Arial", 12),

            text_color=TEXT_LIGHT

        ).pack(

            anchor="w",

            padx=20,

            pady=(0, 4)

        )



        ctk.CTkLabel(

            card,

            text=f"Status: {status}",

            font=("Arial", 12, "bold"),

            text_color=self.get_status_color(status)

        ).pack(

            anchor="w",

            padx=20,

            pady=(0, 15)

        )



        self.add_view_section(

            card,

            "Activities",

            activities or "None"

        )



        self.add_view_section(

            card,

            "Skills Learned",

            skills or "None"

        )



        self.add_view_section(

            card,

            "Challenges",

            challenges or "None"

        )



        self.add_view_section(

            card,

            "Supervisor Comment",

            supervisor_comment or "No supervisor comment yet."

        )



        ctk.CTkButton(

            card,

            text="Close",

            width=110,

            height=40,

            fg_color=NAVY_LIGHT,

            hover_color=NAVY,

            command=dialog.destroy,

            corner_radius=8

        ).pack(

            anchor="e",

            padx=20,

            pady=20

        )



    def add_view_section(

        self,

        parent,

        title,

        content

    ):



        section = ctk.CTkFrame(

            parent,

            fg_color="transparent"

        )



        section.pack(

            fill="x",

            padx=20,

            pady=8

        )



        ctk.CTkLabel(

            section,

            text=title,

            font=("Arial", 13, "bold"),

            text_color=TEXT

        ).pack(

            anchor="w",

            pady=(0, 5)

        )



        content_box = ctk.CTkTextbox(

            section,

            height=90,

            fg_color=INPUT_BG,

            border_color=BORDER,

            border_width=1,

            text_color=TEXT,

            corner_radius=8,

            wrap="word"

        )



        content_box.pack(

            fill="x"

        )



        content_box.insert(

            "1.0",

            content

        )



        content_box.configure(

            state="disabled"

        )



    # =========================================================

    # EDIT

    # =========================================================



    def start_edit_entry(self, entry_id):



        row = self.get_entry(

            entry_id

        )



        if row is None:



            messagebox.showerror(

                "Entry Not Found",

                "The selected entry could not be found."

            )



            return



        status = row[8]



        if status == "Approved":



            messagebox.showwarning(

                "Cannot Edit Entry",

                "Approved entries cannot be edited."

            )



            return



        (

            entry_id,

            student_id,

            database_date,

            week_number,

            activities,

            skills,

            challenges,

            supervisor_comment,

            status

        ) = row



        try:



            display_date = datetime.strptime(

                database_date,

                "%Y-%m-%d"

            ).strftime(

                "%d/%m/%Y"

            )



        except ValueError:



            display_date = database_date



        self.editing_entry_id = entry_id



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

            display_date

        )



        self.week_entry.delete(

            0,

            "end"

        )



        self.week_entry.insert(

            0,

            str(week_number)

        )



        self.activities_text.delete(

            "1.0",

            "end"

        )



        self.activities_text.insert(

            "1.0",

            activities or ""

        )



        self.skills_entry.delete(

            0,

            "end"

        )



        self.skills_entry.insert(

            0,

            skills or ""

        )



        self.challenges_text.delete(

            "1.0",

            "end"

        )



        self.challenges_text.insert(

            "1.0",

            challenges or ""

        )



        self.save_button.configure(

            text="Save Changes"

        )



        self.scroll_frame._parent_canvas.yview_moveto(

            0

        )



    # =========================================================

    # DELETE

    # =========================================================



    def delete_entry(self, entry_id):



        row = self.get_entry(

            entry_id

        )



        if row is None:



            messagebox.showerror(

                "Entry Not Found",

                "The selected entry could not be found."

            )



            return



        status = row[8]



        if status == "Approved":



            messagebox.showwarning(

                "Cannot Delete Entry",

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



            conn = get_connection()



            cursor = conn.cursor()



            cursor.execute(

                """

                DELETE FROM logbook_entries

                WHERE id = ?

                AND student_id = ?

                """,

                (

                    entry_id,

                    self.student_id

                )

            )



            conn.commit()



            conn.close()



            messagebox.showinfo(

                "Success",

                "Logbook entry deleted successfully."

            )



            self.load_entries()



        except Exception as error:



            messagebox.showerror(

                "Database Error",

                f"Could not delete the entry.\n\n{error}"

            )



    # =========================================================

    # STATUS

    # =========================================================



    def update_status(self, entry_id):



        role = self.user_data.get(

            "role",

            "student"

        )



        if role not in (

            "supervisor",

            "admin"

        ):



            messagebox.showwarning(

                "Access Denied",

                "Only supervisors and administrators can update "

                "logbook status."

            )



            return



        row = self.get_entry(

            entry_id

        )



        if row is None:



            messagebox.showerror(

                "Entry Not Found",

                "The selected entry could not be found."

            )



            return



        (

            entry_id,

            student_id,

            database_date,

            week_number,

            activities,

            skills,

            challenges,

            supervisor_comment,

            current_status

        ) = row



        dialog = ctk.CTkToplevel(

            self

        )



        dialog.title(

            "Update Logbook Status"

        )



        dialog.geometry(

            "520x500"

        )



        dialog.configure(

            fg_color=BACKGROUND

        )



        dialog.transient(

            self.winfo_toplevel()

        )



        dialog.grab_set()



        card = ctk.CTkFrame(

            dialog,

            fg_color=CARD,

            corner_radius=CORNER_RADIUS,

            border_width=1,

            border_color=BORDER

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

            font=("Arial", 20, "bold"),

            text_color=TEXT

        ).pack(

            anchor="w",

            padx=20,

            pady=(20, 5)

        )



        ctk.CTkLabel(

            card,

            text=f"Entry ID: {entry_id}",

            font=("Arial", 12),

            text_color=TEXT_LIGHT

        ).pack(

            anchor="w",

            padx=20,

            pady=(0, 15)

        )



        ctk.CTkLabel(

            card,

            text="Status",

            font=("Arial", 12, "bold"),

            text_color=TEXT

        ).pack(

            anchor="w",

            padx=20,

            pady=(0, 5)

        )



        status_choice = ctk.CTkComboBox(

            card,

            values=[

                "Pending",

                "Approved",

                "Rejected"

            ],

            height=42,

            fg_color=INPUT_BG,

            border_color=BORDER,

            button_color=NAVY_LIGHT,

            button_hover_color=NAVY,

            text_color=TEXT,

            corner_radius=8

        )



        status_choice.set(

            current_status

        )



        status_choice.pack(

            fill="x",

            padx=20

        )



        ctk.CTkLabel(

            card,

            text="Supervisor Comment",

            font=("Arial", 12, "bold"),

            text_color=TEXT

        ).pack(

            anchor="w",

            padx=20,

            pady=(15, 5)

        )



        comment_text = ctk.CTkTextbox(

            card,

            height=110,

            fg_color=INPUT_BG,

            border_color=BORDER,

            border_width=1,

            text_color=TEXT,

            corner_radius=8,

            wrap="word"

        )



        comment_text.pack(

            fill="x",

            padx=20

        )



        if supervisor_comment:



            comment_text.insert(

                "1.0",

                supervisor_comment

            )



        def save_status():



            new_status = status_choice.get()



            comment = comment_text.get(

                "1.0",

                "end"

            ).strip()



            try:



                conn = get_connection()



                cursor = conn.cursor()



                cursor.execute(

                    """

                    UPDATE logbook_entries

                    SET

                        status = ?,

                        supervisor_comment = ?

                    WHERE id = ?

                    """,

                    (

                        new_status,

                        comment,

                        entry_id

                    )

                )



                conn.commit()



                conn.close()



                dialog.destroy()



                messagebox.showinfo(

                    "Success",

                    "Logbook status updated successfully."

                )



                self.load_entries()



            except Exception as error:



                messagebox.showerror(

                    "Database Error",

                    f"Could not update status.\n\n{error}"

                )



        ctk.CTkButton(

            card,

            text="Update Status",

            height=42,

            fg_color=BLUE,

            hover_color=BLUE_HOVER,

            command=save_status,

            corner_radius=8

        ).pack(

            fill="x",

            padx=20,

            pady=20

        )



    # =========================================================

    # STATUS COLORS

    # =========================================================



    def get_status_color(self, status):



        if status == "Approved":

            return SUCCESS



        if status == "Rejected":

            return ERROR



        return WARNING



    def get_status_background(self, status):



        if status == "Approved":

            return "#DCFCE7"



        if status == "Rejected":

            return "#FEE2E2"



        return "#FEF3C7"
