"""
SIWES Attendance Management Module
-----------------------------------
Features
  1. Record attendance        (pick a date, mark each student, save)
  2. Present / Absent tracking (one status per student per day, editable)
  3. Attendance history        (filter by student, date range, status)
  4. Attendance percentage     (present / days recorded, flags low attendance)
  5. Attendance reports        (summary, per-student, daily; export to CSV)

Run standalone:   python attendance_module.py
Embed in your app:
    from attendance_module import AttendanceFrame
    AttendanceFrame(parent_widget).pack(fill="both", expand=True)

Uses only the Python standard library (tkinter + sqlite3).
"""

import csv
import sqlite3
import datetime as dt
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

DB_PATH = "siwes.db"
MIN_PERCENT = 75.0          # attendance below this is flagged
DATE_FMT = "%Y-%m-%d"
PRESENT, ABSENT = "Present", "Absent"


# --------------------------------------------------------------------------
# Data / business logic (no GUI code here, so it is easy to test or reuse)
# --------------------------------------------------------------------------
class AttendanceManager:
    def __init__(self, db_path=DB_PATH):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._create_tables()

    def _create_tables(self):
        # `students` is created only if your Student Management module has
        # not already made it. If yours differs, adapt list_students/add_student.
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS students (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                matric_no TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS attendance (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
                att_date   TEXT NOT NULL,
                status     TEXT NOT NULL CHECK (status IN ('Present','Absent')),
                UNIQUE (student_id, att_date)
            );
        """)
        self.conn.commit()

    # ---- students --------------------------------------------------------
    def add_student(self, matric_no, full_name):
        self.conn.execute(
            "INSERT INTO students (matric_no, full_name) VALUES (?, ?)",
            (matric_no.strip(), full_name.strip()))
        self.conn.commit()

    def list_students(self):
        return self.conn.execute(
            "SELECT id, matric_no, full_name FROM students ORDER BY full_name"
        ).fetchall()

    # ---- recording -------------------------------------------------------
    def get_day(self, att_date):
        """Return {student_id: status} already saved for a date."""
        rows = self.conn.execute(
            "SELECT student_id, status FROM attendance WHERE att_date = ?",
            (att_date,)).fetchall()
        return {r["student_id"]: r["status"] for r in rows}

    def record_day(self, att_date, statuses):
        """Save {student_id: status} for a date (inserts or updates)."""
        self.conn.executemany(
            """INSERT INTO attendance (student_id, att_date, status)
               VALUES (?, ?, ?)
               ON CONFLICT(student_id, att_date)
               DO UPDATE SET status = excluded.status""",
            [(sid, att_date, st) for sid, st in statuses.items()])
        self.conn.commit()

    def set_status(self, record_id, status):
        self.conn.execute("UPDATE attendance SET status=? WHERE id=?",
                          (status, record_id))
        self.conn.commit()

    def delete_record(self, record_id):
        self.conn.execute("DELETE FROM attendance WHERE id=?", (record_id,))
        self.conn.commit()

    # ---- history ---------------------------------------------------------
    def history(self, student_id=None, start=None, end=None, status=None):
        sql = """SELECT a.id, a.att_date, s.matric_no, s.full_name, a.status
                 FROM attendance a JOIN students s ON s.id = a.student_id
                 WHERE 1=1"""
        params = []
        if student_id:
            sql += " AND a.student_id = ?"; params.append(student_id)
        if start:
            sql += " AND a.att_date >= ?"; params.append(start)
        if end:
            sql += " AND a.att_date <= ?"; params.append(end)
        if status:
            sql += " AND a.status = ?"; params.append(status)
        sql += " ORDER BY a.att_date DESC, s.full_name"
        return self.conn.execute(sql, params).fetchall()

    # ---- percentage ------------------------------------------------------
    def percentages(self, start=None, end=None, student_id=None):
        """Per-student totals and percentage (present / days recorded)."""
        join_filter, params = "", []
        if start:
            join_filter += " AND a.att_date >= ?"; params.append(start)
        if end:
            join_filter += " AND a.att_date <= ?"; params.append(end)
        where = ""
        if student_id:
            where = " WHERE s.id = ?"; params.append(student_id)
        rows = self.conn.execute(f"""
            SELECT s.id, s.matric_no, s.full_name,
                   COUNT(a.id) AS total,
                   SUM(CASE WHEN a.status='Present' THEN 1 ELSE 0 END) AS present,
                   SUM(CASE WHEN a.status='Absent'  THEN 1 ELSE 0 END) AS absent
            FROM students s
            LEFT JOIN attendance a ON a.student_id = s.id {join_filter}
            {where}
            GROUP BY s.id ORDER BY s.full_name""", params).fetchall()
        out = []
        for r in rows:
            pct = (r["present"] / r["total"] * 100) if r["total"] else 0.0
            out.append({**dict(r), "percent": round(pct, 1)})
        return out

    # ---- reports ---------------------------------------------------------
    def daily_report(self, att_date):
        rows = self.history(start=att_date, end=att_date)
        return [(r["matric_no"], r["full_name"], r["status"]) for r in rows]


# --------------------------------------------------------------------------
# GUI
# --------------------------------------------------------------------------
def valid_date(text):
    try:
        dt.datetime.strptime(text.strip(), DATE_FMT)
        return True
    except ValueError:
        return False


class AttendanceFrame(ttk.Frame):
    def __init__(self, master, db_path=DB_PATH):
        super().__init__(master)
        self.mgr = AttendanceManager(db_path)
        self.students = []            # cached list of student rows
        self.pending = {}             # {student_id: status} on Record tab
        self.report_data = ([], [])   # (headers, rows) for CSV export

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=8, pady=8)
        self.tab_record = ttk.Frame(nb)
        self.tab_history = ttk.Frame(nb)
        self.tab_percent = ttk.Frame(nb)
        self.tab_report = ttk.Frame(nb)
        nb.add(self.tab_record, text="Record Attendance")
        nb.add(self.tab_history, text="Attendance History")
        nb.add(self.tab_percent, text="Attendance Percentage")
        nb.add(self.tab_report, text="Reports")
        nb.bind("<<NotebookTabChanged>>", lambda e: self.refresh_all())

        self._build_record_tab()
        self._build_history_tab()
        self._build_percent_tab()
        self._build_report_tab()
        self.refresh_all()

    # ---- helpers ---------------------------------------------------------
    def _today(self):
        return dt.date.today().strftime(DATE_FMT)

    def _student_choices(self):
        return ["All students"] + [f"{s['matric_no']} - {s['full_name']}"
                                   for s in self.students]

    def _student_id_from_choice(self, combo):
        idx = combo.current()
        return None if idx <= 0 else self.students[idx - 1]["id"]

    def _make_tree(self, parent, columns, widths):
        frame = ttk.Frame(parent)
        tree = ttk.Treeview(frame, columns=[c[0] for c in columns],
                            show="headings", selectmode="extended")
        for (key, title), w in zip(columns, widths):
            tree.heading(key, text=title)
            tree.column(key, width=w, anchor="w")
        sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        return frame, tree

    def refresh_all(self):
        self.students = self.mgr.list_students()
        choices = self._student_choices()
        self.hist_student["values"] = choices
        self.rep_student["values"] = choices
        if self.hist_student.current() < 0:
            self.hist_student.current(0)
        if self.rep_student.current() < 0:
            self.rep_student.current(0)

    # ---- Tab 1: record attendance ---------------------------------------
    def _build_record_tab(self):
        t = self.tab_record
        top = ttk.Frame(t); top.pack(fill="x", pady=6, padx=6)
        ttk.Label(top, text="Date (YYYY-MM-DD):").pack(side="left")
        self.rec_date = tk.StringVar(value=self._today())
        ttk.Entry(top, textvariable=self.rec_date, width=12).pack(side="left", padx=4)
        ttk.Button(top, text="Today",
                   command=lambda: self.rec_date.set(self._today())).pack(side="left")
        ttk.Button(top, text="Load day", command=self.load_day).pack(side="left", padx=6)
        ttk.Button(top, text="+ Add student", command=self.add_student_dialog)\
            .pack(side="right")

        frame, self.rec_tree = self._make_tree(
            t, [("matric", "Matric No"), ("name", "Student Name"), ("status", "Status")],
            [150, 300, 100])
        frame.pack(fill="both", expand=True, padx=6)
        self.rec_tree.tag_configure("Present", foreground="#1b7f3b")
        self.rec_tree.tag_configure("Absent", foreground="#c0392b")
        self.rec_tree.bind("<Double-1>", self._toggle_selected)

        btns = ttk.Frame(t); btns.pack(fill="x", pady=6, padx=6)
        ttk.Button(btns, text="Mark Present",
                   command=lambda: self._mark_selected(PRESENT)).pack(side="left")
        ttk.Button(btns, text="Mark Absent",
                   command=lambda: self._mark_selected(ABSENT)).pack(side="left", padx=4)
        ttk.Button(btns, text="All Present",
                   command=lambda: self._mark_all(PRESENT)).pack(side="left", padx=(16, 4))
        ttk.Button(btns, text="All Absent",
                   command=lambda: self._mark_all(ABSENT)).pack(side="left")
        ttk.Button(btns, text="Save Attendance", command=self.save_day)\
            .pack(side="right")
        self.rec_info = ttk.Label(t, text="Double-click a row to toggle Present/Absent.")
        self.rec_info.pack(anchor="w", padx=8, pady=(0, 6))

    def load_day(self):
        date = self.rec_date.get().strip()
        if not valid_date(date):
            messagebox.showerror("Invalid date", "Use the format YYYY-MM-DD.")
            return
        self.students = self.mgr.list_students()
        saved = self.mgr.get_day(date)
        # unrecorded students default to Present for quick marking
        self.pending = {s["id"]: saved.get(s["id"], PRESENT) for s in self.students}
        self.rec_tree.delete(*self.rec_tree.get_children())
        for s in self.students:
            st = self.pending[s["id"]]
            self.rec_tree.insert("", "end", iid=str(s["id"]),
                                 values=(s["matric_no"], s["full_name"], st), tags=(st,))
        note = "already recorded" if saved else "not yet recorded"
        self.rec_info.config(text=f"{date}: {note}. Double-click a row to toggle.")

    def _set_row(self, sid, status):
        self.pending[sid] = status
        vals = list(self.rec_tree.item(str(sid), "values"))
        vals[2] = status
        self.rec_tree.item(str(sid), values=vals, tags=(status,))

    def _mark_selected(self, status):
        for iid in self.rec_tree.selection():
            self._set_row(int(iid), status)

    def _mark_all(self, status):
        for iid in self.rec_tree.get_children():
            self._set_row(int(iid), status)

    def _toggle_selected(self, _event):
        for iid in self.rec_tree.selection():
            cur = self.pending.get(int(iid), PRESENT)
            self._set_row(int(iid), ABSENT if cur == PRESENT else PRESENT)

    def save_day(self):
        date = self.rec_date.get().strip()
        if not valid_date(date):
            messagebox.showerror("Invalid date", "Use the format YYYY-MM-DD.")
            return
        if not self.pending:
            messagebox.showinfo("Nothing to save", "Click 'Load day' first.")
            return
        self.mgr.record_day(date, self.pending)
        present = sum(1 for v in self.pending.values() if v == PRESENT)
        messagebox.showinfo("Saved", f"Attendance for {date} saved.\n"
                            f"Present: {present}   Absent: {len(self.pending) - present}")

    def add_student_dialog(self):
        win = tk.Toplevel(self); win.title("Add student"); win.grab_set()
        m, n = tk.StringVar(), tk.StringVar()
        ttk.Label(win, text="Matric No:").grid(row=0, column=0, padx=8, pady=6, sticky="e")
        ttk.Entry(win, textvariable=m, width=28).grid(row=0, column=1, padx=8)
        ttk.Label(win, text="Full name:").grid(row=1, column=0, padx=8, pady=6, sticky="e")
        ttk.Entry(win, textvariable=n, width=28).grid(row=1, column=1, padx=8)

        def save():
            if not m.get().strip() or not n.get().strip():
                messagebox.showerror("Missing data", "Fill in both fields.", parent=win)
                return
            try:
                self.mgr.add_student(m.get(), n.get())
            except sqlite3.IntegrityError:
                messagebox.showerror("Duplicate", "That matric number already exists.",
                                     parent=win)
                return
            win.destroy(); self.refresh_all(); self.load_day()
        ttk.Button(win, text="Save", command=save).grid(row=2, column=1, pady=10, sticky="e", padx=8)

    # ---- Tab 2: history --------------------------------------------------
    def _build_history_tab(self):
        t = self.tab_history
        top = ttk.Frame(t); top.pack(fill="x", pady=6, padx=6)
        ttk.Label(top, text="Student:").pack(side="left")
        self.hist_student = ttk.Combobox(top, state="readonly", width=32)
        self.hist_student.pack(side="left", padx=4)
        ttk.Label(top, text="From:").pack(side="left", padx=(8, 0))
        self.hist_from = tk.StringVar()
        ttk.Entry(top, textvariable=self.hist_from, width=11).pack(side="left", padx=2)
        ttk.Label(top, text="To:").pack(side="left")
        self.hist_to = tk.StringVar()
        ttk.Entry(top, textvariable=self.hist_to, width=11).pack(side="left", padx=2)
        self.hist_status = ttk.Combobox(top, state="readonly", width=9,
                                        values=["Any", PRESENT, ABSENT])
        self.hist_status.current(0)
        self.hist_status.pack(side="left", padx=6)
        ttk.Button(top, text="Search", command=self.load_history).pack(side="left")

        frame, self.hist_tree = self._make_tree(
            t, [("date", "Date"), ("matric", "Matric No"),
                ("name", "Student Name"), ("status", "Status")],
            [100, 140, 280, 90])
        frame.pack(fill="both", expand=True, padx=6)
        self.hist_tree.tag_configure("Present", foreground="#1b7f3b")
        self.hist_tree.tag_configure("Absent", foreground="#c0392b")

        btns = ttk.Frame(t); btns.pack(fill="x", pady=6, padx=6)
        ttk.Button(btns, text="Toggle status of selected",
                   command=self.hist_toggle).pack(side="left")
        ttk.Button(btns, text="Delete selected",
                   command=self.hist_delete).pack(side="left", padx=6)
        self.hist_count = ttk.Label(btns, text="")
        self.hist_count.pack(side="right")

    def _date_or_none(self, var):
        v = var.get().strip()
        if not v:
            return None
        if not valid_date(v):
            raise ValueError(f"'{v}' is not a valid date (use YYYY-MM-DD).")
        return v

    def load_history(self):
        try:
            start, end = self._date_or_none(self.hist_from), self._date_or_none(self.hist_to)
        except ValueError as e:
            messagebox.showerror("Invalid date", str(e)); return
        status = self.hist_status.get()
        rows = self.mgr.history(self._student_id_from_choice(self.hist_student),
                                start, end, None if status == "Any" else status)
        self.hist_tree.delete(*self.hist_tree.get_children())
        for r in rows:
            self.hist_tree.insert("", "end", iid=str(r["id"]), tags=(r["status"],),
                                  values=(r["att_date"], r["matric_no"],
                                          r["full_name"], r["status"]))
        self.hist_count.config(text=f"{len(rows)} record(s)")

    def hist_toggle(self):
        for iid in self.hist_tree.selection():
            cur = self.hist_tree.item(iid, "values")[3]
            self.mgr.set_status(int(iid), ABSENT if cur == PRESENT else PRESENT)
        self.load_history()

    def hist_delete(self):
        sel = self.hist_tree.selection()
        if sel and messagebox.askyesno("Delete", f"Delete {len(sel)} record(s)?"):
            for iid in sel:
                self.mgr.delete_record(int(iid))
            self.load_history()

    # ---- Tab 3: percentage ----------------------------------------------
    def _build_percent_tab(self):
        t = self.tab_percent
        top = ttk.Frame(t); top.pack(fill="x", pady=6, padx=6)
        ttk.Label(top, text="From:").pack(side="left")
        self.pct_from = tk.StringVar()
        ttk.Entry(top, textvariable=self.pct_from, width=11).pack(side="left", padx=2)
        ttk.Label(top, text="To:").pack(side="left")
        self.pct_to = tk.StringVar()
        ttk.Entry(top, textvariable=self.pct_to, width=11).pack(side="left", padx=2)
        ttk.Button(top, text="Calculate", command=self.load_percent).pack(side="left", padx=6)
        ttk.Label(top, text=f"Red = below {MIN_PERCENT:.0f}%").pack(side="right")

        frame, self.pct_tree = self._make_tree(
            t, [("matric", "Matric No"), ("name", "Student Name"), ("total", "Days"),
                ("present", "Present"), ("absent", "Absent"), ("pct", "Attendance %")],
            [130, 250, 60, 70, 70, 110])
        frame.pack(fill="both", expand=True, padx=6, pady=(0, 6))
        self.pct_tree.tag_configure("low", foreground="#c0392b")
        self.pct_tree.tag_configure("ok", foreground="#1b7f3b")

    def load_percent(self):
        try:
            start, end = self._date_or_none(self.pct_from), self._date_or_none(self.pct_to)
        except ValueError as e:
            messagebox.showerror("Invalid date", str(e)); return
        self.pct_tree.delete(*self.pct_tree.get_children())
        for r in self.mgr.percentages(start, end):
            tag = "ok" if r["percent"] >= MIN_PERCENT else "low"
            self.pct_tree.insert("", "end", tags=(tag,), values=(
                r["matric_no"], r["full_name"], r["total"], r["present"],
                r["absent"], f"{r['percent']:.1f}%"))

    # ---- Tab 4: reports --------------------------------------------------
    def _build_report_tab(self):
        t = self.tab_report
        top = ttk.Frame(t); top.pack(fill="x", pady=6, padx=6)
        ttk.Label(top, text="Report:").pack(side="left")
        self.rep_type = ttk.Combobox(top, state="readonly", width=20,
                                     values=["Summary report", "Student report", "Daily report"])
        self.rep_type.current(0); self.rep_type.pack(side="left", padx=4)
        self.rep_student = ttk.Combobox(top, state="readonly", width=30)
        self.rep_student.pack(side="left", padx=4)
        ttk.Label(top, text="From / Date:").pack(side="left", padx=(8, 0))
        self.rep_from = tk.StringVar()
        ttk.Entry(top, textvariable=self.rep_from, width=11).pack(side="left", padx=2)
        ttk.Label(top, text="To:").pack(side="left")
        self.rep_to = tk.StringVar()
        ttk.Entry(top, textvariable=self.rep_to, width=11).pack(side="left", padx=2)

        btns = ttk.Frame(t); btns.pack(fill="x", padx=6)
        ttk.Button(btns, text="Generate", command=self.generate_report).pack(side="left")
        ttk.Button(btns, text="Export to CSV", command=self.export_csv).pack(side="left", padx=6)
        ttk.Label(btns, text="Daily report uses the 'From / Date' box. "
                             "Student report needs a student selected.").pack(side="right")

        self.rep_text = tk.Text(t, wrap="none", font=("Courier New", 10), height=20)
        self.rep_text.pack(fill="both", expand=True, padx=6, pady=6)

    def generate_report(self):
        try:
            start, end = self._date_or_none(self.rep_from), self._date_or_none(self.rep_to)
        except ValueError as e:
            messagebox.showerror("Invalid date", str(e)); return
        kind = self.rep_type.get()
        today = self._today()

        if kind == "Summary report":
            title = "SIWES ATTENDANCE SUMMARY"
            headers = ["Matric No", "Name", "Days", "Present", "Absent", "Percent", "Remark"]
            rows = [(r["matric_no"], r["full_name"], r["total"], r["present"], r["absent"],
                     f"{r['percent']:.1f}%",
                     "OK" if r["percent"] >= MIN_PERCENT else "LOW")
                    for r in self.mgr.percentages(start, end)]
        elif kind == "Student report":
            sid = self._student_id_from_choice(self.rep_student)
            if not sid:
                messagebox.showwarning("Select student", "Choose a student first."); return
            who = self.rep_student.get()
            title = f"ATTENDANCE REPORT: {who}"
            headers = ["Date", "Status"]
            rows = [(r["att_date"], r["status"])
                    for r in self.mgr.history(sid, start, end)]
            p = self.mgr.percentages(start, end, sid)[0]
            rows.append(("", ""))
            rows.append(("Attendance", f"{p['present']}/{p['total']} = {p['percent']:.1f}%"))
        else:  # Daily report
            if not start:
                messagebox.showwarning("Date needed", "Enter a date in 'From / Date'."); return
            title = f"DAILY ATTENDANCE: {start}"
            headers = ["Matric No", "Name", "Status"]
            rows = self.mgr.daily_report(start)

        self.report_data = (headers, rows)
        self._show_report(title, headers, rows, today)

    def _show_report(self, title, headers, rows, today):
        widths = [max(len(str(x)) for x in [h] + [r[i] for r in rows])
                  for i, h in enumerate(headers)]
        line = lambda cells: "  ".join(str(c).ljust(w) for c, w in zip(cells, widths))
        out = [title, f"Generated: {today}", "", line(headers),
               "  ".join("-" * w for w in widths)]
        out += [line(r) for r in rows]
        if not rows:
            out.append("(no records found)")
        self.rep_text.delete("1.0", "end")
        self.rep_text.insert("1.0", "\n".join(out))

    def export_csv(self):
        headers, rows = self.report_data
        if not rows:
            messagebox.showinfo("Nothing to export", "Generate a report first."); return
        path = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(headers); w.writerows(rows)
        messagebox.showinfo("Exported", f"Report saved to:\n{path}")


# --------------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("SIWES - Attendance Management")
    root.geometry("900x560")
    AttendanceFrame(root).pack(fill="both", expand=True)
    root.mainloop()
