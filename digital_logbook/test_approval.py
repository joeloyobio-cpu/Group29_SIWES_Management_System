from database import get_entries, update_entry_status


update_entry_status(
    entry_id=999,
    status="Approved"
)


entries = get_entries(1023)

for entry in entries:

    print("Entry ID:", entry.entry_id)
    print("Status:", entry.status)
    print("Supervisor Comment:", entry.supervisor_comment)

    print("----------------------")