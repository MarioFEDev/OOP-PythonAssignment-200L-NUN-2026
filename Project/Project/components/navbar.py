"""
navbar.py — Bottom navigation bar component.

The navbar appears at the bottom of every page. It has 4 tabs:
Home, Planner, Weather, and Chat. The active tab is highlighted
with an orange pill background.

Usage:
    navbar(active_page="home")
    navbar(active_page="planner")
"""

import reflex as rx
from Project.theme import COLORS, NAV_ITEM_STYLE


def navbar(active_page: str = "home") -> rx.Component:
    """
    Render the fixed bottom navigation bar.

    Args:
        active_page: Which tab to highlight as active.
                     One of: "home", "planner", "weather", "chat"
    """
    return rx.box(
        rx.flex(
            # ---- Home Tab ----
            _nav_tab(
                icon_name="home",
                label="Home",
                href="/",
                is_active=(active_page == "home"),
            ),
            # ---- Planner Tab ----
            _nav_tab(
                icon_name="calendar",
                label="Planner",
                href="/planner",
                is_active=(active_page == "planner"),
            ),
            # ---- Weather Tab ----
            _nav_tab(
                icon_name="cloud",
                label="Weather",
                href="/weather",
                is_active=(active_page == "weather"),
            ),
            # ---- Chat Tab ----
            _nav_tab(
                icon_name="sparkles",
                label="Chat",
                href="/chat",
                is_active=(active_page == "chat"),
            ),
            justify="between",
            align="center",
            width="100%",
            padding_top="8px",
            padding_bottom="8px",
        ),
        # ---- Navbar Container Styling ----
        position="fixed",
        bottom="0",
        left="50%",
        transform="translateX(-50%)",
        width="100%",
        max_width="430px",
        background=COLORS["background_nav"],
        backdrop_filter="blur(20px)",
        border_top=f"1px solid {COLORS['border']}",
        padding_left="8px",
        padding_right="8px",
        padding_bottom="12px",
        z_index="50",
    )


def _nav_tab(
    icon_name: str,
    label: str,
    href: str,
    is_active: bool,
) -> rx.Component:
    """
    Render a single navigation tab (icon + label).

    This is a private helper function (starts with underscore)
    used only by the navbar() function above.

    Args:
        icon_name: The Lucide icon name (e.g. "home", "calendar")
        label: The text label below the icon (e.g. "Home")
        href: The URL path to navigate to (e.g. "/planner")
        is_active: Whether this tab is currently active
    """
    # Determine colors based on active state
    if is_active:
        icon_color = COLORS["primary"]
        text_color = COLORS["primary"]
        bg_color = COLORS["nav_active_bg"]
    else:
        icon_color = COLORS["nav_inactive"]
        text_color = COLORS["nav_inactive"]
        bg_color = "transparent"

    return rx.link(
        rx.box(
            rx.icon(
                tag=icon_name,
                size=20,
                color=icon_color,
            ),
            rx.text(
                label,
                font_size="11px",
                font_weight="600",
                color=text_color,
            ),
            display="flex",
            flex_direction="column",
            align_items="center",
            gap="4px",
            padding_left="16px",
            padding_right="16px",
            padding_top="8px",
            padding_bottom="8px",
            border_radius="16px",
            background_color=bg_color,
            transition="all 0.3s ease",
            _hover={
                "background_color": COLORS["primary_light"],
            },
        ),
        href=href,
        text_decoration="none",
    )
