"""
task_item.py — A single task row for the planner page.

Shows a checkbox, task title, time, category badge, and
edit/delete action icons. Used inside rx.foreach on the planner page.
"""

import reflex as rx
from Project.theme import COLORS
from Project.state.planner_state import PlannerState


def task_item(task: dict) -> rx.Component:
    """
    Render a single planner task row with actions.

    task keys: id, title, time, category, period, is_done
    """
    is_done = task["is_done"] == "true"

    # Category badge colour helpers
    badge_color = rx.cond(
        task["category"] == "health",
        COLORS["badge_health"],
        rx.cond(
            task["category"] == "work",
            COLORS["badge_work"],
            rx.cond(
                task["category"] == "errands",
                COLORS["badge_errands"],
                COLORS["text_muted"],  # personal / other
            ),
        ),
    )
    badge_bg = rx.cond(
        task["category"] == "health",
        COLORS["badge_health_bg"],
        rx.cond(
            task["category"] == "work",
            COLORS["badge_work_bg"],
            rx.cond(
                task["category"] == "errands",
                COLORS["badge_errands_bg"],
                "rgba(168,149,133,0.12)",
            ),
        ),
    )
    badge_label = rx.cond(
        task["category"] == "health",
        "Health",
        rx.cond(
            task["category"] == "work",
            "Work",
            rx.cond(
                task["category"] == "errands",
                "Errands",
                "Personal",
            ),
        ),
    )

    return rx.flex(
        # ---- Checkbox ----
        rx.box(
            rx.cond(
                task["is_done"] == "true",
                rx.icon(tag="square-check", size=22, color=COLORS["primary"]),
                rx.icon(tag="square", size=22, color=COLORS["text_muted"]),
            ),
            cursor="pointer",
            on_click=PlannerState.toggle_task(task["id"]),
            flex_shrink="0",
        ),

        # ---- Task Info (middle) ----
        rx.vstack(
            rx.text(
                task["title"],
                font_size="15px",
                font_weight="600",
                color=rx.cond(
                    task["is_done"] == "true",
                    COLORS["text_muted"],
                    COLORS["text_primary"],
                ),
                text_decoration=rx.cond(
                    task["is_done"] == "true",
                    "line-through",
                    "none",
                ),
            ),
            rx.flex(
                rx.icon(tag="clock", size=13, color=COLORS["text_muted"]),
                rx.text(
                    task["time"],
                    font_size="12px",
                    color=COLORS["text_muted"],
                ),
                gap="5px",
                align_items="center",
            ),
            align_items="flex-start",
            gap="3px",
            flex="1",
            min_width="0",
        ),

        # ---- Right side: badge + actions ----
        rx.vstack(
            # Category badge
            rx.box(
                rx.text(
                    badge_label,
                    font_size="11px",
                    font_weight="600",
                    color=badge_color,
                ),
                background_color=badge_bg,
                padding_left="10px",
                padding_right="10px",
                padding_top="3px",
                padding_bottom="3px",
                border_radius="20px",
                flex_shrink="0",
            ),
            # Edit + Delete icons
            rx.flex(
                # Edit button
                rx.box(
                    rx.icon(tag="pencil", size=14, color=COLORS["text_secondary"]),
                    cursor="pointer",
                    padding="4px",
                    border_radius="6px",
                    transition="all 0.15s ease",
                    on_click=PlannerState.start_edit(task["id"]),
                    _hover={
                        "background_color": COLORS["primary_light"],
                        "color": COLORS["primary"],
                    },
                ),
                # Delete button
                rx.box(
                    rx.icon(tag="trash-2", size=14, color="#E53935"),
                    cursor="pointer",
                    padding="4px",
                    border_radius="6px",
                    transition="all 0.15s ease",
                    on_click=PlannerState.delete_task(task["id"]),
                    _hover={
                        "background_color": "rgba(229,57,53,0.10)",
                    },
                ),
                gap="2px",
                align_items="center",
            ),
            align_items="flex-end",
            gap="4px",
            flex_shrink="0",
        ),

        # ---- Row Styling ----
        align_items="center",
        gap="12px",
        width="100%",
        padding_top="14px",
        padding_bottom="14px",
        padding_left="4px",
        padding_right="4px",
        border_bottom=f"1px solid {COLORS['border']}",
        transition="all 0.2s ease",
        _hover={
            "background_color": COLORS["primary_light"],
            "padding_left": "10px",
            "padding_right": "10px",
            "border_radius": "12px",
        },
    )
