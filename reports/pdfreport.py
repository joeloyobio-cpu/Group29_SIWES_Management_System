"""
PDF report generation for the SIWES Management System.

Module: Reports & Analytics
Developer: Samuel Okpo
"""

from pathlib import Path
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent

REPORTS_DIRECTORY = (
    PROJECT_ROOT / "reports" / "generated_reports"
)

REPORTS_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)


def generate_student_progress_report(
    student,
    placement,
    attendance,
    logbook,
    supervisor_evaluation=None,
    chart_path=None
):
    """
    Generate a student's SIWES progress report as PDF.

    Parameters
    ----------
    student : dict
        Student information.

    placement : dict
        SIWES placement information.

    attendance : dict
        Attendance statistics.

    logbook : dict
        Logbook statistics.

    supervisor_evaluation : dict, optional
        Supervisor evaluation information.

    chart_path : str or Path, optional
        Optional chart to include in the PDF.
    """

    student_name = student.get(
        "name",
        "Unknown Student"
    )

    safe_name = "".join(
        character
        for character in student_name
        if character.isalnum() or character in (" ", "_", "-")
    ).strip().replace(" ", "_")

    if not safe_name:
        safe_name = "student"

    output_path = (
        REPORTS_DIRECTORY
        / f"{safe_name}_SIWES_Report.pdf"
    )

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )

    styles = getSampleStyleSheet()

    story = []

    # Title
    story.append(
        Paragraph(
            "SIWES / INTERNSHIP PROGRESS REPORT",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 15))

    # Student information
    story.append(
        Paragraph(
            "1. Student Information",
            styles["Heading2"]
        )
    )

    student_data = [
        ["Field", "Information"],
        ["Name", student.get("name", "N/A")],
        ["Student ID", student.get("student_id", "N/A")],
        ["Department", student.get("department", "N/A")],
        ["Level", student.get("level", "N/A")],
        ["School", student.get("school", "N/A")],
        ["Email", student.get("email", "N/A")]
    ]

    student_table = Table(
        student_data,
        colWidths=[45 * mm, 110 * mm]
    )

    student_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("PADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(student_table)
    story.append(Spacer(1, 15))

    # Placement
    story.append(
        Paragraph(
            "2. SIWES Placement",
            styles["Heading2"]
        )
    )

    placement_data = [
        ["Field", "Information"],
        [
            "Organization",
            placement.get("organization", "N/A")
        ],
        [
            "Position",
            placement.get("position", "N/A")
        ],
        [
            "Location",
            placement.get("location", "N/A")
        ],
        [
            "Start Date",
            placement.get("start_date", "N/A")
        ],
        [
            "End Date",
            placement.get("end_date", "N/A")
        ],
        [
            "Status",
            placement.get("status", "N/A")
        ]
    ]

    placement_table = Table(
        placement_data,
        colWidths=[45 * mm, 110 * mm]
    )

    placement_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("PADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(placement_table)
    story.append(Spacer(1, 15))

    # Attendance
    story.append(
        Paragraph(
            "3. Attendance Summary",
            styles["Heading2"]
        )
    )

    attendance_data = [
        ["Metric", "Value"],
        [
            "Days Present",
            str(attendance.get("present", 0))
        ],
        [
            "Days Absent",
            str(attendance.get("absent", 0))
        ],
        [
            "Total Records",
            str(attendance.get("total", 0))
        ],
        [
            "Attendance Percentage",
            f"{attendance.get('percentage', 0)}%"
        ]
    ]

    attendance_table = Table(
        attendance_data,
        colWidths=[80 * mm, 75 * mm]
    )

    attendance_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("PADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(attendance_table)
    story.append(Spacer(1, 15))

    # Logbook
    story.append(
        Paragraph(
            "4. Digital Logbook Summary",
            styles["Heading2"]
        )
    )

    logbook_data = [
        ["Metric", "Value"],
        [
            "Total Entries",
            str(logbook.get("total_entries", 0))
        ],
        [
            "Approved Entries",
            str(logbook.get("approved", 0))
        ],
        [
            "Pending Entries",
            str(logbook.get("pending", 0))
        ]
    ]

    logbook_table = Table(
        logbook_data,
        colWidths=[80 * mm, 75 * mm]
    )

    logbook_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("PADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(logbook_table)
    story.append(Spacer(1, 15))

    # Supervisor evaluation
    story.append(
        Paragraph(
            "5. Supervisor Evaluation",
            styles["Heading2"]
        )
    )

    if supervisor_evaluation:
        evaluation_data = [
            ["Category", "Evaluation"],
        ]

        for category, evaluation in supervisor_evaluation.items():
            evaluation_data.append(
                [str(category), str(evaluation)]
            )
    else:
        evaluation_data = [
            ["Evaluation", "Not available"]
        ]

    evaluation_table = Table(
        evaluation_data,
        colWidths=[60 * mm, 95 * mm]
    )

    evaluation_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("PADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(evaluation_table)
    story.append(Spacer(1, 15))

    # Chart
    if chart_path and Path(chart_path).exists():

        story.append(
            Paragraph(
                "6. Progress Chart",
                styles["Heading2"]
            )
        )

        chart = Image(
            str(chart_path),
            width=150 * mm,
            height=90 * mm
        )

        story.append(chart)
        story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "End of Report",
            styles["Italic"]
        )
    )

    document.build(story)

    return output_path


if __name__ == "__main__":

    sample_student = {
        "name": "Samuel Okpo",
        "student_id": "NC-NY-000955",
        "department": "Computer Science",
        "level": "ND",
        "school": "Nasarawa Polytechnic",
        "email": "samuel@example.com"
    }

    sample_placement = {
        "organization": "Example Technology Ltd",
        "position": "IT Intern",
        "location": "Nigeria",
        "start_date": "03 August 2026",
        "end_date": "30 October 2026",
        "status": "Active"
    }

    sample_attendance = {
        "present": 18,
        "absent": 2,
        "total": 20,
        "percentage": 90
    }

    sample_logbook = {
        "total_entries": 18,
        "approved": 15,
        "pending": 3
    }

    sample_evaluation = {
        "Technical Skills": "Good",
        "Communication": "Very Good",
        "Professionalism": "Good"
    }

    output = generate_student_progress_report(
        student=sample_student,
        placement=sample_placement,
        attendance=sample_attendance,
        logbook=sample_logbook,
        supervisor_evaluation=sample_evaluation
    )

    print("PDF generated:")
    print(output)