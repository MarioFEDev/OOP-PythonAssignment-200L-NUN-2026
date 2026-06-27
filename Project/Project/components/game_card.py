"""
game_card.py — Game card for the games section.

Displays a game title, description, duration badge,
and icon. Each card has a distinct style based on game type.

Usage:
    # Inside rx.foreach:
    def render_game(game):
        return game_card(game)
"""

import reflex as rx
from Project.theme import COLORS, GLASS_CARD_STYLE, CARD_HOVER


def game_card(game: dict) -> rx.Component:
    """
    Render a single game card.

    Reads from the game dict:
        game["title"]       — Game name
        game["description"] — Short description
        game["duration"]    — Time estimate (e.g. "3 mins")
        game["icon"]        — Lucide icon name
        game["type"]        — "quiz", "puzzle", or "wellness"

    Args:
        game: A dict var from rx.foreach.
    """
    return rx.box(
        rx.vstack(
            # ---- Top Row: Duration Badge + Play Icon ----
            rx.flex(
                # Duration badge
                rx.flex(
                    rx.icon(
                        tag="clock",
                        size=14,
                        color=COLORS["text_secondary"],
                    ),
                    rx.text(
                        game["duration"],
                        font_size="12px",
                        font_weight="500",
                        color=COLORS["text_secondary"],
                    ),
                    gap="4px",
                    align_items="center",
                    background_color=COLORS["background_card"],
                    padding_left="10px",
                    padding_right="10px",
                    padding_top="4px",
                    padding_bottom="4px",
                    border_radius="20px",
                ),
                # Play button icon
                rx.box(
                    rx.icon(
                        tag="play",
                        size=16,
                        color=COLORS["primary"],
                    ),
                    width="32px",
                    height="32px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    background_color=COLORS["primary_light"],
                    border_radius="50%",
                    cursor="pointer",
                    transition="all 0.2s ease",
                    _hover={
                        "background_color": COLORS["primary"],
                        "color": COLORS["white"],
                    },
                ),
                justify="between",
                align_items="center",
                width="100%",
            ),

            # ---- Game Icon ----
            rx.box(
                rx.icon(
                    tag=game["icon"],
                    size=40,
                    color=COLORS["primary_dark"],
                    opacity="0.6",
                ),
                padding_top="12px",
                padding_bottom="4px",
            ),

            # ---- Title ----
            rx.text(
                game["title"],
                font_size="20px",
                font_weight="700",
                color=COLORS["text_primary"],
            ),

            # ---- Description ----
            rx.text(
                game["description"],
                font_size="14px",
                color=COLORS["text_secondary"],
                line_height="1.5",
            ),

            align_items="flex-start",
            gap="6px",
            width="100%",
        ),

        # ---- Card Styling ----
        style=GLASS_CARD_STYLE,
        _hover=CARD_HOVER,
        width="100%",
        cursor="pointer",
        on_click=rx.redirect(f"/games/" + game["id"]),
    )
