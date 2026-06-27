"""
weather_detail_card.py — Weather stat card (Humidity, Wind, Rain).

A small card showing a single weather stat with an icon,
value, and label. Used on the weather page in a row of 3.

Usage:
    weather_detail_card(icon="droplets", value="45%", label="Humidity")
"""

import reflex as rx
from Project.theme import COLORS, GLASS_CARD_STYLE


def weather_detail_card(
    icon_name: str,
    value: str,
    label: str,
) -> rx.Component:
    """
    Render a single weather stat card.

    Args:
        icon_name: Lucide icon name (e.g. "droplets", "wind", "cloud-rain")
        value: The stat value (e.g. "45%", "12mph")
        label: The stat label (e.g. "Humidity", "Wind")
    """
    return rx.vstack(
        # Stat icon
        rx.icon(
            tag=icon_name,
            size=20,
            color=COLORS["primary"],
        ),
        # Stat value (large)
        rx.text(
            value,
            font_size="22px",
            font_weight="700",
            color=COLORS["text_primary"],
        ),
        # Stat label (small)
        rx.text(
            label,
            font_size="12px",
            font_weight="500",
            color=COLORS["text_muted"],
        ),
        align_items="center",
        gap="4px",
        padding_top="16px",
        padding_bottom="16px",
        padding_left="12px",
        padding_right="12px",
        background=COLORS["background_card"],
        border_radius="16px",
        border=f"1px solid {COLORS['border']}",
        box_shadow=COLORS["shadow_soft"],
        flex="1",
        transition="all 0.2s ease",
        _hover={
            "transform": "translateY(-2px)",
            "box_shadow": COLORS["shadow_medium"],
        },
    )
