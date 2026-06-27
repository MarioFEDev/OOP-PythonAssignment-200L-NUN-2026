"""
leaderboard_row.py — A single row in the weekly leaderboard.

Shows rank number, avatar circle with initials, player name,
and points. The current user's row is highlighted.

Usage:
    # Inside rx.foreach:
    def render_entry(entry):
        return leaderboard_row(entry)
"""

import reflex as rx
from Project.theme import COLORS


def leaderboard_row(entry: dict) -> rx.Component:
    """
    Render a single leaderboard entry.

    Reads from the entry dict:
        entry["rank"]     — Ranking number (e.g. "1")
        entry["name"]     — Player name
        entry["initials"] — Two-letter initials for the avatar
        entry["points"]   — Points display string
        entry["is_user"]  — "true" if this is the current user

    Args:
        entry: A dict var from rx.foreach.
    """
    return rx.flex(
        # ---- Rank Number ----
        rx.text(
            entry["rank"],
            font_size="16px",
            font_weight="700",
            color=rx.cond(
                entry["is_user"] == "true",
                COLORS["primary"],
                COLORS["text_secondary"],
            ),
            width="24px",
        ),

        # ---- Avatar Circle with Initials ----
        rx.box(
            rx.text(
                entry["initials"],
                font_size="12px",
                font_weight="700",
                color=COLORS["text_on_primary"],
            ),
            width="36px",
            height="36px",
            display="flex",
            align_items="center",
            justify_content="center",
            border_radius="50%",
            background_color=rx.cond(
                entry["is_user"] == "true",
                COLORS["primary"],
                COLORS["primary_dark"],
            ),
            flex_shrink="0",
        ),

        # ---- Player Name ----
        rx.text(
            entry["name"],
            font_size="15px",
            font_weight=rx.cond(
                entry["is_user"] == "true",
                "700",
                "500",
            ),
            color=COLORS["text_primary"],
            flex="1",
        ),

        # ---- Points ----
        rx.text(
            entry["points"],
            font_size="14px",
            font_weight="600",
            color=COLORS["text_secondary"],
        ),

        # ---- Row Styling ----
        align_items="center",
        gap="12px",
        width="100%",
        padding_top="10px",
        padding_bottom="10px",
        padding_left="8px",
        padding_right="8px",
        border_radius="12px",
        background_color=rx.cond(
            entry["is_user"] == "true",
            COLORS["primary_light"],
            "transparent",
        ),
        transition="all 0.2s ease",
        _hover={
            "background_color": COLORS["primary_light"],
        },
    )
