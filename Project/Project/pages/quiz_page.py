"""
quiz_page.py — The Daily Quiz game page.
"""

import reflex as rx
from Project.theme import COLORS, PAGE_BACKGROUND_STYLE, GLASS_CARD_STYLE
from Project.state.quiz_state import QuizState
from Project.state.user_state import UserState
from Project.components.navbar import navbar

def game_companion_ui() -> rx.Component:
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
                QuizState.ai_message,
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

def quiz_page() -> rx.Component:
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
                rx.text("Daily Quiz", font_size="20px", font_weight="700"),
                rx.box(width="24px"), # Spacer
                justify="between",
                align_items="center",
                width="100%",
                padding_bottom="20px",
            ),
            
            # Companion Message
            game_companion_ui(),
            
            # Main Game Area
            rx.cond(
                QuizState.is_loading,
                rx.center(rx.spinner(color=COLORS["primary"]), width="100%", height="200px"),
                rx.cond(
                    QuizState.questions.length() == 0,
                    rx.center(
                        rx.button(
                            "Start Quiz", 
                            on_click=QuizState.start_game,
                            background_color=COLORS["primary"],
                            color="white",
                        ),
                        width="100%",
                        height="200px",
                    ),
                    rx.cond(
                        QuizState.game_over,
                        rx.vstack(
                            rx.text(f"Final Score: {QuizState.score}", font_size="24px", font_weight="bold", color=COLORS["primary"]),
                            rx.button(
                                "Play Again", 
                                on_click=QuizState.start_game,
                                background_color=COLORS["primary"],
                                color="white",
                                margin_top="20px",
                            ),
                            align_items="center",
                            width="100%",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    f"Question {QuizState.current_index + 1} of {QuizState.questions.length()}", 
                                    font_size="12px", 
                                    color=COLORS["text_secondary"]
                                ),
                                rx.text(
                                    QuizState.current_question_text, 
                                    font_size="18px", 
                                    font_weight="600",
                                    margin_bottom="20px"
                                ),
                                rx.foreach(
                                    QuizState.options,
                                    lambda opt: rx.button(
                                        opt,
                                        width="100%",
                                        padding="16px",
                                        margin_bottom="10px",
                                        background_color=COLORS["background"],
                                        color=COLORS["text_primary"],
                                        border=f"1px solid {COLORS['border']}",
                                        _hover={"background_color": COLORS["primary_light"]},
                                        on_click=QuizState.submit_answer(opt),
                                    )
                                ),
                                width="100%",
                                style=GLASS_CARD_STYLE,
                            ),
                            width="100%",
                        )
                    )
                )
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
