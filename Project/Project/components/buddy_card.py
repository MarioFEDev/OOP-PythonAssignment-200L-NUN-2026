"""
buddy_card.py — AI suggestion card with companion character.

This is the "BUDDY SUGGESTS" card that appears on the home page
and planner page. It shows the companion character (half-body)
next to the suggestion text, with action buttons.

The card has a warm gradient background with glassmorphism effects.

Usage:
    buddy_card()
    buddy_card(compact=True)   # Smaller version for planner page
"""

import reflex as rx
from Project.theme import COLORS, SUGGESTION_CARD_STYLE, CARD_HOVER
from Project.state.companion_state import CompanionState
from Project.state.user_state import UserState
from Project.components.buddy_avatar import buddy_avatar


def buddy_card(compact: bool = False) -> rx.Component:
    """
    Render the AI companion's suggestion card.

    Shows the character image beside the suggestion text,
    with "Yes, move it" and "Keep as is" action buttons.
    The entire card is wrapped in rx.cond so it only shows
    when CompanionState.is_suggestion_visible is True.

    Args:
        compact: If True, uses a smaller layout for the planner page.
    """
    # Choose avatar size based on compact mode
    if compact:
        avatar_size = "small"
    else:
        avatar_size = "medium"

    return rx.cond(
        CompanionState.is_suggestion_visible,
        # ---- Card Content (shown when visible) ----
        rx.box(
            rx.flex(
                # ---- Character Image (left side) ----
                buddy_avatar(size=avatar_size),

                # ---- Text Content (right side) ----
                rx.vstack(
                    # Label: "BUDDY SUGGESTS"
                    rx.text(
                        UserState.assistant_name, " SUGGESTS",
                        font_size="11px",
                        font_weight="700",
                        letter_spacing="0.05em",
                        color=COLORS["primary"],
                        text_transform="uppercase",
                    ),
                    # Suggestion text
                    rx.text(
                        CompanionState.suggestion_text,
                        font_size="15px",
                        font_weight="500",
                        color=COLORS["text_primary"],
                        line_height="1.5",
                    ),
                    # Action buttons
                    rx.flex(
                        # "Yes, move it" button (primary)
                        rx.box(
                            rx.text(
                                "Yes, move it",
                                font_size="13px",
                                font_weight="600",
                                color=COLORS["text_on_primary"],
                            ),
                            background_color=COLORS["primary"],
                            padding_left="16px",
                            padding_right="16px",
                            padding_top="8px",
                            padding_bottom="8px",
                            border_radius="10px",
                            cursor="pointer",
                            transition="all 0.2s ease",
                            _hover={
                                "background_color": COLORS["primary_hover"],
                                "transform": "scale(1.02)",
                            },
                            on_click=CompanionState.accept_suggestion,
                        ),
                        # "Keep as is" button (secondary)
                        rx.box(
                            rx.text(
                                "Keep as is",
                                font_size="13px",
                                font_weight="500",
                                color=COLORS["text_secondary"],
                            ),
                            background_color="transparent",
                            padding_left="16px",
                            padding_right="16px",
                            padding_top="8px",
                            padding_bottom="8px",
                            border_radius="10px",
                            border=f"1px solid {COLORS['border']}",
                            cursor="pointer",
                            transition="all 0.2s ease",
                            _hover={
                                "background_color": COLORS["primary_light"],
                                "color": COLORS["primary_dark"],
                            },
                            on_click=CompanionState.dismiss_suggestion,
                        ),
                        gap="10px",
                        flex_wrap="wrap",
                    ),
                    align_items="flex-start",
                    gap="10px",
                    flex="1",
                ),
                gap="16px",
                align_items="flex-start",
                width="100%",
            ),
            # ---- Card Container Styling ----
            style=SUGGESTION_CARD_STYLE,
            _hover=CARD_HOVER,
            animation="pulse_glow 4s ease-in-out infinite",
            width="100%",
        ),
        # ---- Empty placeholder when suggestion is hidden ----
        rx.fragment(),
    )
