"""
weather_preview.py — Compact hourly weather strip for the home page.

Shows 3 time slots (Now, 1 PM, 3 PM) with weather icons and
temperatures in a horizontal row inside a warm gradient card.

Usage:
    weather_preview()
"""

import reflex as rx
from Project.theme import COLORS, GLASS_CARD_STYLE, CARD_HOVER
from Project.state.weather_state import WeatherState


def weather_preview() -> rx.Component:
    """
    Render the compact weather preview card for the home page.
    Shows 3 hourly forecasts in a row with a gradient background.
    """
    return rx.box(
        # ---- Section Title ----
        rx.text(
            "Weather",
            font_size="22px",
            font_weight="700",
            color=COLORS["text_primary"],
            margin_bottom="16px",
        ),

        # ---- Hourly Slots ----
        rx.flex(
            rx.foreach(
                WeatherState.hourly_preview,
                render_hourly_slot,
            ),
            gap="24px",
            width="100%",
        ),

        # ---- Card Styling ----
        style=GLASS_CARD_STYLE,
        _hover=CARD_HOVER,
        background=(
            f"linear-gradient(135deg, "
            f"{COLORS['background_card']} 0%, "
            f"{COLORS['gradient_warm_mid']} 100%)"
        ),
        width="100%",
    )


def render_hourly_slot(slot: dict) -> rx.Component:
    """
    Render a single hourly weather slot (time + icon + temp).

    Args:
        slot: A dict with "time", "icon", and "temp" keys.
    """
    return rx.vstack(
        # Time label
        rx.text(
            slot["time"],
            font_size="13px",
            font_weight="600",
            color=COLORS["text_accent"],
        ),
        # Weather icon
        rx.icon(
            tag=slot["icon"],
            size=24,
            color=COLORS["primary"],
        ),
        # Temperature
        rx.text(
            slot["temp"],
            font_size="20px",
            font_weight="700",
            color=COLORS["text_primary"],
        ),
        align_items="center",
        gap="8px",
    )
