from datetime import datetime

class LogbookEntry:

    def __init__(
        self,
        student_id,
        date,
        week_number,
        activities,
        skills_learned="",
        challenges="",
        entry_id=None,
        supervisor_comment=None,
        status="Pending"
    ):
        self.entry_id = entry_id
        self.student_id = student_id
        self.date = date
        self.week_number = week_number
        self.activities = activities
        self.skills_learned = skills_learned
        self.challenges = challenges
        self.supervisor_comment = supervisor_comment
        self.status = status

        self.validate()


    def validate(self):

        if not self.student_id:
            raise ValueError("Student ID is required.")

        if not self.date:
            raise ValueError("Date is required.")
        try:
               datetime.strptime(self.date, "%d/%m/%Y")

        except ValueError:
            raise ValueError("Date must be in DD/MM/YYYY format.")

        if not isinstance(self.week_number, int):
            raise ValueError("Week number must be a number.")

        if self.week_number <= 0:
            raise ValueError("Week number must be greater than zero.")

        if not self.activities.strip():
            raise ValueError("Activities cannot be empty.")
        valid_statuses = ["Pending", "Approved", "Rejected"]

        if self.status not in valid_statuses:
            raise ValueError("Invalid status.")