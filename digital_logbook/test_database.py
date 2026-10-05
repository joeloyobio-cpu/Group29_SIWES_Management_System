from database import get_entries, delete_entry


entries = get_entries(1023)

print("ENTRIES BEFORE DELETE:")

for entry in entries:
    print(entry.entry_id, "-", entry.activities)


entry_to_delete = entries[-1]

delete_entry(entry_to_delete)


print("\nENTRIES AFTER DELETE:")

entries = get_entries(1023)

for entry in entries:
    print(entry.entry_id, "-", entry.activities)