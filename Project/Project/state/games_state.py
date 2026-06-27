"""
games_state.py — State for the mini-games section.

Manages game card data, the user's streak, and the
weekly leaderboard. Games include Daily Quiz,
Memory Match, and Mood Booster.
"""

import reflex as rx


class GamesState(rx.State):
    """
    Manages all game-related data.

    Attributes:
        streak_days: How many consecutive days the user has played.
        games: List of available games with their details.
        leaderboard: Weekly leaderboard entries.
    """

    # ---- Streak ----
    streak_days: int = 5

    # ---- Available Games ----
    # Each game is a dict with display information.
    games: list[dict[str, str]] = [
        {
            "id": "quiz",
            "title": "Daily Quiz",
            "description": "Test your knowledge with 5 trivia questions.",
            "duration": "3 mins",
            "icon": "brain",
            "type": "quiz",
        },
        {
            "id": "memory",
            "title": "Memory Match",
            "description": "Find the pairs and train your recall.",
            "duration": "5 mins",
            "icon": "grid-3x3",
            "type": "puzzle",
        },
        {
            "id": "tictactoe",
            "title": "Tic-Tac-Toe",
            "description": "A classic game of X and O against me.",
            "duration": "2 mins",
            "icon": "hash",
            "type": "puzzle",
        },
    ]

    # ---- Weekly Leaderboard ----
    leaderboard: list[dict[str, str]] = [
        {
            "rank": "1",
            "name": "Alex L.",
            "initials": "AL",
            "points": "2,450 pts",
            "is_user": "false",
        },
        {
            "rank": "2",
            "name": "You",
            "initials": "MA",
            "points": "2,100 pts",
            "is_user": "true",
        },
        {
            "rank": "3",
            "name": "Sam K.",
            "initials": "SK",
            "points": "1,890 pts",
            "is_user": "false",
        },
    ]

    @rx.var
    def streak_text(self) -> str:
        """Display-friendly streak text."""
        return f"{self.streak_days} Day Streak!"
