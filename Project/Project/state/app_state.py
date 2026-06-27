"""
app_state.py — Main application state.

Provides a thin wrapper that other components can import.
User profile data lives in UserState (with localStorage persistence).
"""

import reflex as rx


class AppState(rx.State):
    """
    Top-level app state.
    Components use AppState.user_name and AppState.user_avatar
    which are wired directly to UserState vars via the UI layer.
    """

    # ---- Navigation ----
    active_page: str = "home"

    # ---- Event Handlers ----

    @rx.event
    def set_active_page(self, page_name: str):
        """Update which page is currently active (for navbar highlighting)."""
        self.active_page = page_name
