import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

from database.database import get_connection
from ui.theme import (
    BACKGROUND,
    CARD,
    TEXT,
    TEXT_LIGHT,
    BLUE,
    BLUE_HOVER,
    SUCCESS,
    WARNING,
    BORDER,
    CORNER_RADIUS,
)
from ui.components import (
    PageHeader,
    Card,
    SectionHeader,
    PrimaryButton,
    SecondaryButton,
)


class PlacementPage(ctk.CTkFrame):
    """
    SIWES Placement Management Page.

    Uses the central SIWES.db database and the existing:
        organizations
        supervisors
        students
        placements
    tables.
    """

    def __init__(self, parent, user_data=None):
        super().__init__(parent, fg_color=BACKGROUND)

        self.user_data = user_data or {}

        self.student_id = None
        self.current_placement_id = None

        self.organizations = []
        self.supervisors = []

        self._build_ui()
        self._load_data()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self):
        header = PageHeader(
            self,
            title="SIWES Placement",
            subtitle="Manage your internship organization, supervisor and placement period."
        )
        header.pack(
            fill="x",
            padx=24,
            pady=(20, 12)
        )

        content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        content.pack(
            fill="both",
            expand=True,
            padx=24,
            pady=(0, 24)
        )

        # =====================================================
        # CURRENT PLACEMENT
        # =====================================================

        current_card = Card(content)
        current_card.pack(
            fill="x",
            pady=(0, 16)
        )

        SectionHeader(
            current_card,
            title="Current Placement",
            subtitle="Your current SIWES placement status."
        ).pack(
            fill="x",
            padx=20,
            pady=(18, 10)
        )

        self.current_status = ctk.CTkLabel(
            current_card,
            text="No placement record found.",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color=TEXT_LIGHT
        )
        self.current_status.pack(
            anchor="w",
            padx=20,
            pady=(0, 18)
        )

        # =====================================================
        # PLACEMENT FORM
        # =====================================================

        form_card = Card(content)
        form_card.pack(
            fill="both",
            expand=True
        )

        SectionHeader(
            form_card,
            title="Placement Details",
            subtitle="Enter the details of your SIWES placement."
        ).pack(
            fill="x",
            padx=20,
            pady=(18, 12)
        )

        form = ctk.CTkFrame(
            form_card,
            fg_color="transparent"
        )
        form.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        form.grid_columnconfigure(0, weight=1)
        form.grid_columnconfigure(1, weight=1)

        # =====================================================
        # ORGANIZATION
        # =====================================================

        ctk.CTkLabel(
            form,
            text="Organization",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=TEXT
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 12),
            pady=(0, 6)
        )

        self.organization_combo = ctk.CTkComboBox(
            form,
            values=["Loading..."],
            height=42,
            corner_radius=CORNER_RADIUS,
            border_color=BORDER,
            fg_color=CARD,
            button_color=BLUE,
            button_hover_color=BLUE_HOVER,
            text_color=TEXT,
            state="readonly",
            command=self._organization_selected
        )
        self.organization_combo.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 12),
            pady=(0, 8)
        )

        self.organization_info = ctk.CTkLabel(
            form,
            text="Select an organization.",
            font=ctk.CTkFont(size=12),
            text_color=TEXT_LIGHT,
            justify="left",
            anchor="w"
        )
        self.organization_info.grid(
            row=2,
            column=0,
            sticky="w",
            padx=(0, 12),
            pady=(0, 18)
        )

        # =====================================================
        # SUPERVISOR
        # =====================================================

        ctk.CTkLabel(
            form,
            text="Supervisor",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=TEXT
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=(12, 0),
            pady=(0, 6)
        )

        self.supervisor_combo = ctk.CTkComboBox(
            form,
            values=["Loading..."],
            height=42,
            corner_radius=CORNER_RADIUS,
            border_color=BORDER,
            fg_color=CARD,
            button_color=BLUE,
            button_hover_color=BLUE_HOVER,
            text_color=TEXT,
            state="readonly",
            command=self._supervisor_selected
        )
        self.supervisor_combo.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(12, 0),
            pady=(0, 8)
        )

        self.supervisor_info = ctk.CTkLabel(
            form,
            text="Select a supervisor.",
            font=ctk.CTkFont(size=12),
            text_color=TEXT_LIGHT,
            justify="left",
            anchor="w"
        )
        self.supervisor_info.grid(
            row=2,
            column=1,
            sticky="w",
            padx=(12, 0),
            pady=(0, 18)
        )

        # =====================================================
        # START DATE
        # =====================================================

        ctk.CTkLabel(
            form,
            text="Start Date",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=TEXT
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=(0, 12),
            pady=(0, 6)
        )

        self.start_date_entry = ctk.CTkEntry(
            form,
            placeholder_text="DD/MM/YYYY",
            height=42,
            corner_radius=CORNER_RADIUS,
            border_color=BORDER,
            fg_color=CARD,
            text_color=TEXT
        )
        self.start_date_entry.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=(0, 12),
            pady=(0, 18)
        )

        # =====================================================
        # END DATE
        # =====================================================

        ctk.CTkLabel(
            form,
            text="End Date",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=TEXT
        ).grid(
            row=3,
            column=1,
            sticky="w",
            padx=(12, 0),
            pady=(0, 6)
        )

        self.end_date_entry = ctk.CTkEntry(
            form,
            placeholder_text="DD/MM/YYYY",
            height=42,
            corner_radius=CORNER_RADIUS,
            border_color=BORDER,
            fg_color=CARD,
            text_color=TEXT
        )
        self.end_date_entry.grid(
            row=4,
            column=1,
            sticky="ew",
            padx=(12, 0),
            pady=(0, 18)
        )

        # =====================================================
        # STATUS
        # =====================================================

        ctk.CTkLabel(
            form,
            text="Placement Status",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=TEXT
        ).grid(
            row=5,
            column=0,
            sticky="w",
            padx=(0, 12),
            pady=(0, 6)
        )

        self.status_combo = ctk.CTkComboBox(
            form,
            values=[
                "Pending",
                "Active",
                "Completed",
                "Cancelled"
            ],
            height=42,
            corner_radius=CORNER_RADIUS,
            border_color=BORDER,
            fg_color=CARD,
            button_color=BLUE,
            button_hover_color=BLUE_HOVER,
            text_color=TEXT,
            state="readonly"
        )
        self.status_combo.set("Pending")
        self.status_combo.grid(
            row=6,
            column=0,
            sticky="ew",
            padx=(0, 12),
            pady=(0, 20)
        )

        # =====================================================
        # BUTTONS
        # =====================================================

        buttons = ctk.CTkFrame(
            form_card,
            fg_color="transparent"
        )
        buttons.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        SecondaryButton(
            buttons,
            text="Clear",
            command=self._clear_form
        ).pack(
            side="left"
        )

        self.save_button = PrimaryButton(
            buttons,
            text="Save Placement",
            command=self._save_placement
        )
        self.save_button.pack(
            side="right"
        )

    # =========================================================
    # LOAD DATA
    # =========================================================

    def _load_data(self):
        try:
            conn = get_connection()

            self._find_student(conn)
            self._load_organizations(conn)
            self._load_supervisors(conn)

            if self.student_id:
                self._load_existing_placement(conn)

            conn.close()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"Unable to load placement information.\n\n{e}"
            )

    # =========================================================
    # FIND STUDENT
    # =========================================================

    def _find_student(self, conn):
        """
        Find the student using the logged-in user's email.

        The actual students table contains:
            id
            full_name
            email
            ...
        """

        email = self.user_data.get("email")

        if not email:
            return

        row = conn.execute(
            """
            SELECT id
            FROM students
            WHERE email = ?
            LIMIT 1
            """,
            (email,)
        ).fetchone()

        if row:
            self.student_id = row[0]

    # =========================================================
    # ORGANIZATIONS
    # =========================================================

    def _load_organizations(self, conn):
        rows = conn.execute(
            """
            SELECT
                id,
                organization_name,
                address,
                contact_person,
                email,
                phone
            FROM organizations
            ORDER BY organization_name
            """
        ).fetchall()

        self.organizations = rows

        names = [
            row[1]
            for row in rows
        ]

        if names:
            self.organization_combo.configure(
                values=names
            )
            self.organization_combo.set(
                names[0]
            )
            self._organization_selected(
                names[0]
            )
        else:
            self.organization_combo.configure(
                values=["No organizations available"]
            )
            self.organization_combo.set(
                "No organizations available"
            )

    # =========================================================
    # SUPERVISORS
    # =========================================================

    def _load_supervisors(self, conn):
        rows = conn.execute(
            """
            SELECT
                id,
                full_name,
                email,
                phone,
                department
            FROM supervisors
            ORDER BY full_name
            """
        ).fetchall()

        self.supervisors = rows

        names = [
            row[1]
            for row in rows
        ]

        if names:
            self.supervisor_combo.configure(
                values=names
            )
            self.supervisor_combo.set(
                names[0]
            )
            self._supervisor_selected(
                names[0]
            )
        else:
            self.supervisor_combo.configure(
                values=["No supervisors available"]
            )
            self.supervisor_combo.set(
                "No supervisors available"
            )

    # =========================================================
    # EXISTING PLACEMENT
    # =========================================================

    def _load_existing_placement(self, conn):
        row = conn.execute(
            """
            SELECT
                id,
                organization_id,
                supervisor_id,
                start_date,
                end_date,
                status
            FROM placements
            WHERE student_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (self.student_id,)
        ).fetchone()

        if not row:
            self.current_status.configure(
                text="No placement record found.",
                text_color=TEXT_LIGHT
            )
            return

        (
            placement_id,
            organization_id,
            supervisor_id,
            start_date,
            end_date,
            status
        ) = row

        self.current_placement_id = placement_id

        # Select organization
        for organization in self.organizations:
            if organization[0] == organization_id:
                self.organization_combo.set(
                    organization[1]
                )
                self._organization_selected(
                    organization[1]
                )
                break

        # Select supervisor
        for supervisor in self.supervisors:
            if supervisor[0] == supervisor_id:
                self.supervisor_combo.set(
                    supervisor[1]
                )
                self._supervisor_selected(
                    supervisor[1]
                )
                break

        # Dates
        self.start_date_entry.delete(
            0,
            "end"
        )
        self.start_date_entry.insert(
            0,
            self._display_date(start_date)
        )

        self.end_date_entry.delete(
            0,
            "end"
        )
        self.end_date_entry.insert(
            0,
            self._display_date(end_date)
        )

        self.status_combo.set(
            status or "Pending"
        )

        self.current_status.configure(
            text=f"Placement Status: {status or 'Pending'}",
            text_color=self._status_color(
                status
            )
        )

        self.save_button.configure(
            text="Update Placement"
        )

    # =========================================================
    # ORGANIZATION SELECTION
    # =========================================================

    def _organization_selected(self, selected_name):
        for organization in self.organizations:

            if organization[1] == selected_name:

                (
                    _id,
                    name,
                    address,
                    contact_person,
                    email,
                    phone
                ) = organization

                info = (
                    f"{name}\n"
                    f"Address: {address or 'N/A'}\n"
                    f"Contact: {contact_person or 'N/A'}\n"
                    f"Email: {email or 'N/A'}\n"
                    f"Phone: {phone or 'N/A'}"
                )

                self.organization_info.configure(
                    text=info
                )

                break

    # =========================================================
    # SUPERVISOR SELECTION
    # =========================================================

    def _supervisor_selected(self, selected_name):
        for supervisor in self.supervisors:

            if supervisor[1] == selected_name:

                (
                    _id,
                    full_name,
                    email,
                    phone,
                    department
                ) = supervisor

                info = (
                    f"{full_name}\n"
                    f"Department: {department or 'N/A'}\n"
                    f"Email: {email or 'N/A'}\n"
                    f"Phone: {phone or 'N/A'}"
                )

                self.supervisor_info.configure(
                    text=info
                )

                break

    # =========================================================
    # SAVE / UPDATE PLACEMENT
    # =========================================================

    def _save_placement(self):

        if not self.student_id:
            messagebox.showwarning(
                "Student Record Required",
                "No student record is linked to this account.\n\n"
                "Please complete Student Information first."
            )
            return

        organization_name = (
            self.organization_combo.get().strip()
        )

        supervisor_name = (
            self.supervisor_combo.get().strip()
        )

        if (
            not organization_name
            or organization_name == "No organizations available"
        ):
            messagebox.showwarning(
                "Organization Required",
                "Please select an organization."
            )
            return

        if (
            not supervisor_name
            or supervisor_name == "No supervisors available"
        ):
            messagebox.showwarning(
                "Supervisor Required",
                "Please select a supervisor."
            )
            return

        start_text = (
            self.start_date_entry.get().strip()
        )

        end_text = (
            self.end_date_entry.get().strip()
        )

        status = (
            self.status_combo.get().strip()
        )

        # -----------------------------------------------------
        # Validate dates
        # -----------------------------------------------------

        try:
            start_date = datetime.strptime(
                start_text,
                "%d/%m/%Y"
            )

            end_date = datetime.strptime(
                end_text,
                "%d/%m/%Y"
            )

        except ValueError:
            messagebox.showwarning(
                "Invalid Date",
                "Please enter dates using:\n\n"
                "DD/MM/YYYY\n\n"
                "Example: 06/10/2026"
            )
            return

        if end_date < start_date:
            messagebox.showwarning(
                "Invalid Dates",
                "The end date cannot be earlier than the start date."
            )
            return

        # -----------------------------------------------------
        # Find IDs
        # -----------------------------------------------------

        organization_id = None
        supervisor_id = None

        for organization in self.organizations:
            if organization[1] == organization_name:
                organization_id = organization[0]
                break

        for supervisor in self.supervisors:
            if supervisor[1] == supervisor_name:
                supervisor_id = supervisor[0]
                break

        if organization_id is None:
            messagebox.showerror(
                "Error",
                "Selected organization could not be found."
            )
            return

        if supervisor_id is None:
            messagebox.showerror(
                "Error",
                "Selected supervisor could not be found."
            )
            return

        # -----------------------------------------------------
        # Convert dates to SQLite format
        # -----------------------------------------------------

        start_db = start_date.strftime(
            "%Y-%m-%d"
        )

        end_db = end_date.strftime(
            "%Y-%m-%d"
        )

        try:
            conn = get_connection()

            if self.current_placement_id:

                conn.execute(
                    """
                    UPDATE placements
                    SET
                        organization_id = ?,
                        supervisor_id = ?,
                        start_date = ?,
                        end_date = ?,
                        status = ?
                    WHERE id = ?
                    """,
                    (
                        organization_id,
                        supervisor_id,
                        start_db,
                        end_db,
                        status,
                        self.current_placement_id
                    )
                )

                message = (
                    "Placement updated successfully."
                )

            else:

                cursor = conn.execute(
                    """
                    INSERT INTO placements (
                        student_id,
                        organization_id,
                        supervisor_id,
                        start_date,
                        end_date,
                        status
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        self.student_id,
                        organization_id,
                        supervisor_id,
                        start_db,
                        end_db,
                        status
                    )
                )

                self.current_placement_id = (
                    cursor.lastrowid
                )

                message = (
                    "Placement saved successfully."
                )

            conn.commit()
            conn.close()

            self.current_status.configure(
                text=f"Placement Status: {status}",
                text_color=self._status_color(
                    status
                )
            )

            self.save_button.configure(
                text="Update Placement"
            )

            messagebox.showinfo(
                "Success",
                message
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to save placement.\n\n{e}"
            )

    # =========================================================
    # CLEAR FORM
    # =========================================================

    def _clear_form(self):

        if self.organizations:
            self.organization_combo.set(
                self.organizations[0][1]
            )

            self._organization_selected(
                self.organizations[0][1]
            )

        if self.supervisors:
            self.supervisor_combo.set(
                self.supervisors[0][1]
            )

            self._supervisor_selected(
                self.supervisors[0][1]
            )

        self.start_date_entry.delete(
            0,
            "end"
        )

        self.end_date_entry.delete(
            0,
            "end"
        )

        self.status_combo.set(
            "Pending"
        )

    # =========================================================
    # HELPERS
    # =========================================================

    @staticmethod
    def _display_date(value):

        if not value:
            return ""

        try:
            return datetime.strptime(
                value,
                "%Y-%m-%d"
            ).strftime(
                "%d/%m/%Y"
            )

        except ValueError:
            return value

    @staticmethod
    def _status_color(status):

        if status == "Active":
            return SUCCESS

        if status == "Completed":
            return BLUE

        if status == "Cancelled":
            return "#DC2626"

        return WARNING


# =============================================================
# STANDALONE TEST
# =============================================================

if __name__ == "__main__":

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()

    app.geometry(
        "1100x750"
    )

    app.title(
        "SIWES Placement"
    )

    page = PlacementPage(
        app,
        user_data={}
    )

    page.pack(
        fill="both",
        expand=True
    )

    app.mainloop()