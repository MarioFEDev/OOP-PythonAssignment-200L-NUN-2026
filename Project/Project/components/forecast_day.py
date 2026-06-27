"""
forecast_day.py — Single day column for the weekly forecast.

Shows the day name, a weather icon, and high/low temperatures.
Used inside the weather page's forecast grid.

Usage:
    # Inside rx.foreach:
    def render_forecast(day_data):
        return forecast_day(day_data)
"""

import reflex as rx
from Project.theme import COLORS


def forecast_day(day_data: dict) -> rx.Component:
    """
    Render a single day's forecast column.

    Reads from the day_data dict:
        day_data["day"]  — Day name (e.g. "Mon")
        day_data["icon"] — Lucide icon name
        day_data["high"] — High temperature (e.g. "74°")
        day_data["low"]  — Low temperature (e.g. "62°")

    Args:
        day_data: A dict var from rx.foreach.
    """
    return rx.vstack(
        # Day name
        rx.text(
            day_data["day"],
            font_size="13px",
            font_weight="600",
            color=COLORS["text_secondary"],
        ),
        # Weather icon
        rx.icon(
            tag=day_data["icon"],
            size=28,
            color=COLORS["primary"],
        ),
        # High / Low temps
        rx.flex(
            rx.text(
                day_data["high"],
                font_size="15px",
                font_weight="700",
                color=COLORS["text_primary"],
            ),
            rx.text(
                day_data["low"],
                font_size="13px",
                font_weight="400",
                color=COLORS["text_muted"],
            ),
            gap="6px",
        ),
        align_items="center",
        gap="8px",
        padding_top="12px",
        padding_bottom="12px",
        transition="all 0.2s ease",
        _hover={
            "transform": "scale(1.05)",
        },
    )
