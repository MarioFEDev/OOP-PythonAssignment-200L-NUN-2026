"""
chat_page.py — AI companion chat interface.

A full chat screen with the buddy character displayed at the top,
a scrollable message area with chat bubbles, quick suggestion
chips, and a text input bar at the bottom.

Route: /chat
"""

import reflex as rx
from Project.theme import COLORS, PAGE_BACKGROUND_STYLE, GLASS_CARD_STYLE
from Project.state.app_state import AppState
from Project.state.chat_state import ChatState
from Project.state.companion_state import CompanionState
from Project.state.user_state import UserState
from Project.state.planner_state import PlannerState
from Project.state.weather_state import WeatherState
from Project.components.navbar import navbar
from Project.components.buddy_avatar import buddy_avatar
from Project.components.chat_bubble import chat_bubble


def chat_page() -> rx.Component:
    """Render the complete chat page."""
    return rx.box(
        rx.vstack(
            # ==============================
            # SECTION 1: Header
            # ==============================
            rx.flex(
                # Left: Settings icon
                rx.icon(
                    tag="settings",
                    size=22,
                    color=COLORS["text_secondary"],
                    cursor="pointer",
                ),
                # Center: App name and Model Toggle
                rx.vstack(
                    rx.text(
                        UserState.assistant_name,
                        font_size="20px",
                        font_weight="800",
                        color=COLORS["primary_dark"],
                    ),
                    rx.select(
                        ["gemini", "groq"],
                        value=ChatState.model_provider,
                        on_change=ChatState.set_model_provider,
                        size="1",
                        variant="soft",
                        color_scheme="gray",
                        radius="full",
                    ),
                    align_items="center",
                    gap="2px",
                ),
                # Right: User icon
                rx.icon(
                    tag="user",
                    size=22,
                    color=COLORS["text_secondary"],
                    cursor="pointer",
                ),
                justify="between",
                align_items="center",
                width="100%",
            ),

            # ==============================
            # SECTION 2: Character Display
            # ==============================
            rx.vstack(
                # Full-body character image centered
                rx.box(
                    buddy_avatar(size="hero", enable_float=True),
                    display="flex",
                    justify_content="center",
                    width="100%",
                ),
                # "Your Buddy is listening" text
                rx.text(
                    UserState.assistant_name, " is listening",
                    font_size="14px",
                    font_weight="500",
                    color=COLORS["text_secondary"],
                ),
                align_items="center",
                gap="8px",
                padding_top="8px",
                padding_bottom="8px",
                background=COLORS["background_glass"],
                backdrop_filter="blur(16px)",
                border_radius="20px",
                width="100%",
            ),

            # ==============================
            # SECTION 3: Date Divider
            # ==============================
            rx.flex(
                rx.box(
                    rx.text(
                        "Today",
                        font_size="12px",
                        font_weight="600",
                        color=COLORS["text_muted"],
                    ),
                    background_color=COLORS["background_card"],
                    padding_left="16px",
                    padding_right="16px",
                    padding_top="4px",
                    padding_bottom="4px",
                    border_radius="20px",
                    border=f"1px solid {COLORS['border']}",
                ),
                justify="center",
                width="100%",
                padding_top="8px",
                padding_bottom="8px",
            ),

            # ==============================
            # SECTION 4: Chat Messages
            # ==============================
            rx.vstack(
                rx.foreach(
                    ChatState.messages,
                    chat_bubble,
                ),
                width="100%",
                gap="4px",
                flex="1",
                overflow_y="auto",
                min_height="250px",
            ),

            # ==============================
            # SECTION 5: Quick Suggestion Chips
            # ==============================
            rx.flex(
                rx.foreach(
                    ChatState.quick_suggestions,
                    render_suggestion_chip,
                ),
                gap="8px",
                overflow_x="auto",
                width="100%",
                padding_top="8px",
                padding_bottom="8px",
                flex_shrink="0",
            ),

            # ==============================
            # SECTION 6: Input Bar
            # ==============================
            rx.flex(
                # Plus icon
                rx.box(
                    rx.icon(
                        tag="circle-plus",
                        size=24,
                        color=COLORS["primary"],
                    ),
                    cursor="pointer",
                    flex_shrink="0",
                ),
                # Text input
                rx.input(
                    placeholder="Talk to " + UserState.assistant_name + "...",
                    value=ChatState.current_input,
                    on_change=ChatState.set_input,
                    variant="soft",
                    radius="full",
                    size="3",
                    width="100%",
                    color=COLORS["text_primary"],
                ),
                # Send button
                rx.box(
                    rx.icon(
                        tag="send",
                        size=18,
                        color=COLORS["text_on_primary"],
                    ),
                    width="40px",
                    height="40px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    border_radius="50%",
                    background_color=COLORS["primary"],
                    cursor="pointer",
                    flex_shrink="0",
                    transition="all 0.2s ease",
                    _hover={
                        "background_color": COLORS["primary_hover"],
                        "transform": "scale(1.05)",
                    },
                    on_click=ChatState.send_message,
                ),
                gap="10px",
                align_items="center",
                width="100%",
                padding_top="8px",
                padding_bottom="8px",
                flex_shrink="0",
            ),

            # ---- Bottom padding for navbar ----
            rx.box(height="80px", flex_shrink="0"),

            # ---- VStack Layout ----
            width="100%",
            max_width="430px",
            padding_left="16px",
            padding_right="16px",
            padding_top="16px",
            gap="4px",
            align_items="stretch",
            min_height="100vh",
            animation="fade_in 0.4s ease-out",
        ),

        # ==============================
        # BOTTOM NAVBAR
        # ==============================
        navbar(active_page="chat"),

        # ---- Page Background ----
        style=PAGE_BACKGROUND_STYLE,
        display="flex",
        flex_direction="column",
        align_items="center",
        overflow_y="auto",
        on_mount=[UserState.check_setup, WeatherState.fetch_weather],
    )


def render_suggestion_chip(suggestion: rx.Var[str]) -> rx.Component:
    """
    Render a single quick suggestion chip button.

    Args:
        suggestion: The suggestion text from rx.foreach.
    """
    return rx.box(
        rx.flex(
            rx.icon(
                tag="sparkles",
                size=14,
                color=COLORS["primary"],
            ),
            rx.text(
                suggestion,
                font_size="13px",
                font_weight="500",
                color=COLORS["text_primary"],
            ),
            gap="6px",
            align_items="center",
        ),
        background_color=COLORS["background_card"],
        border=f"1px solid {COLORS['border']}",
        border_radius="20px",
        padding_left="14px",
        padding_right="14px",
        padding_top="8px",
        padding_bottom="8px",
        cursor="pointer",
        white_space="nowrap",
        flex_shrink="0",
        transition="all 0.2s ease",
        _hover={
            "background_color": COLORS["primary_light"],
            "border_color": COLORS["primary"],
        },
        on_click=ChatState.send_quick_suggestion(suggestion),
    )
