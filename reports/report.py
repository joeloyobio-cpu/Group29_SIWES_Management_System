"""
Reports & Analytics GUI.

Module: Reports & Analytics
Developer: Samuel Okpo
"""

import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from .analytics import Analytics
from .charts import (
    create_placement_status_chart,
    create_attendance_chart,
    create_logbook_chart
)


class ReportsWindow(ctk.CTkFrame):
    """Reports and Analytics dashboard."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.analytics = Analytics()

        self.build_interface()

    def build_interface(self):

        title = ctk.CTkLabel(
            self,
            text="Reports & Analytics",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        title.pack(
            pady=(25, 5)
        )

        subtitle = ctk.CTkLabel(
            self,
            text="SIWES Management System Statistics and Reports",
            font=ctk.CTkFont(size=14)
        )

        subtitle.pack(
            pady=(0, 25)
        )

        # Statistics section
        statistics_frame = ctk.CTkFrame(self)

        statistics_frame.pack(
            fill="x",
            padx=25,
            pady=10
        )

        self.student_label = self.create_stat_card(
            statistics_frame,
            "Students"
        )

        self.supervisor_label = self.create_stat_card(
            statistics_frame,
            "Supervisors"
        )

        self.organization_label = self.create_stat_card(
            statistics_frame,
            "Organizations"
        )

        self.placement_label = self.create_stat_card(
            statistics_frame,
            "Placements"
        )

        # Attendance
        attendance_frame = ctk.CTkFrame(self)

        attendance_frame.pack(
            fill="x",
            padx=25,
            pady=10
        )

        ctk.CTkLabel(
            attendance_frame,
            text="Attendance",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).pack(pady=(15, 5))

        self.attendance_label = ctk.CTkLabel(
            attendance_frame,
            text="Attendance: 0%"
        )

        self.attendance_label.pack(
            pady=(0, 15)
        )

        # Buttons
        button_frame = ctk.CTkFrame(self)

        button_frame.pack(
            fill="x",
            padx=25,
            pady=20
        )

        ctk.CTkButton(
            button_frame,
            text="Refresh Statistics",
            command=self.refresh_statistics
        ).pack(
            side="left",
            padx=10,
            pady=15
        )

        ctk.CTkButton(
            button_frame,
            text="Generate Charts",
            command=self.generate_charts
        ).pack(
            side="left",
            padx=10,
            pady=15
        )

        ctk.CTkButton(
            button_frame,
            text="Generate PDF",
            command=self.generate_pdf
        ).pack(
            side="left",
            padx=10,
            pady=15
        )

        self.refresh_statistics()

    def create_stat_card(self, parent, title):

        frame = ctk.CTkFrame(parent)

        frame.pack(
            side="left",
            expand=True,
            fill="both",
            padx=8,
            pady=15
        )

        ctk.CTkLabel(
            frame,
            text=title,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).pack(pady=(15, 5))

        value_label = ctk.CTkLabel(
            frame,
            text="0",
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            )
        )

        value_label.pack(
            pady=(0, 15)
        )

        return value_label

    def refresh_statistics(self):

        try:
            summary = self.analytics.get_summary()

            self.student_label.configure(
                text=str(summary["total_students"])
            )

            self.supervisor_label.configure(
                text=str(summary["total_supervisors"])
            )

            self.organization_label.configure(
                text=str(summary["total_organizations"])
            )

            self.placement_label.configure(
                text=str(summary["total_placements"])
            )

            self.attendance_label.configure(
                text=(
                    "Attendance: "
                    f"{summary['attendance']['percentage']}%"
                )
            )

        except Exception as error:

            messagebox.showerror(
                "Reports Error",
                f"Unable to load statistics:\n\n{error}"
            )

    def generate_charts(self):

        try:
            summary = self.analytics.get_summary()

            created = []

            placement_chart = create_placement_status_chart(
                summary["placement_status"]
            )

            if placement_chart:
                created.append(str(placement_chart))

            attendance_chart = create_attendance_chart(
                summary["attendance"]["present"],
                summary["attendance"]["absent"]
            )

            if attendance_chart:
                created.append(str(attendance_chart))

            logbook_chart = create_logbook_chart(
                summary["logbook"]["total_entries"],
                summary["logbook"]["approved"],
                summary["logbook"]["pending"]
            )

            if logbook_chart:
                created.append(str(logbook_chart))

            if created:
                messagebox.showinfo(
                    "Charts Generated",
                    "Charts generated successfully."
                )
            else:
                messagebox.showinfo(
                    "Charts",
                    "There is currently no data available "
                    "for generating charts."
                )

        except Exception as error:

            messagebox.showerror(
                "Chart Error",
                str(error)
            )

    def generate_pdf(self):

        messagebox.showinfo(
            "PDF Reports",
            "The PDF report generator is ready. "
            "It will be connected to the student/placement "
            "records during integration."
        )


if __name__ == "__main__":

    root = ctk.CTk()

    root.title(
        "SIWES Management System - Reports"
    )

    root.geometry("1000x700")

    reports = ReportsWindow(root)

    reports.pack(
        fill="both",
        expand=True
    )

    root.mainloop()