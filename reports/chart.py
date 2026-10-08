"""
Charts module for the SIWES Management System.

Module: Reports & Analytics
Developer: Samuel Okpo
"""

from pathlib import Path

import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHARTS_DIRECTORY = PROJECT_ROOT / "reports" / "generated_charts"

CHARTS_DIRECTORY.mkdir(parents=True, exist_ok=True)


def create_placement_status_chart(status_data):
    """
    Create a bar chart showing SIWES placement status.

    Example input:
    {
        "Pending": 5,
        "Approved": 10,
        "Active": 20,
        "Completed": 8
    }
    """

    if not status_data:
        return None

    labels = list(status_data.keys())
    values = list(status_data.values())

    plt.figure(figsize=(8, 5))

    plt.bar(labels, values)

    plt.title("SIWES Placement Status")
    plt.xlabel("Placement Status")
    plt.ylabel("Number of Students")

    plt.tight_layout()

    output_path = (
        CHARTS_DIRECTORY / "placement_status.png"
    )

    plt.savefig(output_path, dpi=150)
    plt.close()

    return output_path


def create_attendance_chart(present, absent):
    """Create a pie chart showing attendance."""

    if present == 0 and absent == 0:
        return None

    labels = ["Present", "Absent"]
    values = [present, absent]

    plt.figure(figsize=(7, 7))

    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("SIWES Attendance")

    output_path = (
        CHARTS_DIRECTORY / "attendance.png"
    )

    plt.savefig(output_path, dpi=150)
    plt.close()

    return output_path


def create_logbook_chart(total, approved, pending):
    """Create a bar chart for logbook progress."""

    values = [total, approved, pending]
    labels = ["Total Entries", "Approved", "Pending"]

    if total == 0:
        return None

    plt.figure(figsize=(8, 5))

    plt.bar(labels, values)

    plt.title("Digital Logbook Statistics")
    plt.xlabel("Category")
    plt.ylabel("Number of Entries")

    plt.tight_layout()

    output_path = (
        CHARTS_DIRECTORY / "logbook_statistics.png"
    )

    plt.savefig(output_path, dpi=150)
    plt.close()

    return output_path


if __name__ == "__main__":

    test_status = {
        "Pending": 5,
        "Approved": 10,
        "Active": 20,
        "Completed": 8
    }

    path = create_placement_status_chart(test_status)

    print("Chart generated:", path)