"""
weather_page.py — Full weather dashboard screen.

Displays live weather data from Open-Meteo for Abuja, Nigeria.
Shows current conditions, weather stats (humidity, wind, rain),
feels-like temperature, and a 7-day forecast grid.
The buddy character peeks from the corner of the forecast section.

Route: /weather
On load: WeatherState.fetch_weather()
"""

import reflex as rx
from Project.theme import COLORS, PAGE_BACKGROUND_STYLE, GLASS_CARD_STYLE, CARD_HOVER
from Project.state.app_state import AppState
from Project.state.weather_state import WeatherState
from Project.state.user_state import UserState
from Project.components.navbar import navbar
from Project.components.buddy_avatar import buddy_avatar
from Project.components.weather_detail_card import weather_detail_card
from Project.components.forecast_day import forecast_day


def _loading_spinner() -> rx.Component:
    """Animated loading indicator shown while fetching weather data."""
    return rx.cond(
        WeatherState.is_loading,
        rx.flex(
            rx.icon(
                tag="loader-circle",
                size=16,
                color=COLORS["primary"],
                style={"animation": "spin 1s linear infinite"},
            ),
            rx.text(
                "Updating…",
                font_size="12px",
                color=COLORS["text_muted"],
            ),
            gap="6px",
            align_items="center",
        ),
        rx.cond(
            WeatherState.last_updated != "",
            rx.text(
                "Updated at " + WeatherState.last_updated,
                font_size="12px",
                color=COLORS["text_muted"],
            ),
            rx.fragment(),
        ),
    )


def _error_banner() -> rx.Component:
    """Banner shown when the weather fetch fails."""
    return rx.cond(
        WeatherState.error_message != "",
        rx.flex(
            rx.icon(tag="triangle-alert", size=16, color="#e74c3c"),
            rx.text(
                WeatherState.error_message,
                font_size="13px",
                color="#e74c3c",
                font_weight="500",
            ),
            gap="8px",
            align_items="center",
            padding="10px 14px",
            background="rgba(231, 76, 60, 0.08)",
            border="1px solid rgba(231, 76, 60, 0.25)",
            border_radius="12px",
            width="100%",
        ),
        rx.fragment(),
    )


def weather_page() -> rx.Component:
    """Render the complete weather page with live Open-Meteo data."""
    return rx.box(
        rx.vstack(
            # ==============================
            # SECTION 1: Header
            # ==============================
            rx.flex(
                # Left: App icon
                rx.icon(
                    tag="sun",
                    size=22,
                    color=COLORS["primary"],
                ),
                # Center: App name
                rx.text(
                    UserState.assistant_name,
                    font_size="20px",
                    font_weight="800",
                    color=COLORS["primary_dark"],
                ),
                # Right: User avatar
                rx.box(
                    rx.image(
                        src=UserState.assistant_image,
                        alt="User Avatar",
                        width="100%",
                        height="100%",
                        object_fit="cover",
                        border_radius="50%",
                    ),
                    width="36px",
                    height="36px",
                    border_radius="50%",
                    border=f"2px solid {COLORS['primary_light']}",
                    overflow="hidden",
                    flex_shrink="0",
                ),
                justify="between",
                align_items="center",
                width="100%",
            ),

            # ==============================
            # SECTION 2: City + Refresh Row
            # ==============================
            rx.flex(
                rx.vstack(
                    rx.flex(
                        rx.text(
                            WeatherState.city,
                            font_size="26px",
                            font_weight="800",
                            color=COLORS["text_primary"],
                        ),
                        rx.icon(
                            tag="map-pin",
                            size=18,
                            color=COLORS["primary"],
                        ),
                        gap="6px",
                        align_items="center",
                    ),
                    _loading_spinner(),
                    align_items="flex-start",
                    gap="2px",
                ),
                # Refresh button
                rx.box(
                    rx.icon(
                        tag="refresh-cw",
                        size=18,
                        color=COLORS["text_secondary"],
                    ),
                    width="38px",
                    height="38px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    border_radius="50%",
                    background_color=COLORS["background_card"],
                    border=f"1px solid {COLORS['border']}",
                    cursor="pointer",
                    transition="all 0.2s ease",
                    _hover={
                        "background_color": COLORS["primary_light"],
                        "transform": "rotate(180deg)",
                    },
                    on_click=WeatherState.fetch_weather,
                ),
                justify="between",
                align_items="center",
                width="100%",
            ),

            # Error banner (shown only on failure)
            _error_banner(),

            # ==============================
            # SECTION 3: Current Weather Card
            # ==============================
            rx.box(
                rx.vstack(
                    # Weather icon
                    rx.icon(
                        tag=WeatherState.current_icon,
                        size=64,
                        color=COLORS["primary"],
                    ),
                    # Temperature
                    rx.heading(
                        WeatherState.current_temp.to(str) + "°C",
                        font_size="64px",
                        font_weight="800",
                        color=COLORS["text_primary"],
                        line_height="1",
                    ),
                    # Condition text
                    rx.box(
                        rx.text(
                            WeatherState.current_condition,
                            font_size="14px",
                            font_weight="500",
                            color=COLORS["text_secondary"],
                        ),
                        padding_left="16px",
                        padding_right="16px",
                        padding_top="6px",
                        padding_bottom="6px",
                        background_color=COLORS["background_card"],
                        border_radius="20px",
                        border=f"1px solid {COLORS['border']}",
                    ),
                    # Feels like
                    rx.text(
                        "Feels like " + WeatherState.feels_like.to(str) + "°C",
                        font_size="13px",
                        color=COLORS["text_muted"],
                        font_weight="400",
                    ),
                    align_items="center",
                    gap="10px",
                    width="100%",
                ),
                style=GLASS_CARD_STYLE,
                _hover=CARD_HOVER,
                background=(
                    f"linear-gradient(180deg, "
                    f"{COLORS['background_card']} 0%, "
                    f"{COLORS['gradient_warm_mid']} 100%)"
                ),
                width="100%",
                padding_top="32px",
                padding_bottom="32px",
            ),

            # ==============================
            # SECTION 4: Weather Stats Row
            # ==============================
            rx.flex(
                weather_detail_card(
                    icon_name="droplets",
                    value=WeatherState.humidity,
                    label="Humidity",
                ),
                weather_detail_card(
                    icon_name="wind",
                    value=WeatherState.wind_speed,
                    label="Wind",
                ),
                weather_detail_card(
                    icon_name="cloud-rain",
                    value=WeatherState.rain_chance,
                    label="Rain",
                ),
                gap="12px",
                width="100%",
            ),

            # ==============================
            # SECTION 5: 7-Day Forecast Grid
            # ==============================
            rx.box(
                rx.text(
                    "7-Day Forecast",
                    font_size="20px",
                    font_weight="700",
                    color=COLORS["text_primary"],
                    margin_bottom="16px",
                ),
                # Grid of forecast days
                rx.box(
                    rx.grid(
                        rx.foreach(
                            WeatherState.weekly_forecast,
                            forecast_day,
                        ),
                        columns="4",
                        gap="8px",
                        width="100%",
                    ),
                    # Buddy character peeking from bottom-left
                    rx.box(
                        buddy_avatar(size="peek", enable_float=True),
                        position="absolute",
                        bottom="-10px",
                        left="-10px",
                        opacity="0.9",
                    ),
                    position="relative",
                    overflow="visible",
                ),
                width="100%",
            ),

            # ---- Bottom padding for navbar ----
            rx.box(height="100px"),

            # ---- VStack Layout ----
            width="100%",
            max_width="430px",
            padding_left="20px",
            padding_right="20px",
            padding_top="20px",
            gap="20px",
            align_items="stretch",
            animation="slide_up 0.5s ease-out",
        ),

        # ==============================
        # AI CHAT FAB (sparkle icon)
        # ==============================
        rx.link(
            rx.box(
                rx.icon(
                    tag="sparkles",
                    size=22,
                    color=COLORS["text_on_primary"],
                ),
                width="52px",
                height="52px",
                display="flex",
                align_items="center",
                justify_content="center",
                border_radius="50%",
                background_color=COLORS["primary"],
                box_shadow=COLORS["shadow_medium"],
                cursor="pointer",
                transition="all 0.2s ease",
                _hover={
                    "transform": "scale(1.1)",
                    "box_shadow": COLORS["shadow_hover"],
                },
            ),
            href="/chat",
            position="fixed",
            bottom="100px",
            right="calc(50% - 195px)",
            z_index="40",
            text_decoration="none",
        ),

        # ==============================
        # BOTTOM NAVBAR
        # ==============================
        navbar(active_page="weather"),

        # ---- Page Background ----
        style=PAGE_BACKGROUND_STYLE,
        display="flex",
        flex_direction="column",
        align_items="center",
        overflow_y="auto",
        on_mount=[UserState.check_setup, WeatherState.fetch_weather],
    )
