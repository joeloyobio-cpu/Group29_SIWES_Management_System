import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from logbook import LogbookEntry
from database import (
    save_entry,
    get_entries,
    update_entry,
    delete_entry,
    filter_entries,
    update_entry_status,
    entry_exists
)

window = tk.Tk()

window.title("SIWES Management System - Digital Logbook")
window.geometry("1200x800")
window.configure(bg="#f5f7fa")
# Main scrollable area
main_canvas = tk.Canvas(
    window,
    bg="#f5f7fa",
    highlightthickness=0
)

main_scrollbar = ttk.Scrollbar(
    window,
    orient="vertical",
    command=main_canvas.yview
)

main_scrollable_frame = tk.Frame(
    main_canvas,
    bg="#f5f7fa"
)

main_scrollable_frame.bind(
    "<Configure>",
    lambda event: main_canvas.configure(
        scrollregion=main_canvas.bbox("all")
    )
)

main_canvas.create_window(
    (0, 0),
    window=main_scrollable_frame,
    anchor="nw"
)

main_canvas.configure(
    yscrollcommand=main_scrollbar.set
)

main_canvas.pack(
    side="left",
    fill="both",
    expand=True
)

main_scrollbar.pack(
    side="right",
    fill="y"
)

def set_today():
    today = datetime.now().strftime("%d/%m/%Y")

    date_entry.delete(0, tk.END)
    date_entry.insert(0, today)

# Form
form_frame = tk.Frame(
    main_scrollable_frame,
    bg="#f5f7fa"
)

form_frame.pack(
    fill="x",
    padx=30,
    pady=10
)

form_card = tk.Frame(
    form_frame,
    bg="white",
    bd=1,
    relief="solid"
)
form_card.pack(
    fill="x",
)

form_title = tk.Label(
    form_card,
    text="New Logbook Entry",
    font=("Arial", 18, "bold"),
    bg="white",
    fg="#1f2937"
)
form_title.pack(
    anchor="w",
    padx=20,
    pady=(10, 3)
)

form_subtitle = tk.Label(
    form_card,
    text="Record your daily SIWES activities and learning progress.",
    font=("Arial", 10),
    bg="white",
    fg="#6b7280"
)
form_subtitle.pack(
    anchor="w",
    padx=20,
    pady=(0, 8)
)

fields_frame = tk.Frame(
    form_card,
    bg="white"
)
fields_frame.pack(
    fill="x",
    padx=20,
    pady=5
)

# Date
date_frame = tk.Frame(
    fields_frame,
    bg="white"
)
date_frame.grid(
    row=0,
    column=0,
    padx=10,
    pady=5,
    sticky="w"
)

date_label = tk.Label(
    date_frame,
    text="Date:",
    bg="white",
    fg="#374151"
)
date_label.pack(anchor="w")

date_entry = tk.Entry(
    date_frame,
    width=25,
    font=("Arial", 10),
    bd=1,
    relief="solid"
)

date_entry.pack(
    side="left"
)

today_button = tk.Button(
    date_frame,
    text="Today",
    command=set_today,
    bg="#6b7280",
    fg="white",
    font=("Arial", 9, "bold"),
    padx=10,
    pady=3,
    relief="flat",
    cursor="hand2"
)

today_button.pack(
    side="left",
    padx=8
)

tk.Label(
    date_frame,
    text="Format: DD/MM/YYYY",
    font=("Arial", 8),
    bg="white",
    fg="#6b7280"
).pack(
    side="left",
    padx=5
)




# Week Number
week_frame = tk.Frame(
    fields_frame,
    bg="white"
)
week_frame.grid(
    row=0,
    column=1,
    padx=10,
    pady=5,
    sticky="w"
)

week_label = tk.Label(
    week_frame,
    text="Week Number:",
    bg="white",
    fg="#374151"
)
week_label.pack(anchor="w")

week_entry = tk.Entry(
    week_frame,
    width=25,
    font=("Arial", 10),
    bd=1,
    relief="solid"
)

week_entry.pack()

fields_frame.columnconfigure(0, weight=1)
fields_frame.columnconfigure(1, weight=1)


# Activities
activities_frame = tk.Frame(
    fields_frame,
    bg="white"
)

activities_frame.grid(
    row=1,
    column=0,
    columnspan=2,
    padx=10,
    pady=3,
    sticky="ew"
)

activities_label = tk.Label(
    activities_frame,
    text="Activities:",
    bg="white",
    fg="#374151"
)

activities_label.pack(anchor="w")

activities_text = tk.Text(
    activities_frame,
    height=3,
    width=80,
    font=("Arial", 10),
    bd=1,
    relief="solid"
)

activities_text.pack(fill="x")

activities_count = tk.Label(
    activities_frame,
    text="0 characters",
    font=("Arial", 8),
    bg="white",
    fg="#6b7280"
)

activities_count.pack(
    anchor="e",
    pady=(2, 0)
)

def update_activities_count(event=None):

    text = activities_text.get(
        "1.0",
        tk.END
    ).strip()

    activities_count.config(
        text=f"{len(text)} characters"
    )


activities_text.bind(
    "<KeyRelease>",
    update_activities_count
)

# Skills Learned
skills_frame = tk.Frame(
    fields_frame,
    bg="white"
)

skills_frame.grid(
    row=2,
    column=0,
    columnspan=2,
    padx=10,
    pady=3,
    sticky="ew"
)

skills_label = tk.Label(
    skills_frame,
    text="Skills Learned:",
    bg="white",
    fg="#374151"
)

skills_label.pack(anchor="w")

skills_entry = tk.Entry(
    skills_frame,
    width=80,
    font=("Arial", 10),
    bd=1,
    relief="solid"
)

skills_entry.pack(fill="x")


# Challenges
challenges_frame = tk.Frame(
    fields_frame,
    bg="white"
)

challenges_frame.grid(
    row=3,
    column=0,
    columnspan=2,
    padx=10,
    pady=3,
    sticky="ew"
)

challenges_label = tk.Label(
    challenges_frame,
    text="Challenges:",
    bg="white",
    fg="#374151"
)

challenges_label.pack(anchor="w")

challenges_text = tk.Text(
    challenges_frame,
    height=3,
    width=80,
    font=("Arial", 10),
    bd=1,
    relief="solid"
)

challenges_text.pack(fill="x")

# Logbook entries table

table_frame = tk.Frame(
    main_scrollable_frame,
    bg="#f5f7fa"
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


columns = ("id", "date", "week", "activities", "status", "actions")

# Search section

search_frame = tk.Frame(
    table_frame,
    bg="#f5f7fa"
)
search_frame.pack(fill="x", pady=5)

search_label = tk.Label(
    search_frame,
    text="Search:",
    font=("Arial", 10, "bold"),
    bg="#f5f7fa",
    fg="#374151"
)

search_label.pack(side="left", padx=5)

search_entry = tk.Entry(
    search_frame,
    width=35,
    font=("Arial", 10),
    bd=1,
    relief="solid"
)

search_entry.pack(side="left", padx=5)

week_filter_label = tk.Label(
    search_frame,
    text="Week:",
    font=("Arial", 10, "bold"),
    bg="#f5f7fa",
    fg="#374151"
)

week_filter_label.pack(
    side="left",
    padx=5
)

week_filter = ttk.Combobox(
    search_frame,
    values=["All", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
    state="readonly",
    width=8,
    font=("Arial", 10)
)

week_filter.set("All")

week_filter.pack(
    side="left",
    padx=5
)

status_filter_label = tk.Label(
    search_frame,
    text="Status:",
    font=("Arial", 10, "bold"),
    bg="#f5f7fa",
    fg="#374151"
)

status_filter_label.pack(
    side="left",
    padx=5
)

status_filter = ttk.Combobox(
    search_frame,
    values=["All", "Pending", "Approved", "Rejected"],
    state="readonly",
    width=10,
    font=("Arial", 10)
)

status_filter.set("All")

status_filter.pack(
    side="left",
    padx=5
)

# Entries table

style = ttk.Style()

style.configure(
    "Treeview",
    background="white",
    foreground="#374151",
    rowheight=32,
    font=("Arial", 10),
    borderwidth=0
)

style.configure(
    "Treeview.Heading",
    background="#e5e7eb",
    foreground="#1f2937",
    font=("Arial", 10, "bold"),
    relief="flat"
)

style.map(
    "Treeview",
    background=[
        ("selected", "#dbeafe")
    ],
    foreground=[
        ("selected", "#1e3a8a")
    ]
)

style.configure(
    "Treeview",
    fieldbackground="white"
)

entry_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

entry_table.heading("id", text="ID")
entry_table.heading("date", text="Date")
entry_table.heading("week", text="Week")
entry_table.heading("activities", text="Activities")
entry_table.heading("status", text="Status")
entry_table.heading("actions", text="Actions")

entry_table.tag_configure(
    "pending",
    foreground="#d97706"
)

entry_table.tag_configure(
    "approved",
    foreground="#16a34a"
)

entry_table.tag_configure(
    "rejected",
    foreground="#dc2626"
)

# Scrollbar
table_scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=entry_table.yview
)

entry_table.configure(
    yscrollcommand=table_scrollbar.set
)

entry_table.pack(
    side="left",
    fill="both",
    expand=True
)

table_scrollbar.pack(
    side="right",
    fill="y"
)

editing_entry = None

def view_entry(entry):

    view_window = tk.Toplevel(window)

    view_window.title("View Logbook Entry")
    view_window.geometry("650x650")
    view_window.configure(bg="#f5f7fa")

    # Main card
    view_canvas = tk.Canvas(
    view_window,
    bg="#f5f7fa",
    highlightthickness=0
)
    
    view_scrollbar = ttk.Scrollbar(
        view_window,
        orient="vertical",
        command=view_canvas.yview
        )
    
    view_card = tk.Frame(
        view_canvas,
        bg="white",
        bd=1,
        relief="solid"
        )
    
    view_card.bind(
        "<Configure>",
        lambda event: view_canvas.configure(
            scrollregion=view_canvas.bbox("all")
        )
    )
    
    view_canvas.create_window(
        (0, 0),
        window=view_card,
        anchor="nw"
        )
    
    view_canvas.configure(
        yscrollcommand=view_scrollbar.set
        )
    
    view_canvas.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(20, 0),
        pady=20
        )
    
    view_scrollbar.pack(
        side="right",
        fill="y",
        pady=20
        )

    # Title
    tk.Label(
        view_card,
        text="Logbook Entry",
        font=("Arial", 18, "bold"),
        bg="white",
        fg="#1f2937"
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 5)
    )

    # Basic information
    info_frame = tk.Frame(
        view_card,
        bg="white"
    )

    info_frame.pack(
        fill="x",
        padx=20,
        pady=10
    )

    tk.Label(
        info_frame,
        text=f"Date: {entry.date}",
        font=("Arial", 10),
        bg="white",
        fg="#374151"
    ).pack(anchor="w", pady=2)

    tk.Label(
        info_frame,
        text=f"Week Number: {entry.week_number}",
        font=("Arial", 10),
        bg="white",
        fg="#374151"
    ).pack(anchor="w", pady=2)

    tk.Label(
        info_frame,
        text=f"Status: {entry.status}",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#374151"
    ).pack(anchor="w", pady=2)

    # Activities
    tk.Label(
        view_card,
        text="Activities",
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#1f2937"
    ).pack(
        anchor="w",
        padx=20,
        pady=(10, 3)
    )

    activities = tk.Text(
        view_card,
        height=5,
        width=60,
        font=("Arial", 10),
        bd=1,
        relief="solid"
    )

    activities.insert(
        tk.END,
        entry.activities
    )

    activities.config(state="disabled")

    activities.pack(
        fill="x",
        padx=20
    )

    # Skills Learned
    tk.Label(
        view_card,
        text="Skills Learned",
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#1f2937"
    ).pack(
        anchor="w",
        padx=20,
        pady=(10, 3)
    )

    skills = tk.Text(
    view_card,
    height=3,
    font=("Arial", 10),
    bd=1,
    relief="solid",
    wrap="word"
    )
    
    skills.insert(
    tk.END,
    entry.skills_learned or "None"
    )
    
    skills.config(state="disabled")
    
    skills.pack(
    fill="x",
    padx=20
    
    )

    # Challenges
    tk.Label(
        view_card,
        text="Challenges",
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#1f2937"
    ).pack(
        anchor="w",
        padx=20,
        pady=(10, 3)
    )

    challenges = tk.Text(
    view_card,
    height=4,
    font=("Arial", 10),
    bd=1,
    relief="solid",
    wrap="word"
    )
    
    challenges.insert(
    tk.END,
    entry.challenges or "None"
    )
    
    challenges.config(state="disabled")
    
    challenges.pack(
    fill="x",
    padx=20
    )

    # Supervisor Comment
    tk.Label(
        view_card,
        text="Supervisor Comment",
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#1f2937"
    ).pack(
        anchor="w",
        padx=20,
        pady=(10, 3)
    )

    comment = tk.Text(
    view_card,
    height=4,
    font=("Arial", 10),
    bd=1,
    relief="solid",
    wrap="word"
    )
    
    comment.insert(
    tk.END,
    entry.supervisor_comment or "None"
    )
    
    comment.config(state="disabled")
    
    comment.pack(
    fill="x",
    padx=20
    )

def open_selected_entry():

    entry = get_selected_entry()

    if entry is not None:

        view_entry(entry)

def update_selected_status():

    entry = get_selected_entry()

    if entry is None:
        return

    if entry.status == "Approved":
        messagebox.showwarning(
            "Status Locked",
            "Approved entries cannot have their status changed."
        )
        return

    status_window = tk.Toplevel(window)

    status_window.title("Update Logbook Status")
    status_window.geometry("500x500")
    status_window.configure(bg="#f5f7fa")

    status_card = tk.Frame(
        status_window,
        bg="white",
        bd=1,
        relief="solid"
    )

    status_card.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    tk.Label(
        status_card,
        text="Update Logbook Status",
        font=("Arial", 16, "bold"),
        bg="white",
        fg="#1f2937"
    ).pack(
        anchor="w",
        padx=20,
        pady=(20, 10)
    )

    tk.Label(
        status_card,
        text=f"Entry ID: {entry.entry_id}",
        font=("Arial", 10),
        bg="white",
        fg="#374151"
    ).pack(
        anchor="w",
        padx=20,
        pady=5
    )

    tk.Label(
        status_card,
        text="Status:",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#374151"
    ).pack(
        anchor="w",
        padx=20,
        pady=(10, 3)
    )

    status_choice = ttk.Combobox(
        status_card,
        values=["Pending", "Approved", "Rejected"],
        state="readonly",
        width=25,
        font=("Arial", 10)
    )

    status_choice.set(entry.status)

    status_choice.pack(
        anchor="w",
        padx=20
    )

    tk.Label(
        status_card,
        text="Supervisor Comment:",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#374151"
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 3)
    )

    comment_text = tk.Text(
        status_card,
        height=6,
        width=50,
        font=("Arial", 10),
        bd=1,
        relief="solid"
    )

    if entry.supervisor_comment:
        comment_text.insert(
            "1.0",
            entry.supervisor_comment
        )

    comment_text.pack(
        padx=20,
        fill="x"
    )

    def save_status():

        try:

            new_status = status_choice.get()

            comment = comment_text.get(
                "1.0",
                tk.END
            ).strip()

            update_entry_status(
                entry.entry_id,
                new_status,
                comment
            )

            load_entries()

            messagebox.showinfo(
                "Success",
                "Logbook status updated successfully!"
            )

            status_window.destroy()

        except ValueError as error:

            messagebox.showerror(
                "Invalid Status",
                str(error)
            )


    update_status_button = tk.Button(
        status_card,
        text="Update Status",
        command=save_status,
        bg="#7c3aed",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=25,
        pady=8,
        relief="flat",
        cursor="hand2"
    )

    update_status_button.pack(
        side="bottom",
        pady=20
    )

def get_selected_entry():

    selected_item = entry_table.selection()

    if not selected_item:
        messagebox.showwarning(
            "No Entry Selected",
            "Please select a logbook entry first."
        )
        return None

    item = entry_table.item(selected_item[0])

    entry_id = int(selected_item[0])

    entries = get_entries(1023)

    for entry in entries:

        if entry.entry_id == entry_id:
            
            return entry

    return None

def start_edit_entry(entry):

    global editing_entry

    editing_entry = entry

    form_title.config(text="Edit Logbook Entry")

    form_subtitle.config(
        text="Update your SIWES activities and learning progress."
    )

    date_entry.delete(0, tk.END)
    date_entry.insert(0, entry.date)

    week_entry.delete(0, tk.END)
    week_entry.insert(0, entry.week_number)

    activities_text.delete("1.0", tk.END)
    activities_text.insert("1.0", entry.activities)

    skills_entry.delete(0, tk.END)
    skills_entry.insert(0, entry.skills_learned)

    challenges_text.delete("1.0", tk.END)
    challenges_text.insert("1.0", entry.challenges)

    save_button.config(text="Save Changes")

def search_logbook():

    keyword = search_entry.get().strip()

    selected_week = week_filter.get()
    selected_status = status_filter.get()

    if selected_week == "All":
        week_number = None
    else:
        week_number = int(selected_week)

    if selected_status == "All":
        status = None
    else:
        status = selected_status

    entries = filter_entries(
        student_id=1023,
        week_number=week_number,
        status=status,
        keyword=keyword
    )

    # Clear table
    for item in entry_table.get_children():
        entry_table.delete(item)

    # Display filtered results
    for entry in entries:
        entry_table.insert(
            "",
            tk.END,
            iid=str(entry.entry_id),
            values=(
                entry.entry_id,
                entry.date,
                entry.week_number,
                entry.activities,
                entry.status,
                " "
            ),
                tags=(entry.status.lower(),)
        )

def clear_filters():

    search_entry.delete(0, tk.END)

    week_filter.set("All")

    status_filter.set("All")

    load_entries()

search_button = tk.Button(
    search_frame,
    text="Search",
    command=search_logbook,
    bg="#2563eb",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=15,
    pady=5,
    relief="flat",
    cursor="hand2"
)

search_button.pack(side="left", padx=5)

clear_button = tk.Button(
    search_frame,
    text="Clear",
    command=clear_filters,
    bg="#6b7280",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=15,
    pady=5,
    relief="flat",
    cursor="hand2"
)

clear_button.pack(
    side="left",
    padx=5
)

def edit_selected_entry():

    entry = get_selected_entry()

    if entry is None:
        return

    if entry.status == "Approved":
        messagebox.showwarning(
            "Cannot Edit Entry",
            "Approved entries cannot be edited."
        )
        return

    start_edit_entry(entry)

def delete_selected_entry():

    entry = get_selected_entry()

    if entry is None:
        return

    if entry.status == "Approved":
        messagebox.showwarning(
            "Cannot Delete Entry",
            "Approved entries cannot be deleted."
        )
        return

    confirm = messagebox.askyesno(
        "Delete Entry",
        "Are you sure you want to delete this entry?"
    )

    if confirm:

        delete_entry(entry)

        load_entries()

        messagebox.showinfo(
            "Success",
            "Entry deleted successfully!"
        )


# Action buttons

action_frame = tk.Frame(table_frame)
action_frame.pack(
    before=entry_table,
    pady=5
)

view_button = tk.Button(
    action_frame,
    text="View Selected Entry",
    command=open_selected_entry,
    bg="#4b5563",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=15,
    pady=6,
    relief="flat",
    cursor="hand2"
)

view_button.pack(
    side="left",
    padx=5
)

status_button = tk.Button(
    action_frame,
    text="Update Status",
    command=update_selected_status,
    bg="#7c3aed",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=15,
    pady=6,
    relief="flat",
    cursor="hand2"
)

status_button.pack(
    side="left",
    padx=5
)

edit_button = tk.Button(
    action_frame,
    text="Edit Selected Entry",
    command=edit_selected_entry,
    bg="#2563eb",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=15,
    pady=6,
    relief="flat",
    cursor="hand2"
)

edit_button.pack(side="left", padx=5)


delete_button = tk.Button(
    action_frame,
    text="Delete Selected Entry",
    command=delete_selected_entry,
    bg="#dc2626",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=15,
    pady=6,
    relief="flat",
    cursor="hand2"
)

delete_button.pack(side="left", padx=5)

def load_entries():

    for item in entry_table.get_children():
        entry_table.delete(item)

    entries = get_entries(1023)

    for entry in entries:

        entry_table.insert(
            "",
            tk.END,
            iid=str(entry.entry_id),
            values=(
                entry.entry_id,
                entry.date,
                entry.week_number,
                entry.activities,
                entry.status,
                " "
                ),
                tags=(entry.status.lower(),)
        )

def reset_form():

    global editing_entry

    editing_entry = None

    date_entry.delete(0, tk.END)
    week_entry.delete(0, tk.END)

    activities_text.delete(
        "1.0",
        tk.END
    )

    skills_entry.delete(0, tk.END)

    challenges_text.delete(
        "1.0",
        tk.END
    )

    form_title.config(
        text="New Logbook Entry"
    )

    form_subtitle.config(
        text="Record your daily SIWES activities and learning progress."
    )

    save_button.config(
        text="Save Entry"
    )

def save_logbook_entry():

    global editing_entry

    try:

        date = date_entry.get()
        week_number = int(week_entry.get())
        activities = activities_text.get(
            "1.0",
            tk.END
        ).strip()
        skills_learned = skills_entry.get()
        challenges = challenges_text.get(
            "1.0",
            tk.END
        ).strip()

        # Editing an existing entry
        if editing_entry is not None:

            if entry_exists(
                1023,
                date,
                exclude_id=editing_entry.entry_id
            ):
                raise ValueError(
                    "Another logbook entry already exists for this date."
                )

            editing_entry.date = date
            editing_entry.week_number = week_number
            editing_entry.activities = activities
            editing_entry.skills_learned = skills_learned
            editing_entry.challenges = challenges

            editing_entry.validate()

            update_entry(editing_entry)

            messagebox.showinfo(
                "Success",
                "Entry updated successfully!"
            )

            reset_form()

        # Creating a new entry
        else:

            if entry_exists(1023, date):
                raise ValueError(
                    "A logbook entry already exists for this date."
                )

            entry = LogbookEntry(
                student_id=1023,
                date=date,
                week_number=week_number,
                activities=activities,
                skills_learned=skills_learned,
                challenges=challenges
            )

            save_entry(entry)

            messagebox.showinfo(
                "Success",
                "Logbook entry saved successfully!"
            )

            reset_form()

        load_entries()

    except ValueError as error:

        messagebox.showerror(
            "Invalid Entry",
            str(error)
        )


save_button = tk.Button(
    fields_frame,
    text="Save Entry",
    command=save_logbook_entry,
    bg="#2563eb",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=20,
    pady=8,
    relief="flat",
    cursor="hand2"
)

save_button.grid(
    row=4,
    column=0,
    columnspan=2,
    pady=15
)

new_entry_button = tk.Button(
    fields_frame,
    text="New Entry",
    command=reset_form,
    bg="#6b7280",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=20,
    pady=8,
    relief="flat",
    cursor="hand2"
)

new_entry_button.grid(
    row=4,
    column=1,
    padx=10,
    pady=15
)

load_entries()

window.mainloop()