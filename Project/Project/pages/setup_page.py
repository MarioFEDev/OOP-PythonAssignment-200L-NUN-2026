"""
setup_page.py — First-launch onboarding screen.

Three-step card UI:
  1. Enter your name
  2. Pick your city (guided dropdown — unambiguous lat/lon)
  3. Choose your assistant (5 styled cards)

On completion, saves to localStorage via UserState and redirects to /.

Route: /setup
"""

import reflex as rx
from Project.theme import COLORS, PAGE_BACKGROUND_STYLE
from Project.state.user_state import UserState, ASSISTANTS, CITY_NAMES


# ---------------------------------------------------------------------------
# Sub-components
# ---------------------------------------------------------------------------

def _step_dot(n: int, active: bool) -> rx.Component:
    """A progress indicator dot."""
    return rx.box(
        width="8px",
        height="8px",
        border_radius="50%",
        background_color=COLORS["primary"] if active else COLORS["border"],
        transition="all 0.3s ease",
    )


def _section_label(text: str) -> rx.Component:
    return rx.text(
        text,
        font_size="12px",
        font_weight="700",
        color=COLORS["primary"],
        letter_spacing="0.08em",
        text_transform="uppercase",
        margin_bottom="6px",
    )


def _assistant_card(info: dict) -> rx.Component:
    """One selectable assistant card."""
    aid = info["id"]
    is_selected = UserState.form_assistant_id == aid
    return rx.box(
        rx.vstack(
            # Avatar circle
            rx.box(
                rx.image(
                    src=info["greeting_image"],
                    width="56px",
                    height="56px",
                    object_fit="cover",
                    border_radius="50%",
                ),
                width="64px",
                height="64px",
                border_radius="50%",
                display="flex",
                align_items="center",
                justify_content="center",
                background_color=info["accent_light"],
                border=rx.cond(
                    is_selected,
                    f"3px solid {info['accent']}",
                    "3px solid transparent",
                ),
                transition="all 0.2s ease",
                overflow="hidden",
            ),
            # Name
            rx.text(
                info["name"],
                font_size="14px",
                font_weight="700",
                color=rx.cond(is_selected, info["accent"], COLORS["text_primary"]),
                transition="all 0.2s ease",
            ),
            # Personality tag
            rx.text(
                info["short_desc"],
                font_size="11px",
                color=COLORS["text_muted"],
                text_align="center",
                line_height="1.3",
            ),
            align_items="center",
            gap="6px",
        ),
        padding="14px 10px",
        border_radius="16px",
        border=rx.cond(
            is_selected,
            f"2px solid {info['accent']}",
            f"2px solid {COLORS['border']}",
        ),
        background_color=rx.cond(
            is_selected,
            info["accent_light"],
            COLORS["background_card"],
        ),
        cursor="pointer",
        transition="all 0.2s ease",
        on_click=UserState.set_form_assistant(aid),
        _hover={
            "transform": "translateY(-3px)",
            "box_shadow": COLORS["shadow_medium"],
        },
        flex="1",
        min_width="45%",
    )


def setup_page() -> rx.Component:
    """Render the full onboarding setup page."""
    return rx.box(
        rx.vstack(
            # ---- Branding ----
            rx.vstack(
                rx.box(
                    rx.icon(tag="star", size=32, color=COLORS["text_on_primary"]),
                    width="64px",
                    height="64px",
                    border_radius="50%",
                    background_color=COLORS["primary"],
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    box_shadow=COLORS["shadow_medium"],
                ),
                rx.text(
                    "Welcome to Buddy",
                    font_size="26px",
                    font_weight="800",
                    color=COLORS["text_primary"],
                ),
                rx.text(
                    "Let's set up your personal experience",
                    font_size="15px",
                    color=COLORS["text_secondary"],
                ),
                align_items="center",
                gap="10px",
                padding_top="40px",
                padding_bottom="10px",
            ),

            # ==============================
            # CARD: All three steps
            # ==============================
            rx.box(
                rx.vstack(

                    # ----- STEP 1: Name -----
                    rx.vstack(
                        _section_label("Step 1 — Your Name"),
                        rx.text(
                            "What should I call you?",
                            font_size="18px",
                            font_weight="700",
                            color=COLORS["text_primary"],
                        ),
                        rx.input(
                            placeholder="e.g. Alex, Jamie, Chisom…",
                            value=UserState.form_name,
                            on_change=UserState.set_form_name,
                            font_size="16px",
                            height="52px",
                            padding_left="18px",
                            padding_right="18px",
                            border_radius="14px",
                            border=f"2px solid {COLORS['border']}",
                            background_color=COLORS["background_input"],
                            color=COLORS["text_primary"],
                            width="100%",
                            _focus={
                                "border_color": COLORS["primary"],
                                "outline": "none",
                                "box_shadow": f"0 0 0 3px {COLORS['primary_light']}",
                            },
                            _placeholder={"color": COLORS["text_muted"]},
                        ),
                        # Error message
                        rx.cond(
                            UserState.name_error != "",
                            rx.flex(
                                rx.icon(tag="triangle-alert", size=14, color="#E53935"),
                                rx.text(
                                    UserState.name_error,
                                    font_size="13px",
                                    color="#E53935",
                                ),
                                gap="6px",
                                align_items="center",
                            ),
                            rx.fragment(),
                        ),
                        align_items="flex-start",
                        gap="10px",
                        width="100%",
                    ),

                    rx.divider(border_color=COLORS["border"], margin_y="4px"),

                    # ----- STEP 2: Location -----
                    rx.vstack(
                        _section_label("Step 2 — Your City"),
                        rx.text(
                            "Where are you based?",
                            font_size="18px",
                            font_weight="700",
                            color=COLORS["text_primary"],
                        ),
                        rx.text(
                            "Pick your city — we'll use it for live weather updates.",
                            font_size="13px",
                            color=COLORS["text_secondary"],
                        ),
                        rx.select(
                            CITY_NAMES,
                            value=UserState.form_location,
                            on_change=UserState.set_form_location,
                            placeholder="Select your city…",
                            width="100%",
                            color=COLORS["text_primary"],
                            background_color=COLORS["background_input"],
                            border_radius="14px",
                            border=f"2px solid {COLORS['border']}",
                            padding="4px 8px",
                            _focus={
                                "border_color": COLORS["primary"],
                                "outline": "none",
                            },
                        ),
                        align_items="flex-start",
                        gap="10px",
                        width="100%",
                    ),

                    rx.divider(border_color=COLORS["border"], margin_y="4px"),

                    # ----- STEP 3: Assistant -----
                    rx.vstack(
                        _section_label("Step 3 — Your Assistant"),
                        rx.text(
                            "Choose your companion",
                            font_size="18px",
                            font_weight="700",
                            color=COLORS["text_primary"],
                        ),
                        rx.text(
                            "Each has a unique personality — pick who fits you best.",
                            font_size="13px",
                            color=COLORS["text_secondary"],
                        ),
                        # 5 cards in a wrapping flex row
                        rx.flex(
                            *[_assistant_card(a) for a in ASSISTANTS],
                            gap="8px",
                            width="100%",
                            flex_wrap="wrap",
                        ),
                        align_items="flex-start",
                        gap="12px",
                        width="100%",
                    ),

                    rx.divider(border_color=COLORS["border"], margin_y="4px"),

                    # ----- CTA Button -----
                    rx.box(
                        rx.text(
                            "Let's Go! 🚀",
                            font_size="17px",
                            font_weight="700",
                            color=COLORS["text_on_primary"],
                        ),
                        width="100%",
                        padding_top="16px",
                        padding_bottom="16px",
                        background_color=COLORS["primary"],
                        border_radius="16px",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        cursor="pointer",
                        transition="all 0.2s ease",
                        box_shadow=COLORS["shadow_medium"],
                        on_click=UserState.complete_setup,
                        _hover={
                            "background_color": COLORS["primary_hover"],
                            "transform": "scale(1.02)",
                            "box_shadow": COLORS["shadow_hover"],
                        },
                    ),

                    align_items="stretch",
                    gap="20px",
                    width="100%",
                ),

                # Card styling
                background="rgba(255, 255, 255, 0.90)",
                backdrop_filter="blur(20px)",
                border_radius="24px",
                border=f"1px solid {COLORS['border_glass']}",
                box_shadow=COLORS["shadow_medium"],
                padding="28px 24px",
                width="100%",
            ),

            rx.box(height="40px"),

            # ---- Layout ----
            width="100%",
            max_width="430px",
            padding_left="20px",
            padding_right="20px",
            padding_top="0px",
            gap="16px",
            align_items="stretch",
            animation="slide_up 0.5s ease-out",
        ),

        # ---- Page Background ----
        style=PAGE_BACKGROUND_STYLE,
        display="flex",
        flex_direction="column",
        align_items="center",
        overflow_y="auto",
        min_height="100vh",
    )
