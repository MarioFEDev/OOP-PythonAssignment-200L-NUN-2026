"""
games_page.py — Mini-games section.

Shows available games (Daily Quiz, Memory Match, Mood Booster),
a streak counter, and a weekly leaderboard.

Route: /games
"""

import reflex as rx
from Project.theme import COLORS, PAGE_BACKGROUND_STYLE
from Project.state.app_state import AppState
from Project.state.games_state import GamesState
from Project.state.user_state import UserState
from Project.components.navbar import navbar
from Project.components.game_card import game_card
from Project.components.leaderboard_row import leaderboard_row


def games_page() -> rx.Component:
    """Render the complete games page."""
    return rx.box(
        rx.vstack(
            # ==============================
            # SECTION 1: Header
            # ==============================
            rx.flex(
                # Left: App icon
                rx.icon(
                    tag="gamepad-2",
                    size=22,
                    color=COLORS["primary"],
                ),
                # Center: App name
                rx.text(
                    UserState.assistant_name,
                    font_size="20px",
                    font_weight="800",
                    color=COLORS["primary_dark"],
                ),
                # Right: User avatar
                rx.box(
                    rx.image(
                        src=UserState.assistant_image,
                        alt="User Avatar",
                        width="100%",
                        height="100%",
                        object_fit="cover",
                        border_radius="50%",
                    ),
                    width="36px",
                    height="36px",
                    border_radius="50%",
                    border=f"2px solid {COLORS['primary_light']}",
                    overflow="hidden",
                    flex_shrink="0",
                ),
                justify="between",
                align_items="center",
                width="100%",
            ),

            # ==============================
            # SECTION 2: Play & Recharge Header
            # ==============================
            rx.flex(
                # Left: Title + subtitle
                rx.vstack(
                    rx.text(
                        "Play & Recharge",
                        font_size="22px",
                        font_weight="700",
                        color=COLORS["text_primary"],
                    ),
                    rx.text(
                        "Take a quick break, you've earned it.",
                        font_size="14px",
                        color=COLORS["text_secondary"],
                    ),
                    align_items="flex-start",
                    gap="4px",
                ),
                # Right: Streak badge
                rx.flex(
                    rx.icon(
                        tag="flame",
                        size=16,
                        color=COLORS["streak_text"],
                    ),
                    rx.text(
                        GamesState.streak_text,
                        font_size="12px",
                        font_weight="600",
                        color=COLORS["streak_text"],
                    ),
                    gap="4px",
                    align_items="center",
                    background_color=COLORS["streak_bg"],
                    padding_left="12px",
                    padding_right="12px",
                    padding_top="6px",
                    padding_bottom="6px",
                    border_radius="20px",
                    flex_shrink="0",
                ),
                justify="between",
                align_items="flex-start",
                width="100%",
            ),

            # ==============================
            # SECTION 3: Game Cards
            # ==============================
            rx.vstack(
                rx.foreach(
                    GamesState.games,
                    game_card,
                ),
                width="100%",
                gap="16px",
            ),

            # ==============================
            # SECTION 4: Weekly Leaderboard
            # ==============================
            rx.box(
                # Section header
                rx.flex(
                    rx.text(
                        "Weekly Leaderboard",
                        font_size="20px",
                        font_weight="700",
                        color=COLORS["text_primary"],
                    ),
                    rx.text(
                        "View All",
                        font_size="14px",
                        font_weight="600",
                        color=COLORS["text_accent"],
                        cursor="pointer",
                        _hover={
                            "text_decoration": "underline",
                        },
                    ),
                    justify="between",
                    align_items="center",
                    width="100%",
                    margin_bottom="12px",
                ),
                # Leaderboard entries
                rx.vstack(
                    rx.foreach(
                        GamesState.leaderboard,
                        leaderboard_row,
                    ),
                    width="100%",
                    gap="0px",
                ),
                width="100%",
            ),

            # ---- Bottom padding for navbar ----
            rx.box(height="100px"),

            # ---- VStack Layout ----
            width="100%",
            max_width="430px",
            padding_left="20px",
            padding_right="20px",
            padding_top="20px",
            gap="24px",
            align_items="stretch",
            animation="slide_up 0.5s ease-out",
        ),

        # ==============================
        # BOTTOM NAVBAR (Home stays active for games)
        # ==============================
        navbar(active_page="home"),

        # ---- Page Background ----
        style=PAGE_BACKGROUND_STYLE,
        display="flex",
        flex_direction="column",
        align_items="center",
        overflow_y="auto",
        on_mount=UserState.check_setup,
    )
