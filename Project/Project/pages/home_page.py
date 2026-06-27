"""
home_page.py — The main home screen.

This is the first page the user sees. It shows:
1. A greeting with the user's name
2. The AI buddy's suggestion card (weather + schedule advice)
3. Today's schedule preview (3 tasks)
4. A compact weather preview strip
5. Quick action buttons
6. A floating buddy character in the corner
7. Bottom navigation bar

Route: /
"""

import reflex as rx
from Project.theme import COLORS, PAGE_BACKGROUND_STYLE, GLASS_CARD_STYLE, CARD_HOVER
from Project.state.app_state import AppState
from Project.state.planner_state import PlannerState
from Project.state.weather_state import WeatherState
from Project.state.user_state import UserState
from Project.components.navbar import navbar
from Project.components.buddy_card import buddy_card
from Project.components.buddy_avatar import buddy_avatar
from Project.components.schedule_item import schedule_item
from Project.components.weather_preview import weather_preview
from Project.components.quick_actions import quick_actions


def home_page() -> rx.Component:
    """Render the complete home page."""
    return rx.box(
        # ---- Scrollable Content Area ----
        rx.vstack(
            # ==============================
            # SECTION 1: Header / Greeting
            # ==============================
            rx.flex(
                # Left side: Greeting text
                rx.vstack(
                    rx.heading(
                        rx.text.span("Hi "),
                        rx.text.span(
                            UserState.user_name,
                            color=COLORS["primary_dark"],
                        ),
                        font_size="28px",
                        font_weight="800",
                        color=COLORS["text_primary"],
                    ),
                    rx.text(
                        "Here's your day",
                        font_size="15px",
                        color=COLORS["text_secondary"],
                    ),
                    align_items="flex-start",
                    gap="4px",
                ),
                # Right side: User avatar
                rx.box(
                    rx.image(
                        src=UserState.assistant_image,
                        alt="User Avatar",
                        width="100%",
                        height="100%",
                        object_fit="cover",
                        border_radius="50%",
                    ),
                    width="44px",
                    height="44px",
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
            # SECTION 2: Buddy Suggestion Card
            # ==============================
            buddy_card(compact=False),

            # ==============================
            # SECTION 3: Today's Schedule
            # ==============================
            rx.box(
                # Section header
                rx.flex(
                    rx.text(
                        "Today's Schedule",
                        font_size="20px",
                        font_weight="700",
                        color=COLORS["text_primary"],
                    ),
                    rx.icon(
                        tag="ellipsis",
                        size=20,
                        color=COLORS["text_muted"],
                        cursor="pointer",
                    ),
                    justify="between",
                    align_items="center",
                    width="100%",
                    margin_bottom="8px",
                ),
                # Task list
                rx.vstack(
                    rx.foreach(
                        PlannerState.home_schedule,
                        schedule_item,
                    ),
                    width="100%",
                    gap="0px",
                ),
                # "View Full Planner" link
                rx.link(
                    rx.box(
                        rx.text(
                            "View Full Planner",
                            font_size="14px",
                            font_weight="600",
                            color=COLORS["text_accent"],
                            text_align="center",
                        ),
                        width="100%",
                        padding_top="12px",
                        padding_bottom="12px",
                        border=f"1px solid {COLORS['border']}",
                        border_radius="12px",
                        margin_top="12px",
                        cursor="pointer",
                        transition="all 0.2s ease",
                        _hover={
                            "background_color": COLORS["primary_light"],
                        },
                    ),
                    href="/planner",
                    width="100%",
                    text_decoration="none",
                ),
                width="100%",
            ),

            # ==============================
            # SECTION 4: Weather Preview
            # ==============================
            weather_preview(),

            # ==============================
            # SECTION 5: Quick Actions
            # ==============================
            quick_actions(),

            # ---- Bottom padding for navbar ----
            rx.box(height="100px"),

            # ---- VStack Layout Settings ----
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
        # FLOATING BUDDY (bottom-right corner)
        # ==============================
        rx.box(
            # Speech bubble
            rx.box(
                rx.text(
                    "I'm here if you need anything!",
                    font_size="12px",
                    color=COLORS["text_secondary"],
                    font_style="italic",
                ),
                background_color=COLORS["background_card"],
                padding="8px 12px",
                border_radius="12px 12px 0px 12px",
                box_shadow=COLORS["shadow_soft"],
                position="absolute",
                bottom="70px",
                right="60px",
                white_space="nowrap",
            ),
            # Character image
            buddy_avatar(size="peek", enable_float=True),
            position="fixed",
            bottom="90px",
            right="calc(50% - 195px)",
            z_index="40",
        ),

        # ==============================
        # BOTTOM NAVBAR
        # ==============================
        navbar(active_page="home"),

        # ---- Page Background ----
        style=PAGE_BACKGROUND_STYLE,
        display="flex",
        flex_direction="column",
        align_items="center",
        overflow_y="auto",
        on_mount=[UserState.check_setup, WeatherState.fetch_weather],
    )
