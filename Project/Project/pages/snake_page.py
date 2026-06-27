"""
snake_page.py — The Snake game page.
"""

import reflex as rx
from Project.theme import COLORS, PAGE_BACKGROUND_STYLE, GLASS_CARD_STYLE
from Project.state.snake_state import SnakeState, GRID_SIZE
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

def render_grid() -> rx.Component:
    cells = []
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            # Check if this cell is snake or food
            # In Reflex, checking list inclusion in the frontend is tricky if it's dynamic
            # A simple approach: we use CSS grids, but since the grid is dynamic, we'll map over it.
            pass
    # Due to Reflex's frontend compilation, generating a 15x15 grid element-by-element using Var logic is complex.
    # Instead, we will generate the grid cells dynamically using rx.foreach.
    # We will pass a flat list of 225 ints (0 to 224) and check coords.
    
    # Wait, Reflex can do foreach on range.
    return rx.grid(
        rx.foreach(
            rx.Var.range(GRID_SIZE * GRID_SIZE),
            lambda i: rx.box(
                width="100%",
                padding_top="100%", # aspect ratio 1:1
                background_color=rx.cond(
                    SnakeState.snake.contains(i),
                    COLORS["primary"],
                    rx.cond(
                        SnakeState.food == i,
                        COLORS["badge_health"],
                        COLORS["background_card"]
                    )
                ),
                border=f"1px solid {COLORS['border']}",
                border_radius="2px",
            )
        ),
        columns=f"{GRID_SIZE}",
        width="100%",
        max_width="350px",
        background_color=COLORS["border"],
        border=f"2px solid {COLORS['primary_dark']}",
        border_radius="4px",
    )

def snake_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Header
            rx.flex(
                rx.icon(
                    tag="arrow-left",
                    color=COLORS["text_secondary"],
                    cursor="pointer",
                    on_click=[SnakeState.stop_game, rx.redirect("/games")],
                ),
                rx.text("Snake", font_size="20px", font_weight="700"),
                rx.box(width="24px"), # Spacer
                justify="between",
                align_items="center",
                width="100%",
                padding_bottom="10px",
            ),
            
            # Companion Message
            game_companion_ui(SnakeState.ai_message),
            
            # Stats
            rx.flex(
                rx.text(f"Score: {SnakeState.score}", font_weight="700", font_size="18px", color=COLORS["primary"]),
                justify="center",
                width="100%",
                margin_bottom="10px",
            ),
            
            # Game Board
            rx.center(
                rx.cond(
                    SnakeState.is_playing | SnakeState.game_over,
                    render_grid(),
                    rx.button(
                        "Start Game",
                        on_click=SnakeState.start_game,
                        background_color=COLORS["primary"],
                        color="white",
                        width="100%",
                        max_width="200px",
                    )
                ),
                width="100%",
            ),
            
            # Controls
            rx.cond(
                SnakeState.is_playing | SnakeState.game_over,
                rx.vstack(
                    rx.cond(
                        SnakeState.game_over,
                        rx.button("Play Again", on_click=SnakeState.start_game, background_color=COLORS["primary"], color="white", margin_top="10px"),
                        rx.box()
                    ),
                    rx.center(
                        rx.button(rx.icon(tag="arrow-up"), on_click=lambda: SnakeState.change_direction("UP"), width="60px", height="60px", background_color=COLORS["primary_light"])
                    ),
                    rx.flex(
                        rx.button(rx.icon(tag="arrow-left"), on_click=lambda: SnakeState.change_direction("LEFT"), width="60px", height="60px", background_color=COLORS["primary_light"]),
                        rx.box(width="20px"),
                        rx.button(rx.icon(tag="arrow-right"), on_click=lambda: SnakeState.change_direction("RIGHT"), width="60px", height="60px", background_color=COLORS["primary_light"]),
                        justify="center",
                    ),
                    rx.center(
                        rx.button(rx.icon(tag="arrow-down"), on_click=lambda: SnakeState.change_direction("DOWN"), width="60px", height="60px", background_color=COLORS["primary_light"])
                    ),
                    width="100%",
                    margin_top="20px",
                )
            ),
            
            width="100%",
            max_width="430px",
            padding="20px",
            gap="10px",
        ),
        
        navbar(active_page="games"),
        
        style=PAGE_BACKGROUND_STYLE,
        display="flex",
        flex_direction="column",
        align_items="center",
        min_height="100vh",
        
        on_key_down=SnakeState.handle_key,
        tab_index=0,
        id="snake-container",
        
        # Add keyboard listener hook and auto focus
        on_mount=rx.call_script("""
            var container = document.getElementById('snake-container');
            if (container) {
                container.focus();
            }
            document.addEventListener('keydown', function(e) {
                if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) {
                    e.preventDefault(); // Prevent page scrolling
                    // Trigger keydown on the container so reflex catches it
                    if (document.activeElement !== container) {
                        container.focus();
                    }
                }
            });
        """)
    )
