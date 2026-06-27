"""
quick_actions.py — Quick action buttons for the home page.

Shows a row of icon buttons (Add Task, Weather, Play Game)
that provide shortcuts to key features.

Usage:
    quick_actions()
"""

import reflex as rx
from Project.theme import COLORS


def quick_actions() -> rx.Component:
    """
    Render the quick action buttons row for the home page.
    Each button is an icon with a label below it.
    """
    return rx.box(
        rx.text(
            "Quick Actions",
            font_size="14px",
            font_weight="600",
            color=COLORS["text_secondary"],
            margin_bottom="12px",
        ),
        rx.flex(
            _action_button(
                icon_name="circle-plus",
                label="Add Task",
                href="/planner",
            ),
            _action_button(
                icon_name="cloud",
                label="Weather",
                href="/weather",
            ),
            _action_button(
                icon_name="gamepad-2",
                label="Play Game",
                href="/games",
            ),
            _action_button(
                icon_name="message-square",
                label="Chat",
                href="/chat",
            ),
            gap="16px",
        ),
        width="100%",
    )


def _action_button(
    icon_name: str,
    label: str,
    href: str,
) -> rx.Component:
    """
    Render a single quick action button (icon + label).

    Args:
        icon_name: Lucide icon name
        label: Text label below the icon
        href: Page to navigate to when clicked
    """
    return rx.link(
        rx.vstack(
            rx.box(
                rx.icon(
                    tag=icon_name,
                    size=22,
                    color=COLORS["primary"],
                ),
                width="52px",
                height="52px",
                display="flex",
                align_items="center",
                justify_content="center",
                border_radius="16px",
                background_color=COLORS["background_card"],
                border=f"1px solid {COLORS['border']}",
                box_shadow=COLORS["shadow_soft"],
                transition="all 0.2s ease",
                _hover={
                    "transform": "translateY(-3px)",
                    "box_shadow": COLORS["shadow_medium"],
                    "background_color": COLORS["primary_light"],
                },
            ),
            rx.text(
                label,
                font_size="11px",
                font_weight="500",
                color=COLORS["text_secondary"],
            ),
            align_items="center",
            gap="6px",
        ),
        href=href,
        text_decoration="none",
    )
