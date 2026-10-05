from database import search_entries


results = search_entries(1023, "OOP")


for entry in results:

    print("Entry ID:", entry.entry_id)
    print("Date:", entry.date)
    print("Activities:", entry.activities)
    print("Skills:", entry.skills_learned)
    print("-----------------------------")