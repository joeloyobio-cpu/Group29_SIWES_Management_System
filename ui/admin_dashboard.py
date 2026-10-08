import customtkinter as ctk
from tkinter import messagebox

from database.database import get_connection
from ui.theme import (
    NAVY,
    NAVY_LIGHT,
    BLUE,
    BLUE_HOVER,
    WHITE,
    BACKGROUND,
    CARD,
    TEXT,
    TEXT_LIGHT,
    BORDER,
    SUCCESS,
    SUCCESS_HOVER,
    ERROR,
    ERROR_HOVER,
    CORNER_RADIUS,
)


class AdminDashboard(ctk.CTkFrame):
    def __init__(self, user, logout_callback=None):
        self.window = ctk.CTk()
        self.window.title("SIWES Management System - Admin Dashboard")
        self.window.geometry("1200x750")
        self.window.minsize(1000, 650)

        super().__init__(master=self.window, fg_color=BACKGROUND)
        self.pack(fill="both", expand=True)

        self.user = user or {}
        self.logout_callback = logout_callback

        self._build_ui()
        self.refresh_data()

        self.window.mainloop()

    # =========================================================
    # MAIN UI
    # =========================================================

    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(
            self,
            fg_color=NAVY,
            corner_radius=0,
            height=80
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        left_header = ctk.CTkFrame(header, fg_color="transparent")
        left_header.pack(side="left", padx=30, pady=15)

        ctk.CTkLabel(
            left_header,
            text="SIWES Management System",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=WHITE
        ).pack(anchor="w")

        ctk.CTkLabel(
            left_header,
            text="Administrator Dashboard",
            font=ctk.CTkFont(size=13),
            text_color="#D7E3F0"
        ).pack(anchor="w")

        right_header = ctk.CTkFrame(header, fg_color="transparent")
        right_header.pack(side="right", padx=30)

        ctk.CTkLabel(
            right_header,
            text=f"Welcome, {self.user.get('full_name', 'Administrator')}",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=WHITE
        ).pack(side="left", padx=(0, 15))

        ctk.CTkButton(
            right_header,
            text="Logout",
            width=90,
            height=36,
            fg_color=ERROR,
            hover_color=ERROR_HOVER,
            corner_radius=8,
            command=self._logout
        ).pack(side="left")

        # Content
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=25)

        # Stats
        stats_frame = ctk.CTkFrame(content, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 20))

        self.org_count_label = self._create_stat_card(
            stats_frame,
            "Organizations",
            "0",
            0
        )

        self.supervisor_count_label = self._create_stat_card(
            stats_frame,
            "Supervisors",
            "0",
            1
        )

        self.student_count_label = self._create_stat_card(
            stats_frame,
            "Students",
            "0",
            2
        )

        self.placement_count_label = self._create_stat_card(
            stats_frame,
            "Placements",
            "0",
            3
        )

        # Management area
        management = ctk.CTkFrame(
            content,
            fg_color=CARD,
            corner_radius=CORNER_RADIUS,
            border_width=1,
            border_color=BORDER
        )
        management.pack(fill="both", expand=True)

        # Tabs
        self.tabview = ctk.CTkTabview(
            management,
            fg_color=CARD,
            segmented_button_fg_color=BACKGROUND,
            segmented_button_selected_color=BLUE,
            segmented_button_selected_hover_color=BLUE_HOVER
        )
        self.tabview.pack(fill="both", expand=True, padx=15, pady=15)

        self.tabview.add("Organizations")
        self.tabview.add("Supervisors")

        self._build_organizations_tab()
        self._build_supervisors_tab()

    # =========================================================
    # STAT CARD
    # =========================================================

    def _create_stat_card(self, parent, title, value, column):
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
            padx=(0 if column == 0 else 8, 8),
            sticky="nsew"
        )

        parent.grid_columnconfigure(column, weight=1)

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=13),
            text_color=TEXT_LIGHT
        ).pack(anchor="w", padx=18, pady=(15, 2))

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=NAVY
        )
        value_label.pack(anchor="w", padx=18, pady=(0, 15))

        return value_label

    # =========================================================
    # ORGANIZATIONS TAB
    # =========================================================

    def _build_organizations_tab(self):
        tab = self.tabview.tab("Organizations")

        top = ctk.CTkFrame(tab, fg_color="transparent")
        top.pack(fill="x", padx=10, pady=(5, 15))

        ctk.CTkLabel(
            top,
            text="Manage Internship Organizations",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT
        ).pack(side="left")

        ctk.CTkButton(
            top,
            text="+ Add Organization",
            width=160,
            height=38,
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
            command=self._add_organization
        ).pack(side="right")

        # List
        self.org_scroll = ctk.CTkScrollableFrame(
            tab,
            fg_color=BACKGROUND
        )
        self.org_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    # =========================================================
    # SUPERVISORS TAB
    # =========================================================

    def _build_supervisors_tab(self):
        tab = self.tabview.tab("Supervisors")

        top = ctk.CTkFrame(tab, fg_color="transparent")
        top.pack(fill="x", padx=10, pady=(5, 15))

        ctk.CTkLabel(
            top,
            text="Manage SIWES Supervisors",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT
        ).pack(side="left")

        ctk.CTkButton(
            top,
            text="+ Add Supervisor",
            width=150,
            height=38,
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
            command=self._add_supervisor
        ).pack(side="right")

        self.supervisor_scroll = ctk.CTkScrollableFrame(
            tab,
            fg_color=BACKGROUND
        )
        self.supervisor_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    # =========================================================
    # REFRESH DATA
    # =========================================================

    def refresh_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM organizations")
            organizations = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM supervisors")
            supervisors = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM students")
            students = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM placements")
            placements = cursor.fetchone()[0]

            conn.close()

            self.org_count_label.configure(text=str(organizations))
            self.supervisor_count_label.configure(text=str(supervisors))
            self.student_count_label.configure(text=str(students))
            self.placement_count_label.configure(text=str(placements))

            self._load_organizations()
            self._load_supervisors()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"Could not load admin data.\n\n{e}"
            )

    # =========================================================
    # LOAD ORGANIZATIONS
    # =========================================================

    def _load_organizations(self):
        for widget in self.org_scroll.winfo_children():
            widget.destroy()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, organization_name, address,
                   contact_person, email, phone
            FROM organizations
            ORDER BY organization_name
        """)

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            ctk.CTkLabel(
                self.org_scroll,
                text="No organizations have been added yet.",
                font=ctk.CTkFont(size=14),
                text_color=TEXT_LIGHT
            ).pack(pady=40)

            return

        for row in rows:
            self._organization_card(row)

    # =========================================================
    # LOAD SUPERVISORS
    # =========================================================

    def _load_supervisors(self):
        for widget in self.supervisor_scroll.winfo_children():
            widget.destroy()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, full_name, email, phone, department
            FROM supervisors
            ORDER BY full_name
        """)

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            ctk.CTkLabel(
                self.supervisor_scroll,
                text="No supervisors have been added yet.",
                font=ctk.CTkFont(size=14),
                text_color=TEXT_LIGHT
            ).pack(pady=40)

            return

        for row in rows:
            self._supervisor_card(row)

    # =========================================================
    # ORGANIZATION CARD
    # =========================================================

    def _organization_card(self, row):
        org_id, name, address, contact, email, phone = row

        card = ctk.CTkFrame(
            self.org_scroll,
            fg_color=CARD,
            corner_radius=10,
            border_width=1,
            border_color=BORDER
        )
        card.pack(fill="x", pady=6)

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True, padx=15, pady=12)

        ctk.CTkLabel(
            info,
            text=name,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=TEXT
        ).pack(anchor="w")

        details = f"Address: {address or '-'}\n"
        details += f"Contact: {contact or '-'}\n"
        details += f"Email: {email or '-'}    Phone: {phone or '-'}"

        ctk.CTkLabel(
            info,
            text=details,
            justify="left",
            anchor="w",
            font=ctk.CTkFont(size=12),
            text_color=TEXT_LIGHT
        ).pack(anchor="w", pady=(5, 0))

        ctk.CTkButton(
            card,
            text="Delete",
            width=80,
            height=34,
            fg_color=ERROR,
            hover_color=ERROR_HOVER,
            command=lambda i=org_id: self._delete_organization(i)
        ).pack(side="right", padx=15)

    # =========================================================
    # SUPERVISOR CARD
    # =========================================================

    def _supervisor_card(self, row):
        supervisor_id, name, email, phone, department = row

        card = ctk.CTkFrame(
            self.supervisor_scroll,
            fg_color=CARD,
            corner_radius=10,
            border_width=1,
            border_color=BORDER
        )
        card.pack(fill="x", pady=6)

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True, padx=15, pady=12)

        ctk.CTkLabel(
            info,
            text=name,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=TEXT
        ).pack(anchor="w")

        details = f"Email: {email or '-'}\n"
        details += f"Phone: {phone or '-'}    Department: {department or '-'}"

        ctk.CTkLabel(
            info,
            text=details,
            justify="left",
            anchor="w",
            font=ctk.CTkFont(size=12),
            text_color=TEXT_LIGHT
        ).pack(anchor="w", pady=(5, 0))

        ctk.CTkButton(
            card,
            text="Delete",
            width=80,
            height=34,
            fg_color=ERROR,
            hover_color=ERROR_HOVER,
            command=lambda i=supervisor_id: self._delete_supervisor(i)
        ).pack(side="right", padx=15)

    # =========================================================
    # ADD ORGANIZATION
    # =========================================================

    def _add_organization(self):
        dialog = ctk.CTkToplevel(self.window)
        dialog.title("Add Organization")
        dialog.geometry("500x560")
        dialog.resizable(False, False)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="Add Internship Organization",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=NAVY
        ).pack(pady=(25, 20))

        fields = {}

        field_data = [
            ("Organization Name *", "name"),
            ("Address", "address"),
            ("Contact Person", "contact"),
            ("Email", "email"),
            ("Phone", "phone"),
        ]

        for label_text, key in field_data:
            ctk.CTkLabel(
                dialog,
                text=label_text,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=TEXT
            ).pack(anchor="w", padx=35, pady=(8, 4))

            entry = ctk.CTkEntry(
                dialog,
                height=40,
                corner_radius=8,
                border_color=BORDER
            )
            entry.pack(fill="x", padx=35)

            fields[key] = entry

        def save():
            name = fields["name"].get().strip()

            if not name:
                messagebox.showwarning(
                    "Required Field",
                    "Organization name is required.",
                    parent=dialog
                )
                return

            try:
                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO organizations
                    (organization_name, address, contact_person, email, phone)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    name,
                    fields["address"].get().strip(),
                    fields["contact"].get().strip(),
                    fields["email"].get().strip(),
                    fields["phone"].get().strip()
                ))

                conn.commit()
                conn.close()

                dialog.destroy()
                self.refresh_data()

                messagebox.showinfo(
                    "Success",
                    "Organization added successfully."
                )

            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Could not add organization.\n\n{e}",
                    parent=dialog
                )

        ctk.CTkButton(
            dialog,
            text="Save Organization",
            height=42,
            fg_color=SUCCESS,
            hover_color=SUCCESS_HOVER,
            command=save
        ).pack(fill="x", padx=35, pady=25)

    # =========================================================
    # ADD SUPERVISOR
    # =========================================================

    def _add_supervisor(self):
        dialog = ctk.CTkToplevel(self.window)
        dialog.title("Add Supervisor")
        dialog.geometry("500x500")
        dialog.resizable(False, False)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="Add SIWES Supervisor",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=NAVY
        ).pack(pady=(25, 20))

        fields = {}

        field_data = [
            ("Full Name *", "name"),
            ("Email", "email"),
            ("Phone", "phone"),
            ("Department", "department"),
        ]

        for label_text, key in field_data:
            ctk.CTkLabel(
                dialog,
                text=label_text,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=TEXT
            ).pack(anchor="w", padx=35, pady=(8, 4))

            entry = ctk.CTkEntry(
                dialog,
                height=40,
                corner_radius=8,
                border_color=BORDER
            )
            entry.pack(fill="x", padx=35)

            fields[key] = entry

        def save():
            name = fields["name"].get().strip()

            if not name:
                messagebox.showwarning(
                    "Required Field",
                    "Supervisor name is required.",
                    parent=dialog
                )
                return

            try:
                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO supervisors
                    (full_name, email, phone, department)
                    VALUES (?, ?, ?, ?)
                """, (
                    name,
                    fields["email"].get().strip(),
                    fields["phone"].get().strip(),
                    fields["department"].get().strip()
                ))

                conn.commit()
                conn.close()

                dialog.destroy()
                self.refresh_data()

                messagebox.showinfo(
                    "Success",
                    "Supervisor added successfully."
                )

            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Could not add supervisor.\n\n{e}",
                    parent=dialog
                )

        ctk.CTkButton(
            dialog,
            text="Save Supervisor",
            height=42,
            fg_color=SUCCESS,
            hover_color=SUCCESS_HOVER,
            command=save
        ).pack(fill="x", padx=35, pady=25)

    # =========================================================
    # DELETE ORGANIZATION
    # =========================================================

    def _delete_organization(self, organization_id):
        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this organization?"
        )

        if not confirm:
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM organizations WHERE id = ?",
                (organization_id,)
            )

            conn.commit()
            conn.close()

            self.refresh_data()

        except Exception as e:
            messagebox.showerror(
                "Delete Error",
                f"Could not delete organization.\n\n{e}"
            )

    # =========================================================
    # DELETE SUPERVISOR
    # =========================================================

    def _delete_supervisor(self, supervisor_id):
        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this supervisor?"
        )

        if not confirm:
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM supervisors WHERE id = ?",
                (supervisor_id,)
            )

            conn.commit()
            conn.close()

            self.refresh_data()

        except Exception as e:
            messagebox.showerror(
                "Delete Error",
                f"Could not delete supervisor.\n\n{e}"
            )

    # =========================================================
    # LOGOUT
    # =========================================================

    def _logout(self):
        try:
            self.window.destroy()
        except Exception:
            pass

        if self.logout_callback:
            self.logout_callback()


if __name__ == "__main__":
    test_user = {
        "id": 1,
        "username": "admin1",
        "full_name": "Administrator",
        "email": "admin@siwes.com",
        "role": "admin"
    }

    AdminDashboard(test_user)