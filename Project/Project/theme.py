"""
theme.py — Global color tokens and reusable style dictionaries.

All colors used throughout the app are defined here.
Import COLORS and style dicts in any component or page file.
Never use raw hex color values in component files — always
reference COLORS["token_name"] instead.

Example usage in a component file:
    from Project.theme import COLORS, GLASS_CARD_STYLE, CARD_HOVER

    def my_component():
        return rx.box(
            rx.text("Hello", color=COLORS["text_primary"]),
            style=GLASS_CARD_STYLE,
            _hover=CARD_HOVER,
        )
"""


# =============================================================================
# COLOR TOKENS
# =============================================================================
# These are the foundational colors for the entire app.
# To change the app's look, just modify these values here and
# the whole app will update automatically.

COLORS = {
    # ---- Primary Brand Colors ----
    "primary": "#C75B12",              # Burnt orange — buttons, active tabs, accents
    "primary_dark": "#8B4513",         # Saddle brown — headings, strong emphasis
    "primary_light": "#FFE0C0",        # Soft peach — hover backgrounds, glows
    "primary_hover": "#A84E0F",        # Darker orange — button hover state

    # ---- Background Colors ----
    "background": "#FFF8F0",           # Warm cream — main page background
    "background_card": "rgba(255, 255, 255, 0.80)",   # Solid card backgrounds
    "background_glass": "rgba(255, 255, 255, 0.55)",   # Glassmorphism panels
    "background_input": "rgba(255, 255, 255, 0.90)",   # Input field backgrounds
    "background_nav": "rgba(255, 248, 240, 0.95)",     # Bottom navigation bar

    # ---- Text Colors ----
    "text_primary": "#2D1B0E",         # Dark brown — main body text
    "text_secondary": "#7A6555",       # Medium brown — subtitles, descriptions
    "text_muted": "#A89585",           # Light brown — timestamps, placeholders
    "text_on_primary": "#FFFFFF",      # White — text on primary-colored backgrounds
    "text_accent": "#C75B12",          # Orange — links, action text, highlights

    # ---- Border Colors ----
    "border": "rgba(200, 170, 140, 0.25)",       # Soft warm border
    "border_glass": "rgba(255, 255, 255, 0.35)",  # Glass panel borders

    # ---- Box Shadows ----
    "shadow_soft": "0 4px 24px rgba(139, 69, 19, 0.06)",
    "shadow_medium": "0 8px 32px rgba(139, 69, 19, 0.10)",
    "shadow_hover": "0 12px 40px rgba(139, 69, 19, 0.15)",

    # ---- Category Badge Colors ----
    "badge_health": "#4CAF50",
    "badge_health_bg": "rgba(76, 175, 80, 0.12)",
    "badge_work": "#E8860C",
    "badge_work_bg": "rgba(232, 134, 12, 0.12)",
    "badge_errands": "#D4A017",
    "badge_errands_bg": "rgba(212, 160, 23, 0.12)",
    "badge_moved": "#E85D3A",
    "badge_moved_bg": "rgba(232, 93, 58, 0.12)",

    # ---- Chat Colors ----
    "chat_user_bg": "#8B4513",
    "chat_user_text": "#FFFFFF",
    "chat_buddy_bg": "rgba(255, 240, 224, 0.8)",
    "chat_buddy_text": "#2D1B0E",

    # ---- Navigation Colors ----
    "nav_active_bg": "rgba(199, 91, 18, 0.12)",
    "nav_inactive": "#A89585",

    # ---- Gradient Definitions ----
    "gradient_warm_start": "#FFF8F0",
    "gradient_warm_mid": "#FFE8D6",
    "gradient_warm_end": "#FFD4B8",
    "gradient_suggestion": (
        "linear-gradient(135deg, #FFF0E0 0%, #FFE0C0 50%, #FFD4B8 100%)"
    ),

    # ---- Miscellaneous ----
    "white": "#FFFFFF",
    "overlay": "rgba(0, 0, 0, 0.3)",
    "streak_bg": "#FFF3E0",
    "streak_text": "#E8860C",
}


# =============================================================================
# REUSABLE STYLE DICTIONARIES
# =============================================================================
# These contain standard CSS properties only.
# Hover effects are defined as separate dicts and applied via _hover= prop.
# This keeps things explicit and beginner-friendly.
#
# Usage:
#     rx.box(
#         "content",
#         style=GLASS_CARD_STYLE,     # Base styles
#         _hover=CARD_HOVER,          # Hover effect
#     )


# ---- Glassmorphism Card (frosted glass look) ----
GLASS_CARD_STYLE = {
    "background": COLORS["background_glass"],
    "backdrop_filter": "blur(20px)",
    "border_radius": "20px",
    "border": f"1px solid {COLORS['border_glass']}",
    "box_shadow": COLORS["shadow_soft"],
    "padding": "20px",
    "transition": "all 0.3s ease",
}

# ---- Solid Card (opaque white) ----
SOLID_CARD_STYLE = {
    "background": COLORS["background_card"],
    "border_radius": "16px",
    "border": f"1px solid {COLORS['border']}",
    "box_shadow": COLORS["shadow_soft"],
    "padding": "16px",
    "transition": "all 0.3s ease",
}

# ---- Suggestion Card (warm gradient) ----
SUGGESTION_CARD_STYLE = {
    "background": COLORS["gradient_suggestion"],
    "backdrop_filter": "blur(16px)",
    "border_radius": "20px",
    "border": f"1px solid {COLORS['border_glass']}",
    "box_shadow": COLORS["shadow_soft"],
    "padding": "20px",
    "overflow": "hidden",
    "position": "relative",
    "transition": "all 0.3s ease",
}

# ---- Hover Effects (applied via _hover= prop) ----
CARD_HOVER = {
    "box_shadow": COLORS["shadow_hover"],
    "transform": "translateY(-2px)",
}

SUBTLE_HOVER = {
    "background_color": COLORS["primary_light"],
}

BUTTON_HOVER = {
    "background_color": COLORS["primary_hover"],
    "transform": "scale(1.02)",
}

BUTTON_SECONDARY_HOVER = {
    "background_color": COLORS["primary_light"],
    "color": COLORS["primary_dark"],
}

# ---- Page Background (animated gradient) ----
PAGE_BACKGROUND_STYLE = {
    "background": (
        f"linear-gradient(180deg, "
        f"{COLORS['gradient_warm_start']} 0%, "
        f"{COLORS['gradient_warm_mid']} 50%, "
        f"{COLORS['gradient_warm_start']} 100%)"
    ),
    "background_size": "100% 200%",
    "animation": "gradient_shift 12s ease infinite",
    "min_height": "100vh",
    "width": "100%",
    "position": "relative",
}

# ---- Button Styles ----
BUTTON_PRIMARY_STYLE = {
    "background_color": COLORS["primary"],
    "color": COLORS["text_on_primary"],
    "border_radius": "12px",
    "padding_left": "20px",
    "padding_right": "20px",
    "padding_top": "10px",
    "padding_bottom": "10px",
    "font_weight": "600",
    "font_size": "14px",
    "cursor": "pointer",
    "border": "none",
    "transition": "all 0.2s ease",
}

BUTTON_SECONDARY_STYLE = {
    "background_color": "transparent",
    "color": COLORS["text_secondary"],
    "border_radius": "12px",
    "padding_left": "20px",
    "padding_right": "20px",
    "padding_top": "10px",
    "padding_bottom": "10px",
    "font_weight": "500",
    "font_size": "14px",
    "cursor": "pointer",
    "border": f"1px solid {COLORS['border']}",
    "transition": "all 0.2s ease",
}

# ---- Input Styles ----
INPUT_STYLE = {
    "background": COLORS["background_input"],
    "border": f"1px solid {COLORS['border']}",
    "border_radius": "24px",
    "padding_left": "20px",
    "padding_right": "20px",
    "padding_top": "12px",
    "padding_bottom": "12px",
    "color": COLORS["text_primary"],
    "width": "100%",
    "font_size": "14px",
    "transition": "all 0.2s ease",
}

# ---- Navigation Item ----
NAV_ITEM_STYLE = {
    "display": "flex",
    "flex_direction": "column",
    "align_items": "center",
    "gap": "4px",
    "cursor": "pointer",
    "transition": "all 0.3s ease",
    "padding_left": "16px",
    "padding_right": "16px",
    "padding_top": "8px",
    "padding_bottom": "8px",
    "border_radius": "16px",
    "text_decoration": "none",
}
