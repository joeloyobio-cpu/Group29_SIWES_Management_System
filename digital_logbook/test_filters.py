from database import filter_entries


results = filter_entries(
    student_id=1023,
    week_number=4
)


for entry in results:

    print("Entry ID:", entry.entry_id)
    print("Date:", entry.date)
    print("Week:", entry.week_number)
    print("Activities:", entry.activities)
    print("Status:", entry.status)

    print("-----------------------------")