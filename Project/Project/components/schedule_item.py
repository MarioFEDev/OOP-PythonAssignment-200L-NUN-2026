"""
schedule_item.py — A single task row for the home page schedule preview.

Shows a colored left border, task title, time, optional "Moved" badge,
and a category icon on the right.

Usage:
    # Used inside rx.foreach on the home page:
    def render_schedule_item(task):
        return schedule_item(task)
"""

import reflex as rx
from Project.theme import COLORS


def schedule_item(task: dict) -> rx.Component:
    """
    Render a single schedule entry for the home page.

    Reads from the task dict:
        task["title"]    — The task name
        task["time"]     — The time string
        task["category"] — "work", "health", or "errands"
        task["status"]   — "scheduled" or "moved"
        task["icon"]     — Lucide icon name for the right side

    Args:
        task: A dict var from rx.foreach containing task data.
    """
    return rx.flex(
        # ---- Colored Left Border ----
        rx.box(
            width="4px",
            height="100%",
            min_height="50px",
            border_radius="4px",
            background_color=rx.cond(
                task["category"] == "work",
                COLORS["badge_work"],
                rx.cond(
                    task["category"] == "health",
                    COLORS["badge_health"],
                    COLORS["badge_errands"],
                ),
            ),
            flex_shrink="0",
        ),

        # ---- Task Info (middle) ----
        rx.vstack(
            rx.text(
                task["title"],
                font_size="15px",
                font_weight="600",
                color=COLORS["text_primary"],
            ),
            rx.flex(
                # Show "Moved" badge if status is "moved"
                rx.cond(
                    task["status"] == "moved",
                    rx.box(
                        rx.text(
                            "Moved",
                            font_size="11px",
                            font_weight="600",
                            color=COLORS["badge_moved"],
                        ),
                        background_color=COLORS["badge_moved_bg"],
                        padding_left="8px",
                        padding_right="8px",
                        padding_top="2px",
                        padding_bottom="2px",
                        border_radius="6px",
                    ),
                    rx.fragment(),
                ),
                rx.text(
                    task["time"],
                    font_size="13px",
                    color=COLORS["text_muted"],
                ),
                gap="8px",
                align_items="center",
            ),
            align_items="flex-start",
            gap="4px",
            flex="1",
        ),

        # ---- Category Icon (right side) ----
        rx.icon(
            tag=task["icon"],
            size=20,
            color=COLORS["text_muted"],
        ),

        # ---- Row Styling ----
        align_items="center",
        gap="12px",
        width="100%",
        padding_top="12px",
        padding_bottom="12px",
        border_bottom=f"1px solid {COLORS['border']}",
        transition="all 0.2s ease",
        _hover={
            "background_color": COLORS["primary_light"],
            "padding_left": "8px",
            "border_radius": "12px",
        },
    )
