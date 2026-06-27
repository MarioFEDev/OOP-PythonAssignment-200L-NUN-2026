"""
memory_page.py — The Memory Match game page.
"""

import reflex as rx
from Project.theme import COLORS, PAGE_BACKGROUND_STYLE, GLASS_CARD_STYLE
from Project.state.memory_state import MemoryState
from Project.state.user_state import UserState
from Project.components.navbar import navbar

def game_companion_ui(message_var) -> rx.Component:
    """A reusable UI component for the companion's messages in games."""
    return rx.flex(
        rx.image(
            src=UserState.assistant_image,
            width="60px",
            height="60px",
            border_radius="50%",
            border=f"2px solid {COLORS['primary_light']}",
            object_fit="cover",
        ),
        rx.box(
            rx.text(
                UserState.assistant_name,
                font_size="12px",
                font_weight="700",
                color=COLORS["primary"],
                margin_bottom="4px",
            ),
            rx.text(
                message_var,
                font_size="16px",
                color=COLORS["text_primary"],
            ),
            background_color=COLORS["background_card"],
            padding="12px",
            border_radius="12px",
            border=f"1px solid {COLORS['primary_light']}",
            width="100%",
        ),
        gap="12px",
        align_items="center",
        width="100%",
        margin_bottom="20px",
    )

def card_component(card: dict) -> rx.Component:
    """Render a single memory card."""
    is_revealed = card["is_flipped"] | card["is_matched"]
    return rx.box(
        rx.cond(
            is_revealed,
            rx.center(
                rx.text(
                    card["icon"],
                    font_size="40px",
                ),
                width="100%",
                height="80px",
                background_color=rx.cond(card["is_matched"], COLORS["primary"], COLORS["background_card"]),
                border_radius="8px",
                border=f"2px solid {COLORS['primary']}",
                box_shadow="0 4px 6px rgba(0,0,0,0.1)",
                transition="all 0.3s ease",
            ),
            rx.center(
                rx.icon(
                    tag="help-circle",
                    size=30,
                    color=COLORS["text_secondary"],
                    opacity="0.5",
                ),
                width="100%",
                height="80px",
                background_color=COLORS["primary_light"],
                border_radius="8px",
                cursor="pointer",
                _hover={"background_color": COLORS["border"]},
                on_click=MemoryState.flip_card(card["id"]),
                transition="all 0.3s ease",
            )
        )
    )

def memory_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Header
            rx.flex(
                rx.icon(
                    tag="arrow-left",
                    color=COLORS["text_secondary"],
                    cursor="pointer",
                    on_click=rx.redirect("/games"),
                ),
                rx.text("Memory Match", font_size="20px", font_weight="700"),
                rx.box(width="24px"), # Spacer
                justify="between",
                align_items="center",
                width="100%",
                padding_bottom="10px",
            ),
            
            # Companion Message
            game_companion_ui(MemoryState.ai_message),
            
            # Main Game Area
            rx.cond(
                MemoryState.cards.length() == 0,
                rx.center(
                    rx.button(
                        "Start Game", 
                        on_click=MemoryState.start_game,
                        background_color=COLORS["primary"],
                        color="white",
                    ),
                    width="100%",
                    height="200px",
                ),
                rx.vstack(
                    rx.flex(
                        rx.text(f"Moves: {MemoryState.moves}", font_weight="600"),
                        rx.text(f"Matches: {MemoryState.matches}/8", font_weight="600"),
                        justify="between",
                        width="100%",
                        padding_bottom="10px",
                    ),
                    rx.grid(
                        rx.foreach(
                            MemoryState.cards,
                            card_component
                        ),
                        columns="4",
                        spacing="3",
                        width="100%",
                    ),
                    rx.cond(
                        MemoryState.game_over,
                        rx.button(
                            "Play Again",
                            on_click=MemoryState.start_game,
                            background_color=COLORS["primary"],
                            color="white",
                            margin_top="20px",
                            width="100%",
                        )
                    ),
                    width="100%",
                    style=GLASS_CARD_STYLE,
                    padding="20px",
                )
            ),
            
            width="100%",
            max_width="430px",
            padding="20px",
            padding_bottom="120px",
            gap="16px",
        ),
        
        navbar(active_page="games"),
        
        style=PAGE_BACKGROUND_STYLE,
        display="flex",
        flex_direction="column",
        align_items="center",
        min_height="100vh",
    )
