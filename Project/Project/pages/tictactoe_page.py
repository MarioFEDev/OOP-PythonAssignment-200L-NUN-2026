"""
tictactoe_page.py — The Tic-Tac-Toe game page.
"""

import reflex as rx
from Project.theme import COLORS, PAGE_BACKGROUND_STYLE, GLASS_CARD_STYLE
from Project.state.tictactoe_state import TicTacToeState
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

def cell_component(index: int) -> rx.Component:
    """Render a single tic-tac-toe cell."""
    val = TicTacToeState.board[index]
    return rx.flex(
        rx.cond(
            val != "",
            rx.text(
                val, 
                font_size="70px", 
                font_weight="800",
                line_height="1",
                text_align="center",
                color=rx.cond(val == "X", COLORS["primary"], COLORS["text_primary"])
            ),
            rx.text("")
        ),
        width="100%",
        height="100px",
        display="flex",
        align_items="center",
        justify_content="center",
        background_color=COLORS["background_card"],
        border_radius="12px",
        border=f"2px solid {COLORS['primary_light']}",
        cursor="pointer",
        _hover={"background_color": COLORS["border"]},
        on_click=TicTacToeState.make_move(index),
        transition="all 0.2s ease",
    )

def tictactoe_page() -> rx.Component:
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
                rx.text("Tic-Tac-Toe", font_size="20px", font_weight="700"),
                rx.box(width="24px"), # Spacer
                justify="between",
                align_items="center",
                width="100%",
                padding_bottom="10px",
            ),
            
            # Companion Message
            game_companion_ui(TicTacToeState.ai_message),
            
            # Main Game Area
            rx.vstack(
                rx.grid(
                    rx.foreach(
                        rx.Var.range(9),
                        cell_component
                    ),
                    columns="3",
                    spacing="3",
                    width="100%",
                    max_width="300px",
                ),
                rx.cond(
                    TicTacToeState.game_over,
                    rx.button(
                        "Play Again",
                        on_click=TicTacToeState.start_game,
                        background_color=COLORS["primary"],
                        color="white",
                        margin_top="30px",
                        width="100%",
                        max_width="300px",
                    )
                ),
                width="100%",
                align_items="center",
                style=GLASS_CARD_STYLE,
                padding="30px 20px",
            ),
            
            width="100%",
            max_width="430px",
            padding="20px",
            gap="16px",
        ),
        
        navbar(active_page="games"),
        
        style=PAGE_BACKGROUND_STYLE,
        display="flex",
        flex_direction="column",
        align_items="center",
        min_height="100vh",
    )
