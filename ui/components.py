import customtkinter as ctk

from ui.theme import (
    NAVY,
    NAVY_LIGHT,
    BLUE,
    BLUE_HOVER,
    WHITE,
    BACKGROUND,
    CARD,
    INPUT_BG,
    TEXT,
    TEXT_LIGHT,
    BORDER,
    SUCCESS,
    SUCCESS_HOVER,
    ERROR,
    ERROR_HOVER,
    CORNER_RADIUS,
    BUTTON_HEIGHT,
    INPUT_HEIGHT
)

from ui.animations import (
    add_hover_effect,
    add_press_effect
)


# ============================================================
# PAGE HEADER
# ============================================================

class PageHeader(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        title,
        subtitle="",
        action_text=None,
        action_command=None
    ):

        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.pack(
            fill="x",
            padx=40,
            pady=(25, 15)
        )

        # Left side
        text_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        text_frame.pack(
            side="left",
            fill="x",
            expand=True
        )

        title_label = ctk.CTkLabel(
            text_frame,
            text=title,
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            ),
            text_color=TEXT
        )

        title_label.pack(
            anchor="w"
        )

        if subtitle:

            subtitle_label = ctk.CTkLabel(
                text_frame,
                text=subtitle,
                font=ctk.CTkFont(
                    size=14
                ),
                text_color=TEXT_LIGHT
            )

            subtitle_label.pack(
                anchor="w",
                pady=(4, 0)
            )

        # Action button
        if action_text and action_command:

            button = PrimaryButton(
                self,
                text=action_text,
                command=action_command,
                width=150
            )

            button.pack(
                side="right"
            )


# ============================================================
# CARD
# ============================================================

class Card(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        **kwargs
    ):

        super().__init__(
            parent,
            fg_color=CARD,
            corner_radius=CORNER_RADIUS,
            border_width=1,
            border_color=BORDER,
            **kwargs
        )


# ============================================================
# STAT CARD
# ============================================================

class StatCard(Card):

    def __init__(
        self,
        parent,
        title,
        value,
        subtitle="",
        **kwargs
    ):

        super().__init__(
            parent,
            **kwargs
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=TEXT_LIGHT
        )

        title_label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(18, 2)
        )

        value_label = ctk.CTkLabel(
            self,
            text=str(value),
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            ),
            text_color=TEXT
        )

        value_label.grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 2)
        )

        if subtitle:

            subtitle_label = ctk.CTkLabel(
                self,
                text=subtitle,
                font=ctk.CTkFont(
                    size=12
                ),
                text_color=TEXT_LIGHT
            )

            subtitle_label.grid(
                row=2,
                column=0,
                sticky="w",
                padx=20,
                pady=(0, 18)
            )


# ============================================================
# SECTION HEADER
# ============================================================

class SectionHeader(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        title,
        subtitle=""
    ):

        super().__init__(
            parent,
            fg_color="transparent"
        )

        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            ),
            text_color=TEXT
        )

        title_label.pack(
            anchor="w"
        )

        if subtitle:

            subtitle_label = ctk.CTkLabel(
                self,
                text=subtitle,
                font=ctk.CTkFont(
                    size=13
                ),
                text_color=TEXT_LIGHT
            )

            subtitle_label.pack(
                anchor="w",
                pady=(3, 0)
            )


# ============================================================
# PRIMARY BUTTON
# ============================================================

class PrimaryButton(ctk.CTkButton):

    def __init__(
        self,
        parent,
        text,
        command=None,
        width=140,
        **kwargs
    ):

        super().__init__(
            parent,
            text=text,
            command=command,
            width=width,
            height=BUTTON_HEIGHT,
            corner_radius=CORNER_RADIUS,
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
            text_color=WHITE,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            **kwargs
        )

        add_press_effect(
            self,
            BLUE,
            "#1D4ED8"
        )


# ============================================================
# SECONDARY BUTTON
# ============================================================

class SecondaryButton(ctk.CTkButton):

    def __init__(
        self,
        parent,
        text,
        command=None,
        width=120,
        **kwargs
    ):

        super().__init__(
            parent,
            text=text,
            command=command,
            width=width,
            height=BUTTON_HEIGHT,
            corner_radius=CORNER_RADIUS,
            fg_color="#64748B",
            hover_color="#475569",
            text_color=WHITE,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            **kwargs
        )

        add_press_effect(
            self,
            "#64748B",
            "#334155"
        )


# ============================================================
# SUCCESS BUTTON
# ============================================================

class SuccessButton(ctk.CTkButton):

    def __init__(
        self,
        parent,
        text,
        command=None,
        width=140,
        **kwargs
    ):

        super().__init__(
            parent,
            text=text,
            command=command,
            width=width,
            height=BUTTON_HEIGHT,
            corner_radius=CORNER_RADIUS,
            fg_color=SUCCESS,
            hover_color=SUCCESS_HOVER,
            text_color=WHITE,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            **kwargs
        )

        add_press_effect(
            self,
            SUCCESS,
            "#166534"
        )


# ============================================================
# DANGER BUTTON
# ============================================================

class DangerButton(ctk.CTkButton):

    def __init__(
        self,
        parent,
        text,
        command=None,
        width=120,
        **kwargs
    ):

        super().__init__(
            parent,
            text=text,
            command=command,
            width=width,
            height=BUTTON_HEIGHT,
            corner_radius=CORNER_RADIUS,
            fg_color=ERROR,
            hover_color=ERROR_HOVER,
            text_color=WHITE,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            **kwargs
        )

        add_press_effect(
            self,
            ERROR,
            "#991B1B"
        )


# ============================================================
# FORM FIELD
# ============================================================

class FormField(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        label,
        placeholder="",
        value="",
        password=False,
        **kwargs
    ):

        super().__init__(
            parent,
            fg_color="transparent",
            **kwargs
        )

        label_widget = ctk.CTkLabel(
            self,
            text=label,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=TEXT
        )

        label_widget.pack(
            anchor="w",
            pady=(0, 6)
        )

        self.entry = ctk.CTkEntry(
            self,
            height=INPUT_HEIGHT,
            placeholder_text=placeholder,
            fg_color=WHITE,
            text_color=TEXT,
            placeholder_text_color="#94A3B8",
            border_color=BORDER,
            border_width=1,
            corner_radius=CORNER_RADIUS,
            show="•" if password else ""
        )

        self.entry.pack(
            fill="x"
        )

        if value:
            self.entry.insert(
                0,
                value
            )

    def get(self):
        return self.entry.get().strip()

    def set(self, value):
        self.entry.delete(
            0,
            "end"
        )

        self.entry.insert(
            0,
            value or ""
        )

    def clear(self):
        self.entry.delete(
            0,
            "end"
        )


# ============================================================
# STATUS BADGE
# ============================================================

class StatusBadge(ctk.CTkLabel):

    def __init__(
        self,
        parent,
        status
    ):

        status_lower = str(
            status
        ).lower()

        if status_lower in (
            "approved",
            "present",
            "completed",
            "active",
            "success"
        ):

            bg = "#DCFCE7"
            fg = SUCCESS

        elif status_lower in (
            "rejected",
            "absent",
            "failed",
            "inactive",
            "error"
        ):

            bg = "#FEE2E2"
            fg = ERROR

        elif status_lower in (
            "pending",
            "warning"
        ):

            bg = "#FEF3C7"
            fg = "#B45309"

        else:

            bg = "#E2E8F0"
            fg = TEXT_LIGHT

        super().__init__(
            parent,
            text=str(status),
            fg_color=bg,
            text_color=fg,
            corner_radius=8,
            padx=10,
            pady=5,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        )


# ============================================================
# EMPTY STATE
# ============================================================

class EmptyState(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        title="Nothing to display",
        message=""
    ):

        super().__init__(
            parent,
            fg_color=CARD,
            corner_radius=CORNER_RADIUS,
            border_width=1,
            border_color=BORDER
        )

        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            ),
            text_color=TEXT
        )

        title_label.pack(
            pady=(30, 5)
        )

        if message:

            message_label = ctk.CTkLabel(
                self,
                text=message,
                font=ctk.CTkFont(
                    size=13
                ),
                text_color=TEXT_LIGHT
            )

            message_label.pack(
                pady=(0, 30)
            )