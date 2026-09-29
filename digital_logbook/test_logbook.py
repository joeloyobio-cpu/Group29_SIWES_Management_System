from logbook import LogbookEntry
from database import save_entry


entry = LogbookEntry(
    student_id=1023,
    date="25/09/2026",
    week_number=4,
    activities="Practiced Python classes and methods.",
    skills_learned="OOP, classes, methods",
    challenges="Understanding object relationships."
)

save_entry(entry)

print("New entry created.")
print("Entry ID:", entry.entry_id)