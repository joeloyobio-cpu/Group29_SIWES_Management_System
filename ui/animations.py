import tkinter as tk


# ============================================================
# WIDTH ANIMATION
# ============================================================

def animate_width(
    widget,
    start_width,
    end_width,
    duration=450,
    steps=25,
    on_complete=None
):
    """Smoothly animate a widget's width."""

    steps = max(1, steps)
    delay = max(1, duration // steps)
    difference = end_width - start_width

    def animate(step):
        progress = step / steps

        # Smooth ease-out
        eased = 1 - (1 - progress) ** 3

        width = int(
            start_width + difference * eased
        )

        try:
            widget.configure(width=width)
        except tk.TclError:
            return

        if step < steps:
            widget.after(
                delay,
                lambda: animate(step + 1)
            )
        elif on_complete:
            on_complete()

    widget.configure(width=start_width)
    animate(0)


# ============================================================
# SLIDE X
# ============================================================

def animate_slide_x(
    widget,
    start_x,
    end_x,
    duration=300,
    steps=20,
    on_complete=None
):
    """Smoothly move a widget horizontally."""

    steps = max(1, steps)
    delay = max(1, duration // steps)
    difference = end_x - start_x

    def animate(step):
        progress = step / steps
        eased = 1 - (1 - progress) ** 3

        x = int(
            start_x + difference * eased
        )

        try:
            widget.place_configure(x=x)
        except tk.TclError:
            return

        if step < steps:
            widget.after(
                delay,
                lambda: animate(step + 1)
            )
        elif on_complete:
            on_complete()

    widget.place_configure(x=start_x)
    animate(0)


# ============================================================
# SLIDE Y
# ============================================================

def animate_slide_y(
    widget,
    start_y,
    end_y,
    duration=300,
    steps=20,
    on_complete=None
):
    """Smoothly move a widget vertically."""

    steps = max(1, steps)
    delay = max(1, duration // steps)
    difference = end_y - start_y

    def animate(step):
        progress = step / steps
        eased = 1 - (1 - progress) ** 3

        y = int(
            start_y + difference * eased
        )

        try:
            widget.place_configure(y=y)
        except tk.TclError:
            return

        if step < steps:
            widget.after(
                delay,
                lambda: animate(step + 1)
            )
        elif on_complete:
            on_complete()

    widget.place_configure(y=start_y)
    animate(0)


# ============================================================
# HOVER EFFECT
# ============================================================

def add_hover_effect(
    widget,
    normal_color,
    hover_color
):
    """Add a mouse hover effect."""

    widget.bind(
        "<Enter>",
        lambda event: widget.configure(
            fg_color=hover_color
        )
    )

    widget.bind(
        "<Leave>",
        lambda event: widget.configure(
            fg_color=normal_color
        )
    )


# ============================================================
# PRESS EFFECT
# ============================================================

def add_press_effect(
    widget,
    normal_color,
    pressed_color
):
    """Add a visual mouse press effect."""

    widget.bind(
        "<ButtonPress-1>",
        lambda event: widget.configure(
            fg_color=pressed_color
        )
    )

    widget.bind(
        "<ButtonRelease-1>",
        lambda event: widget.configure(
            fg_color=normal_color
        )
    )


# ============================================================
# COUNTER ANIMATION
# ============================================================

def animate_counter(
    widget,
    start_value,
    end_value,
    duration=800,
    steps=30,
    prefix="",
    suffix=""
):
    """Animate a numerical value."""

    steps = max(1, steps)
    delay = max(1, duration // steps)
    difference = end_value - start_value

    def animate(step):
        progress = step / steps
        eased = 1 - (1 - progress) ** 3

        value = int(
            start_value + difference * eased
        )

        try:
            widget.configure(
                text=f"{prefix}{value}{suffix}"
            )
        except tk.TclError:
            return

        if step < steps:
            widget.after(
                delay,
                lambda: animate(step + 1)
            )

    animate(0)


# ============================================================
# LOADING DOTS
# ============================================================

def loading_dots(
    widget,
    base_text="Loading"
):
    """Animate loading dots.

    Returns a function that stops the animation.
    """

    running = True
    dot_count = 0

    def animate():
        nonlocal dot_count

        if not running:
            return

        dot_count = (
            dot_count + 1
        ) % 4

        try:
            widget.configure(
                text=(
                    base_text
                    + "." * dot_count
                )
            )
        except tk.TclError:
            return

        widget.after(
            350,
            animate
        )

    animate()

    def stop():
        nonlocal running
        running = False

    return stop