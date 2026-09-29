from logbook import LogbookEntry


try:

    entry = LogbookEntry(
        student_id=1023,
        date="31/02/2026",
        week_number=4,
        activities="Practiced Python"
    )

    print("Entry is valid.")

except ValueError as error:

    print("Validation error:", error)