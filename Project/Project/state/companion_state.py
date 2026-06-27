"""
companion_state.py — State for the AI companion character system.

This state manages which character is displayed and their current mood.
Characters are 2D illustrated PNGs that appear beside the AI's text
throughout the app. Each character has multiple mood variants.

HOW TO ADD A NEW CHARACTER:
    1. Add their mood images to the assets/ folder
       (e.g. assets/luna_default.png, assets/luna_happy.png)
    2. Add an entry to CHARACTER_IMAGES below
    3. The character will be available for selection

HOW TO ADD A NEW MOOD TO AN EXISTING CHARACTER:
    1. Add the mood image to assets/
    2. Add the mood key to that character's dict in CHARACTER_IMAGES
"""

import reflex as rx


# =============================================================================
# CHARACTER IMAGE REGISTRY
# =============================================================================
# Maps each character name to a dictionary of mood -> image path.
# Image paths are relative to the assets/ folder.
#
# Right now we only have one sample image, so all moods point to it.
# When you create actual mood variants, just update the paths here.

CHARACTER_IMAGES: dict[str, dict[str, str]] = {
    "buddy": {
        "default": "/magnific_vuGFDpZa47.png",
        "happy": "/magnific_vuGFDpZa47.png",
        "worried": "/magnific_vuGFDpZa47.png",
        "surprised": "/magnific_vuGFDpZa47.png",
        "calm": "/magnific_vuGFDpZa47.png",
        "thinking": "/magnific_vuGFDpZa47.png",
    },
    # ---- Add more characters here when ready ----
    # "luna": {
    #     "default": "/characters/luna_default.png",
    #     "happy": "/characters/luna_happy.png",
    #     "worried": "/characters/luna_worried.png",
    #     "surprised": "/characters/luna_surprised.png",
    # },
    # "rex": {
    #     "default": "/characters/rex_default.png",
    #     ...
    # },
}


class CompanionState(rx.State):
    """
    Manages the AI companion's appearance and suggestions.

    The companion is a 2D illustrated character that appears
    throughout the app — in suggestion cards, chat messages,
    weather pages, etc. The character's image changes based
    on their mood, and which character is selected.

    Attributes:
        current_character: The name of the active character (e.g. "buddy").
        current_mood: The character's current emotion (e.g. "happy").
        suggestion_text: What the companion is currently suggesting.
        suggestion_label: The label above the suggestion (e.g. "BUDDY SUGGESTS").
        is_suggestion_visible: Whether the suggestion card is shown.
    """

    # ---- Character Selection ----
    current_character: str = "buddy"
    current_mood: str = "default"

    # ---- Suggestion Content ----
    suggestion_text: str = (
        "It might rain later. Should we move your "
        "outdoor run to 10 AM?"
    )
    suggestion_label: str = "BUDDY SUGGESTS"
    is_suggestion_visible: bool = True

    # ---- Computed Properties ----

    @rx.var
    def character_image(self) -> str:
        """
        Returns the image path for the current character + mood.
        Falls back to the default mood if the requested mood is missing.
        Falls back to the 'buddy' character if the character is missing.
        """
        # Step 1: Get the mood dictionary for this character
        if self.current_character in CHARACTER_IMAGES:
            character_moods = CHARACTER_IMAGES[self.current_character]
        else:
            character_moods = CHARACTER_IMAGES["buddy"]

        # Step 2: Get the image for the current mood
        if self.current_mood in character_moods:
            image_path = character_moods[self.current_mood]
        else:
            image_path = character_moods["default"]

        return image_path

    @rx.var
    def character_name(self) -> str:
        """Returns a display-friendly name for the current character."""
        return self.current_character.capitalize()

    # ---- Event Handlers ----

    @rx.event
    def set_character(self, character_name: str):
        """Switch to a different companion character."""
        self.current_character = character_name
        # Reset mood to default when switching characters
        self.current_mood = "default"

    @rx.event
    def set_mood(self, mood: str):
        """Change the companion's current mood/expression."""
        self.current_mood = mood

    @rx.event
    def dismiss_suggestion(self):
        """User chose to ignore the suggestion — hide the card."""
        self.is_suggestion_visible = False

    @rx.event
    def accept_suggestion(self):
        """User accepted the suggestion — hide card and show happy mood."""
        self.is_suggestion_visible = False
        self.current_mood = "happy"

    @rx.event
    def show_new_suggestion(self, text: str):
        """Display a new suggestion from the companion."""
        self.suggestion_text = text
        self.is_suggestion_visible = True
        self.current_mood = "thinking"
