"""
buddy_avatar.py — Reusable AI companion character image.

Displays the 2D character at different sizes throughout the app.
The image shown comes from CompanionState, which determines the
character and mood. This makes it easy to swap characters or
moods from anywhere in the app.

Usage:
    buddy_avatar(size="small")    # 40px — chat bubbles, inline
    buddy_avatar(size="medium")   # 80px — suggestion cards, sidebar
    buddy_avatar(size="large")    # 160px — chat header, full display
    buddy_avatar(size="peek")     # 100px — peeking from corners
"""

import reflex as rx
from Project.state.user_state import UserState


# Size presets: maps size name to (width, height) in pixels
AVATAR_SIZES = {
    "small": ("40px", "40px"),
    "medium": ("80px", "100px"),
    "large": ("140px", "180px"),
    "peek": ("100px", "130px"),
    "hero": ("160px", "200px"),
}


def buddy_avatar(
    size: str = "medium",
    enable_float: bool = False,
) -> rx.Component:
    """
    Render the AI companion's character image.

    The image automatically updates when CompanionState changes
    (different character selected or mood changes).

    Args:
        size: One of "small", "medium", "large", "peek", "hero".
              Controls the dimensions of the image container.
        enable_float: If True, the character gently bobs up and down
                      using the buddy_float CSS animation.
    """
    # Look up the width and height for the requested size
    if size in AVATAR_SIZES:
        width = AVATAR_SIZES[size][0]
        height = AVATAR_SIZES[size][1]
    else:
        # Default to medium if an unknown size is passed
        width = AVATAR_SIZES["medium"][0]
        height = AVATAR_SIZES["medium"][1]

    # Build the animation string (empty if float is disabled)
    if enable_float:
        animation_value = "buddy_float 3s ease-in-out infinite"
    else:
        animation_value = "none"

    return rx.box(
        rx.image(
            src=UserState.assistant_image,
            alt="AI Companion Character",
            width="100%",
            height="100%",
            object_fit="contain",
        ),
        width=width,
        height=height,
        flex_shrink="0",
        animation=animation_value,
    )
