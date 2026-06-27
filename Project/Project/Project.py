"""
Project.py — Main application entry point.

This file:
1. Sets up the global theme (colors, fonts, appearance)
2. Imports all page definitions
3. Registers each page at its URL route
4. Creates and configures the rx.App instance

Routes:
    /         → Home page
    /setup    → First-launch onboarding (name, city, assistant)
    /planner  → Day planner
    /weather  → Weather dashboard
    /games    → Mini-games section
    /chat     → AI companion chat
"""

import reflex as rx
from Project.theme import COLORS

# ---- Import all page functions ----
from Project.pages.home_page import home_page
from Project.pages.setup_page import setup_page
from Project.pages.planner_page import planner_page
from Project.pages.weather_page import weather_page
from Project.pages.games_page import games_page
from Project.pages.chat_page import chat_page
from Project.pages.quiz_page import quiz_page
from Project.pages.memory_page import memory_page
from Project.pages.tictactoe_page import tictactoe_page

# ---- Import state classes so Reflex registers them ----
from Project.state.app_state import AppState
from Project.state.user_state import UserState
from Project.state.companion_state import CompanionState
from Project.state.planner_state import PlannerState
from Project.state.weather_state import WeatherState
from Project.state.chat_state import ChatState
from Project.state.games_state import GamesState
from Project.state.quiz_state import QuizState
from Project.state.memory_state import MemoryState
from Project.state.tictactoe_state import TicTacToeState


# =============================================================================
# GLOBAL STYLES
# =============================================================================

GLOBAL_STYLE = {
    # ---- Default Font ----
    "font_family": "'Inter', 'Segoe UI', 'Roboto', sans-serif",
    "font_size": "16px",
    "color": COLORS["text_primary"],

    # ---- Global Text Selection Color ----
    "::selection": {
        "background_color": COLORS["primary_light"],
        "color": COLORS["primary_dark"],
    },

    # ---- Default Heading Styles ----
    rx.heading: {
        "color": COLORS["text_primary"],
        "font_weight": "700",
    },

    # ---- Default Text Styles ----
    rx.text: {
        "color": COLORS["text_primary"],
        "line_height": "1.5",
    },

    # ---- Body Background ----
    "body": {
        "background_color": COLORS["background"],
        "margin": "0",
        "padding": "0",
    },
}


# =============================================================================
# APP CONFIGURATION
# =============================================================================

app = rx.App(
    style=GLOBAL_STYLE,
    stylesheets=[
        (
            "https://fonts.googleapis.com/css2?"
            "family=Inter:wght@300;400;500;600;700;800"
            "&display=swap"
        ),
        "/styles.css",
    ],
)


# =============================================================================
# REGISTER PAGES (URL ROUTES)
# =============================================================================

def index():
    return home_page()

app.add_page(
    index,
    route="/",
    title="My AI Companion",
)

app.add_page(
    setup_page,
    route="/setup",
    title="My Companion — Setup",
)

app.add_page(
    planner_page,
    route="/planner",
    title="My Companion — Day Planner",
)

app.add_page(
    weather_page,
    route="/weather",
    title="My Companion — Weather",
)

app.add_page(
    games_page,
    route="/games",
    title="My Companion — Games",
)

app.add_page(
    chat_page,
    route="/chat",
    title="My Companion — Chat",
)

app.add_page(quiz_page, route="/games/quiz", title="My Companion — Quiz")
app.add_page(memory_page, route="/games/memory", title="My Companion — Memory")
app.add_page(tictactoe_page, route="/games/tictactoe", title="My Companion — Tic-Tac-Toe")
