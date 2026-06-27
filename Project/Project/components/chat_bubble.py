"""
chat_bubble.py — A single chat message bubble.

User messages appear right-aligned with a dark brown background.
Buddy messages appear left-aligned with the character image
beside the text (half-body, not in a circle).

Usage:
    # Inside rx.foreach:
    def render_message(msg):
        return chat_bubble(msg)
"""

import reflex as rx
from Project.theme import COLORS
from Project.components.buddy_avatar import buddy_avatar


def chat_bubble(message: dict) -> rx.Component:
    """
    Render a single chat message bubble.

    Uses rx.cond to check if the sender is "user" or "buddy"
    and renders the appropriate layout.

    Reads from the message dict:
        message["sender"] — "user" or "buddy"
        message["text"]   — The message content
        message["time"]   — Timestamp string

    Args:
        message: A dict var from rx.foreach.
    """
    return rx.cond(
        message["sender"] == "user",
        # ============================================
        # USER MESSAGE — right-aligned, dark background
        # ============================================
        rx.flex(
            rx.box(
                rx.text(
                    message["text"],
                    font_size="14px",
                    color=COLORS["chat_user_text"],
                    line_height="1.5",
                ),
                background_color=COLORS["chat_user_bg"],
                padding="12px 16px",
                border_radius="18px 18px 4px 18px",
                max_width="75%",
            ),
            justify="end",
            width="100%",
            padding_top="4px",
            padding_bottom="4px",
        ),

        # ============================================
        # BUDDY MESSAGE — left-aligned with character image
        # ============================================
        rx.flex(
            # Character image (small, beside the text)
            buddy_avatar(size="small"),

            # Message bubble
            rx.box(
                rx.text(
                    message["text"],
                    font_size="14px",
                    color=COLORS["chat_buddy_text"],
                    line_height="1.5",
                ),
                background_color=COLORS["chat_buddy_bg"],
                backdrop_filter="blur(10px)",
                padding="12px 16px",
                border_radius="18px 18px 18px 4px",
                max_width="70%",
            ),

            align_items="flex-end",
            gap="8px",
            justify="start",
            width="100%",
            padding_top="4px",
            padding_bottom="4px",
        ),
    )
