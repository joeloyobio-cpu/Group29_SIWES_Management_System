import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

DB_PATH = "SIWES.db"

# Temporary compatibility layer.
# When the group leader provides the central database.py,
# replace this function with:
#     from database import get_connection
#     return get_connection()
def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_placement_tables():
    """Create only the tables needed by Placement Management.
    Safe to run against an existing central SIWES.db."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            address TEXT,
            contact_person TEXT,
            phone TEXT,
            email TEXT,
            industry TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS placements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            organization_id INTEGER NOT NULL,
            supervisor_id INTEGER,
            start_date TEXT NOT NULL,
            end_date TEXT,
            status TEXT NOT NULL DEFAULT 'Pending',
            remarks TEXT,
            FOREIGN KEY (organization_id) REFERENCES organizations(id)
        )
    """)

    conn.commit()
    conn.close()


class PlacementManager(tk.Toplevel):
    """Standalone Placement Management window.

    Expected integration:
        PlacementManager(parent, student_id=current_user_id)

    If your project's student/supervisor table uses different names,
    adjust only load_students/load_supervisors.
    """

    STATUSES = ("Pending", "Active", "Completed", "Cancelled")

    def __init__(self, parent=None, student_id=None):
        super().__init__(parent)
        self.parent = parent
        self.current_student_id = student_id
        self.title("SIWES Placement & Organization Management")
        self.geometry("1100x700")
        self.minsize(950, 600)

        initialize_placement_tables()
        self._build_ui()
        self.refresh_all()

    def _build_ui(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=12)

        self.org_tab = ttk.Frame(self.notebook, padding=12)
        self.place_tab = ttk.Frame(self.notebook, padding=12)
        self.view_tab = ttk.Frame(self.notebook, padding=12)

        self.notebook.add(self.org_tab, text="Organizations")
        self.notebook.add(self.place_tab, text="Create Placement")
        self.notebook.add(self.view_tab, text="Placement Records")

        self._build_org_tab()
        self._build_place_tab()
        self._build_view_tab()

    # ---------- Organizations ----------
    def _build_org_tab(self):
        form = ttk.LabelFrame(self.org_tab, text="Organization Details", padding=12)
        form.pack(fill="x")

        labels = [
            ("Organization Name", "org_name"),
            ("Address", "address"),
            ("Contact Person", "contact"),
            ("Phone", "phone"),
            ("Email", "email"),
            ("Industry / Type", "industry"),
        ]
        self.org_vars = {key: tk.StringVar() for _, key in labels}

        for i, (label, key) in enumerate(labels):
            ttk.Label(form, text=label).grid(row=i // 2, column=(i % 2) * 2,
                                             sticky="w", padx=6, pady=6)
            ttk.Entry(form, textvariable=self.org_vars[key], width=38).grid(
                row=i // 2, column=(i % 2) * 2 + 1, sticky="ew", padx=6, pady=6
            )

        ttk.Button(form, text="Add Organization",
                   command=self.add_organization).grid(
            row=3, column=0, columnspan=4, pady=10
        )

        table_frame = ttk.LabelFrame(self.org_tab, text="Organizations", padding=8)
        table_frame.pack(fill="both", expand=True, pady=(12, 0))

        cols = ("id", "name", "address", "contact", "phone", "email", "industry")
        self.org_tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        headings = {
            "id": "ID", "name": "Organization", "address": "Address",
            "contact": "Contact", "phone": "Phone", "email": "Email",
            "industry": "Industry"
        }
        widths = {"id": 50, "name": 180, "address": 200, "contact": 140,
                  "phone": 120, "email": 180, "industry": 120}

        for c in cols:
            self.org_tree.heading(c, text=headings[c])
            self.org_tree.column(c, width=widths[c], anchor="w")

        scroll = ttk.Scrollbar(table_frame, orient="vertical",
                               command=self.org_tree.yview)
        self.org_tree.configure(yscrollcommand=scroll.set)
        self.org_tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def add_organization(self):
        name = self.org_vars["org_name"].get().strip()
        if not name:
            messagebox.showwarning("Required", "Organization name is required.")
            return

        conn = get_connection()
        try:
            conn.execute("""
                INSERT INTO organizations
                (name, address, contact_person, phone, email, industry)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                name,
                self.org_vars["address"].get().strip(),
                self.org_vars["contact"].get().strip(),
                self.org_vars["phone"].get().strip(),
                self.org_vars["email"].get().strip(),
                self.org_vars["industry"].get().strip(),
            ))
            conn.commit()
            messagebox.showinfo("Success", "Organization added successfully.")
            for v in self.org_vars.values():
                v.set("")
            self.refresh_organizations()
            self.refresh_organization_combo()
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicate",
                                 "An organization with that name already exists.")
        finally:
            conn.close()

    # ---------- Placement ----------
    def _build_place_tab(self):
        form = ttk.LabelFrame(self.place_tab, text="Placement Details", padding=15)
        form.pack(fill="x")

        self.student_var = tk.StringVar()
        self.org_var = tk.StringVar()
        self.supervisor_var = tk.StringVar()
        self.start_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.end_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Pending")
        self.remarks_var = tk.StringVar()

        fields = [
            ("Student ID", self.student_var),
            ("Organization", self.org_var),
            ("Supervisor ID", self.supervisor_var),
            ("Start Date (YYYY-MM-DD)", self.start_var),
            ("End Date (YYYY-MM-DD)", self.end_var),
            ("Status", self.status_var),
            ("Remarks", self.remarks_var),
        ]

        for i, (label, var) in enumerate(fields):
            ttk.Label(form, text=label).grid(row=i, column=0,
                                             sticky="w", padx=6, pady=7)
            if label == "Organization":
                self.org_combo = ttk.Combobox(
                    form, textvariable=var, state="readonly", width=42
                )
                self.org_combo.grid(row=i, column=1, sticky="w",
                                    padx=6, pady=7)
            elif label == "Status":
                ttk.Combobox(
                    form, textvariable=var, values=self.STATUSES,
                    state="readonly", width=40
                ).grid(row=i, column=1, sticky="w", padx=6, pady=7)
            else:
                ttk.Entry(form, textvariable=var, width=45).grid(
                    row=i, column=1, sticky="w", padx=6, pady=7
                )

        ttk.Button(form, text="Save Placement",
                   command=self.save_placement).grid(
            row=len(fields), column=0, columnspan=2, pady=15
        )

        note = (
            "Integration note: Student ID and Supervisor ID are kept as IDs "
            "so this module can connect cleanly to the team's central "
            "students/supervisors tables."
        )
        ttk.Label(self.place_tab, text=note, wraplength=850).pack(
            anchor="w", pady=15
        )

    def refresh_organization_combo(self):
        if not hasattr(self, "org_combo"):
            return
        conn = get_connection()
        rows = conn.execute(
            "SELECT id, name FROM organizations ORDER BY name"
        ).fetchall()
        conn.close()
        self.org_combo["values"] = [
            f"{row[0]} - {row[1]}" for row in rows
        ]

    def save_placement(self):
        student_text = self.student_var.get().strip()
        org_text = self.org_var.get().strip()
        start = self.start_var.get().strip()
        end = self.end_var.get().strip()

        if not student_text or not org_text or not start:
            messagebox.showwarning(
                "Required",
                "Student ID, organization and start date are required."
            )
            return

        try:
            student_id = int(student_text)
        except ValueError:
            messagebox.showerror("Invalid Student ID",
                                 "Student ID must be a number.")
            return

        try:
            organization_id = int(org_text.split(" - ", 1)[0])
        except (ValueError, IndexError):
            messagebox.showerror("Invalid Organization",
                                 "Please select an organization.")
            return

        supervisor_id = self.supervisor_var.get().strip() or None
        if supervisor_id:
            try:
                supervisor_id = int(supervisor_id)
            except ValueError:
                messagebox.showerror("Invalid Supervisor ID",
                                     "Supervisor ID must be a number.")
                return

        for date_text, label in ((start, "Start date"), (end, "End date")):
            if date_text:
                try:
                    datetime.strptime(date_text, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror(
                        "Invalid Date",
                        f"{label} must use YYYY-MM-DD."
                    )
                    return

        conn = get_connection()
        conn.execute("""
            INSERT INTO placements
            (student_id, organization_id, supervisor_id,
             start_date, end_date, status, remarks)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            student_id,
            organization_id,
            supervisor_id,
            start,
            end or None,
            self.status_var.get(),
            self.remarks_var.get().strip()
        ))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Placement saved successfully.")
        self.refresh_placements()

        self.student_var.set("")
        self.supervisor_var.set("")
        self.end_var.set("")
        self.status_var.set("Pending")
        self.remarks_var.set("")

    # ---------- Records ----------
    def _build_view_tab(self):
        top = ttk.Frame(self.view_tab)
        top.pack(fill="x", pady=(0, 8))

        ttk.Button(top, text="Refresh", command=self.refresh_placements).pack(
            side="left"
        )

        frame = ttk.Frame(self.view_tab)
        frame.pack(fill="both", expand=True)

        cols = (
            "id", "student_id", "organization", "supervisor_id",
            "start", "end", "status", "remarks"
        )
        self.place_tree = ttk.Treeview(frame, columns=cols, show="headings")

        headings = {
            "id": "ID", "student_id": "Student ID",
            "organization": "Organization", "supervisor_id": "Supervisor ID",
            "start": "Start", "end": "End", "status": "Status",
            "remarks": "Remarks"
        }
        widths = {
            "id": 50, "student_id": 90, "organization": 200,
            "supervisor_id": 110, "start": 100, "end": 100,
            "status": 100, "remarks": 220
        }

        for c in cols:
            self.place_tree.heading(c, text=headings[c])
            self.place_tree.column(c, width=widths[c], anchor="w")

        yscroll = ttk.Scrollbar(frame, orient="vertical",
                                command=self.place_tree.yview)
        xscroll = ttk.Scrollbar(frame, orient="horizontal",
                                command=self.place_tree.xview)
        self.place_tree.configure(
            yscrollcommand=yscroll.set,
            xscrollcommand=xscroll.set
        )

        self.place_tree.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        actions = ttk.Frame(self.view_tab)
        actions.pack(fill="x", pady=10)

        ttk.Button(actions, text="Set Active",
                   command=lambda: self.update_status("Active")).pack(
            side="left", padx=4
        )
        ttk.Button(actions, text="Set Completed",
                   command=lambda: self.update_status("Completed")).pack(
            side="left", padx=4
        )
        ttk.Button(actions, text="Cancel Placement",
                   command=lambda: self.update_status("Cancelled")).pack(
            side="left", padx=4
        )
        ttk.Button(actions, text="Delete Placement",
                   command=self.delete_placement).pack(
            side="right", padx=4
        )

    def refresh_organizations(self):
        for item in self.org_tree.get_children():
            self.org_tree.delete(item)

        conn = get_connection()
        rows = conn.execute("""
            SELECT id, name, address, contact_person, phone, email, industry
            FROM organizations
            ORDER BY name
        """).fetchall()
        conn.close()

        for row in rows:
            self.org_tree.insert("", "end", values=row)

    def refresh_placements(self):
        if not hasattr(self, "place_tree"):
            return

        for item in self.place_tree.get_children():
            self.place_tree.delete(item)

        conn = get_connection()
        rows = conn.execute("""
            SELECT p.id, p.student_id, o.name, p.supervisor_id,
                   p.start_date, p.end_date, p.status, p.remarks
            FROM placements p
            JOIN organizations o ON o.id = p.organization_id
            ORDER BY p.id DESC
        """).fetchall()
        conn.close()

        for row in rows:
            self.place_tree.insert("", "end", values=row)

    def update_status(self, status):
        selected = self.place_tree.selection()
        if not selected:
            messagebox.showwarning("Select Placement",
                                   "Select a placement first.")
            return

        placement_id = self.place_tree.item(selected[0], "values")[0]

        conn = get_connection()
        conn.execute(
            "UPDATE placements SET status = ? WHERE id = ?",
            (status, placement_id)
        )
        conn.commit()
        conn.close()

        self.refresh_placements()

    def delete_placement(self):
        selected = self.place_tree.selection()
        if not selected:
            messagebox.showwarning("Select Placement",
                                   "Select a placement first.")
            return

        placement_id = self.place_tree.item(selected[0], "values")[0]

        if not messagebox.askyesno(
            "Confirm Delete",
            "Delete this placement record?"
        ):
            return

        conn = get_connection()
        conn.execute("DELETE FROM placements WHERE id = ?", (placement_id,))
        conn.commit()
        conn.close()
        self.refresh_placements()

    def refresh_all(self):
        self.refresh_organizations()
        self.refresh_organization_combo()
        self.refresh_placements()


def open_placement(parent=None, student_id=None):
    return PlacementManager(parent, student_id)
