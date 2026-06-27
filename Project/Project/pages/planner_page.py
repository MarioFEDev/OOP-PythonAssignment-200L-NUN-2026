"""
planner_page.py — The full day planner screen.

Shows the user's complete schedule grouped by Morning / Afternoon / Evening.
Includes:
  - Inline add-task form (triggered by FAB)
  - Inline edit form per task
  - Empty-state messages per section
  - Full CRUD wired to PlannerState

Route: /planner
"""

import reflex as rx
from Project.theme import (
    COLORS, PAGE_BACKGROUND_STYLE, SUGGESTION_CARD_STYLE, CARD_HOVER,
    GLASS_CARD_STYLE,
)
from Project.state.app_state import AppState
from Project.state.planner_state import PlannerState
from Project.state.user_state import UserState
from Project.state.companion_state import CompanionState
from Project.components.navbar import navbar
from Project.components.buddy_avatar import buddy_avatar
from Project.components.task_item import task_item


# ---------------------------------------------------------------------------
# Form helpers
# ---------------------------------------------------------------------------

_CATEGORIES = ["work", "health", "errands", "personal"]
_PERIODS = ["morning", "afternoon", "evening"]

def _inline_form(
    title_val,
    time_val,
    cat_val,
    period_val,
    error_val,
    on_title,
    on_time,
    on_cat,
    on_period,
    on_save,
    on_cancel,
    save_label: str = "Add Task",
) -> rx.Component:
    """Shared inline form used for both Add and Edit."""
    return rx.box(
        rx.vstack(
            # Title
            rx.input(
                placeholder="Task title…",
                value=title_val,
                on_change=on_title,
                font_size="15px",
                height="44px",
                padding_left="14px",
                padding_right="14px",
                border_radius="10px",
                border=f"2px solid {COLORS['border']}",
                background_color=COLORS["background_input"],
                color=COLORS["text_primary"],
                width="100%",
                _focus={
                    "border_color": COLORS["primary"],
                    "outline": "none",
                },
            ),
            # Time
            rx.input(
                type="time",
                placeholder="Time",
                value=time_val,
                on_change=on_time,
                font_size="14px",
                height="44px",
                padding_left="14px",
                padding_right="14px",
                border_radius="10px",
                border=f"2px solid {COLORS['border']}",
                background_color=COLORS["background_input"],
                color=COLORS["text_primary"],
                width="100%",
                _focus={
                    "border_color": COLORS["primary"],
                    "outline": "none",
                },
            ),
            # Category + Period row
            rx.flex(
                rx.select(
                    _CATEGORIES,
                    value=cat_val,
                    on_change=on_cat,
                    placeholder="Category",
                    flex="1",
                    border_radius="10px",
                    border=f"2px solid {COLORS['border']}",
                    background_color=COLORS["background_input"],
                    color=COLORS["text_primary"],
                    padding="2px 6px",
                    _focus={"border_color": COLORS["primary"], "outline": "none"},
                ),
                rx.select(
                    _PERIODS,
                    value=period_val,
                    on_change=on_period,
                    placeholder="Period",
                    flex="1",
                    border_radius="10px",
                    border=f"2px solid {COLORS['border']}",
                    background_color=COLORS["background_input"],
                    color=COLORS["text_primary"],
                    padding="2px 6px",
                    _focus={"border_color": COLORS["primary"], "outline": "none"},
                ),
                gap="8px",
                width="100%",
            ),
            # Error
            rx.cond(
                error_val != "",
                rx.flex(
                    rx.icon(tag="triangle-alert", size=13, color="#E53935"),
                    rx.text(error_val, font_size="12px", color="#E53935"),
                    gap="5px",
                    align_items="center",
                ),
                rx.fragment(),
            ),
            # Buttons
            rx.flex(
                rx.box(
                    rx.text(save_label, font_size="14px", font_weight="600",
                            color=COLORS["text_on_primary"]),
                    flex="1",
                    padding="10px",
                    background_color=COLORS["primary"],
                    border_radius="10px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    cursor="pointer",
                    on_click=on_save,
                    transition="all 0.2s ease",
                    _hover={"background_color": COLORS["primary_hover"]},
                ),
                rx.box(
                    rx.text("Cancel", font_size="14px", font_weight="500",
                            color=COLORS["text_secondary"]),
                    flex="1",
                    padding="10px",
                    border=f"1px solid {COLORS['border']}",
                    border_radius="10px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    cursor="pointer",
                    on_click=on_cancel,
                    transition="all 0.2s ease",
                    background_color=COLORS["background_card"],
                    _hover={"background_color": COLORS["primary_light"]},
                ),
                gap="8px",
                width="100%",
            ),
            gap="10px",
            width="100%",
            align_items="stretch",
        ),
        background_color=COLORS["background_card"],
        border=f"2px solid {COLORS['primary_light']}",
        border_radius="16px",
        padding="16px",
        width="100%",
        box_shadow=COLORS["shadow_soft"],
    )


def _add_form() -> rx.Component:
    return _inline_form(
        title_val=PlannerState.add_title,
        time_val=PlannerState.add_time,
        cat_val=PlannerState.add_category,
        period_val=PlannerState.add_period,
        error_val=PlannerState.add_error,
        on_title=PlannerState.set_add_title,
        on_time=PlannerState.set_add_time,
        on_cat=PlannerState.set_add_category,
        on_period=PlannerState.set_add_period,
        on_save=PlannerState.submit_add,
        on_cancel=PlannerState.close_add_form,
        save_label="Add Task",
    )


def _edit_form() -> rx.Component:
    return _inline_form(
        title_val=PlannerState.edit_title,
        time_val=PlannerState.edit_time,
        cat_val=PlannerState.edit_category,
        period_val=PlannerState.edit_period,
        error_val=PlannerState.edit_error,
        on_title=PlannerState.set_edit_title,
        on_time=PlannerState.set_edit_time,
        on_cat=PlannerState.set_edit_category,
        on_period=PlannerState.set_edit_period,
        on_save=PlannerState.save_edit,
        on_cancel=PlannerState.cancel_edit,
        save_label="Save Changes",
    )


def _empty_section(period_label: str) -> rx.Component:
    """Message shown when a period group has no tasks."""
    return rx.flex(
        rx.icon(tag="circle-plus", size=16, color=COLORS["text_muted"]),
        rx.text(
            f"No {period_label.lower()} tasks — tap + to add one",
            font_size="13px",
            color=COLORS["text_muted"],
            font_style="italic",
        ),
        gap="6px",
        align_items="center",
        padding_top="8px",
        padding_bottom="8px",
        padding_left="4px",
    )


def _task_section(label: str, tasks_var, has_var) -> rx.Component:
    """A labelled group of tasks with an empty-state fallback."""
    return rx.vstack(
        rx.text(
            label,
            font_size="16px",
            font_weight="700",
            color=COLORS["text_primary"],
        ),
        rx.cond(
            has_var,
            rx.foreach(tasks_var, task_item),
            _empty_section(label),
        ),
        width="100%",
        gap="0px",
        align_items="flex-start",
    )


# ---------------------------------------------------------------------------
# Main page
# ---------------------------------------------------------------------------

def planner_page() -> rx.Component:
    """Render the complete planner page."""
    return rx.box(
        rx.vstack(
            # ==============================
            # SECTION 1: Header
            # ==============================
            rx.flex(
                rx.icon(tag="calendar", size=22, color=COLORS["primary"]),
                rx.text("Planner", font_size="20px", font_weight="800",
                        color=COLORS["primary_dark"]),
                rx.box(
                    rx.image(
                        src=UserState.assistant_image,
                        alt="User Avatar",
                        width="100%", height="100%",
                        object_fit="cover", border_radius="50%",
                    ),
                    width="36px", height="36px",
                    border_radius="50%",
                    border=f"2px solid {COLORS['primary_light']}",
                    overflow="hidden", flex_shrink="0",
                ),
                justify="between", align_items="center", width="100%",
            ),

            # ==============================
            # SECTION 2: Date & Summary
            # ==============================
            rx.vstack(
                rx.flex(
                    rx.text("Today's Plan", font_size="16px", font_weight="600",
                            color=COLORS["text_primary"]),
                    rx.box(
                        rx.text(PlannerState.today_date, font_size="13px",
                                font_weight="600", color=COLORS["primary"]),
                        padding_left="10px", padding_right="10px",
                        padding_top="4px", padding_bottom="4px",
                        background_color=COLORS["primary_light"],
                        border_radius="8px",
                    ),
                    gap="10px", align_items="center",
                ),
                rx.text(PlannerState.today_summary, font_size="14px",
                        color=COLORS["text_secondary"], line_height="1.5"),
                # Progress bar
                rx.cond(
                    PlannerState.task_count > 0,
                    rx.vstack(
                        rx.flex(
                            rx.text(
                                PlannerState.done_count.to(str) + " / " +
                                PlannerState.task_count.to(str) + " done",
                                font_size="12px", color=COLORS["text_muted"],
                            ),
                            width="100%",
                        ),
                        rx.box(
                            rx.box(
                                width=rx.cond(
                                    PlannerState.task_count > 0,
                                    (PlannerState.done_count * 100 // PlannerState.task_count).to(str) + "%",
                                    "0%",
                                ),
                                height="100%",
                                background_color=COLORS["primary"],
                                border_radius="4px",
                                transition="width 0.4s ease",
                            ),
                            width="100%", height="6px",
                            background_color=COLORS["primary_light"],
                            border_radius="4px",
                            overflow="hidden",
                        ),
                        gap="4px", width="100%", align_items="stretch",
                    ),
                    rx.fragment(),
                ),
                align_items="flex-start", gap="6px", width="100%",
            ),

            # ==============================
            # SECTION 3: Buddy Suggestion
            # ==============================
            rx.box(
                rx.flex(
                    buddy_avatar(size="small"),
                    rx.vstack(
                        rx.flex(
                            rx.text(UserState.assistant_name, " Suggests", font_size="13px",
                                    font_weight="700", color=COLORS["primary"]),
                            rx.box(width="6px", height="6px", border_radius="50%",
                                   background_color=COLORS["primary"]),
                            gap="6px", align_items="center",
                        ),
                        rx.text(PlannerState.planner_suggestion, font_size="13px",
                                color=COLORS["text_primary"], line_height="1.4"),
                        align_items="flex-start", gap="4px", flex="1",
                    ),
                    gap="12px", align_items="flex-start", width="100%",
                ),
                style=SUGGESTION_CARD_STYLE,
                _hover=CARD_HOVER,
                width="100%",
            ),

            # ==============================
            # SECTION 4: Add Form (conditional)
            # ==============================
            rx.cond(
                PlannerState.show_add_form,
                _add_form(),
                rx.fragment(),
            ),

            # ==============================
            # SECTION 5: Edit Form (conditional)
            # ==============================
            rx.cond(
                PlannerState.edit_id != "",
                rx.box(
                    rx.flex(
                        rx.icon(tag="pencil", size=14, color=COLORS["primary"]),
                        rx.text("Edit Task", font_size="13px", font_weight="700",
                                color=COLORS["primary"]),
                        gap="6px", align_items="center",
                        margin_bottom="4px",
                    ),
                    _edit_form(),
                    width="100%",
                ),
                rx.fragment(),
            ),

            # ==============================
            # SECTION 6: Task Sections
            # ==============================
            _task_section("Morning", PlannerState.morning_tasks, PlannerState.has_morning),
            _task_section("Afternoon", PlannerState.afternoon_tasks, PlannerState.has_afternoon),
            _task_section("Evening", PlannerState.evening_tasks, PlannerState.has_evening),

            # Bottom padding
            rx.box(height="100px"),

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
        # FAB — Add Task
        # ==============================
        rx.box(
            rx.icon(tag="plus", size=24, color=COLORS["text_on_primary"]),
            width="56px", height="56px",
            display="flex", align_items="center", justify_content="center",
            border_radius="50%",
            background_color=COLORS["primary"],
            box_shadow=COLORS["shadow_medium"],
            position="fixed",
            bottom="100px",
            right="calc(50% - 195px)",
            cursor="pointer",
            transition="all 0.2s ease",
            z_index="40",
            on_click=PlannerState.open_add_form,
            _hover={
                "transform": "scale(1.1) rotate(45deg)",
                "box_shadow": COLORS["shadow_hover"],
            },
        ),

        # ==============================
        # BOTTOM NAVBAR
        # ==============================
        navbar(active_page="planner"),

        # ---- Page Background ----
        style=PAGE_BACKGROUND_STYLE,
        display="flex",
        flex_direction="column",
        align_items="center",
        overflow_y="auto",
        on_mount=[UserState.check_setup],
    )
