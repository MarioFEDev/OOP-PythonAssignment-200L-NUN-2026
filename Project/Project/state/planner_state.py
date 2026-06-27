"""
planner_state.py — State for the day planner / schedule system.

Tasks are stored in rx.LocalStorage so they persist across refreshes.
Full CRUD: add, toggle, edit, delete.

Task dict schema:
    id       — unique string id
    title    — display name
    time     — time string (e.g. "8:00 AM")
    category — "health" | "work" | "errands" | "personal"
    period   — "morning" | "afternoon" | "evening"
    is_done  — "true" | "false"
"""

import reflex as rx
from datetime import datetime
import json
import uuid


def _new_id() -> str:
    """Generate a short unique id."""
    return uuid.uuid4().hex[:8]


def _sort_by_time(tasks: list[dict[str, str]]) -> list[dict[str, str]]:
    def _get_sort_key(t: dict[str, str]):
        time_str = t.get("time", "").strip()
        try:
            return datetime.strptime(time_str, "%H:%M")
        except ValueError:
            pass
        try:
            return datetime.strptime(time_str, "%I:%M %p")
        except ValueError:
            pass
        return datetime.min
    return sorted(tasks, key=_get_sort_key)


class PlannerState(rx.State):
    """
    Manages the user's daily schedule and task list.

    All tasks are stored in rx.LocalStorage for persistence.
    The add/edit forms live here as temporary state vars (not persisted).
    """

    # ---- Planner Buddy Suggestion ----
    planner_suggestion: str = (
        "Stay organised — add your tasks for the day "
        "and I'll help you manage your time!"
    )

    # ---- Task storage ----
    # _tasks_json is persisted to localStorage as a JSON string.
    _tasks_json: str = rx.LocalStorage("", name="buddy_tasks_json")

    @rx.var
    def tasks(self) -> list[dict[str, str]]:
        if self._tasks_json:
            try:
                loaded = json.loads(self._tasks_json)
                if isinstance(loaded, list):
                    return loaded
            except (json.JSONDecodeError, TypeError):
                pass
        return []

    @rx.var
    def today_date(self) -> str:
        return datetime.now().strftime("%b %d")

    @rx.var
    def today_summary(self) -> str:
        pending = self.task_count - self.done_count
        if self.task_count == 0:
            return "No tasks yet — tap + to add one!"
        elif pending == 0:
            return f"All {self.task_count} tasks done — great work! 🎉"
        else:
            return (
                f"{pending} task{'s' if pending != 1 else ''} remaining "
                f"out of {self.task_count} today."
            )

    # ---- Add-form state (not persisted) ----
    show_add_form: bool = False
    add_title: str = ""
    add_time: str = ""
    add_category: str = "work"
    add_period: str = "morning"
    add_error: str = ""

    # ---- Edit-form state (not persisted) ----
    edit_id: str = ""
    edit_title: str = ""
    edit_time: str = ""
    edit_category: str = "work"
    edit_period: str = "morning"
    edit_error: str = ""

    # ---- Computed Vars ----

    @rx.var
    def morning_tasks(self) -> list[dict[str, str]]:
        """Tasks in the 'morning' period."""
        return _sort_by_time([t for t in self.tasks if t.get("period") == "morning"])

    @rx.var
    def afternoon_tasks(self) -> list[dict[str, str]]:
        """Tasks in the 'afternoon' period."""
        return _sort_by_time([t for t in self.tasks if t.get("period") == "afternoon"])

    @rx.var
    def evening_tasks(self) -> list[dict[str, str]]:
        """Tasks in the 'evening' period."""
        return _sort_by_time([t for t in self.tasks if t.get("period") == "evening"])

    @rx.var
    def task_count(self) -> int:
        return len(self.tasks)

    @rx.var
    def done_count(self) -> int:
        return sum(1 for t in self.tasks if t.get("is_done") == "true")

    @rx.var
    def has_morning(self) -> bool:
        return len(self.morning_tasks) > 0

    @rx.var
    def has_afternoon(self) -> bool:
        return len(self.afternoon_tasks) > 0

    @rx.var
    def has_evening(self) -> bool:
        return len(self.evening_tasks) > 0

    @rx.var
    def home_schedule(self) -> list[dict[str, str]]:
        """Up to 3 incomplete tasks for the home page preview."""
        incomplete = [t for t in self.tasks if t.get("is_done") != "true"]
        preview = incomplete[:3]
        result = []
        for t in preview:
            cat = t.get("category", "work")
            icon_map = {"health": "heart", "work": "briefcase", "errands": "shopping-cart", "personal": "user"}
            result.append({
                "title": t.get("title", ""),
                "time": t.get("time", ""),
                "category": cat,
                "status": "scheduled",
                "icon": icon_map.get(cat, "circle"),
            })
        return result

    def _save(self, updated_tasks: list[dict[str, str]]):
        """Serialise tasks to JSON string for localStorage."""
        self._tasks_json = json.dumps(updated_tasks)

    def add_task_from_external(self, new_task: dict):
        """Helper for ChatState to add tasks safely."""
        updated = self.tasks + [new_task]
        self._save(updated)

    def remove_task_from_external(self, task_id: str):
        """Helper for ChatState to remove tasks safely."""
        updated = [t for t in self.tasks if t["id"] != task_id]
        self._save(updated)

    def edit_task_from_external(self, task_id: str, title: str, time: str, category: str, period: str):
        """Helper for ChatState to edit tasks safely."""
        updated = []
        for task in self.tasks:
            if task["id"] == task_id:
                t = dict(task)
                t["title"] = title
                t["time"] = time
                t["category"] = category
                t["period"] = period
                updated.append(t)
            else:
                updated.append(task)
        self._save(updated)

    # ---- Toggle ----

    @rx.event
    def toggle_task(self, task_id: str):
        """Flip a task's done/not-done status."""
        updated = []
        for task in self.tasks:
            if task["id"] == task_id:
                t = dict(task)
                t["is_done"] = "false" if t["is_done"] == "true" else "true"
                updated.append(t)
            else:
                updated.append(task)
        self._save(updated)

    # ---- Add form ----

    @rx.event
    def open_add_form(self):
        self.show_add_form = True
        self.add_title = ""
        self.add_time = ""
        self.add_category = "work"
        self.add_period = "morning"
        self.add_error = ""
        # Close any edit form that's open
        self.edit_id = ""

    @rx.event
    def close_add_form(self):
        self.show_add_form = False
        self.add_error = ""

    @rx.event
    def set_add_title(self, v: str):
        self.add_title = v
        self.add_error = ""

    @rx.event
    def set_add_time(self, v: str):
        self.add_time = v

    @rx.event
    def set_add_category(self, v: str):
        self.add_category = v

    @rx.event
    def set_add_period(self, v: str):
        self.add_period = v

    @rx.event
    def submit_add(self):
        """Save the new task."""
        title = self.add_title.strip()
        if not title:
            self.add_error = "Task title is required."
            return
        new_task = {
            "id": _new_id(),
            "title": title,
            "time": self.add_time.strip() or "No time set",
            "category": self.add_category,
            "period": self.add_period,
            "is_done": "false",
        }
        updated = self.tasks + [new_task]
        self._save(updated)
        self.show_add_form = False
        self.add_title = ""
        self.add_time = ""
        self.add_error = ""

    # ---- Delete ----

    @rx.event
    def delete_task(self, task_id: str):
        """Remove a task by id."""
        updated = [t for t in self.tasks if t["id"] != task_id]
        self._save(updated)
        if self.edit_id == task_id:
            self.edit_id = ""

    # ---- Edit form ----

    @rx.event
    def start_edit(self, task_id: str):
        """Populate edit form for the given task."""
        for task in self.tasks:
            if task["id"] == task_id:
                self.edit_id = task_id
                self.edit_title = task["title"]
                self.edit_time = task["time"]
                self.edit_category = task["category"]
                self.edit_period = task["period"]
                self.edit_error = ""
                # Close add form if open
                self.show_add_form = False
                break

    @rx.event
    def cancel_edit(self):
        self.edit_id = ""
        self.edit_error = ""

    @rx.event
    def set_edit_title(self, v: str):
        self.edit_title = v
        self.edit_error = ""

    @rx.event
    def set_edit_time(self, v: str):
        self.edit_time = v

    @rx.event
    def set_edit_category(self, v: str):
        self.edit_category = v

    @rx.event
    def set_edit_period(self, v: str):
        self.edit_period = v

    @rx.event
    def save_edit(self):
        """Write edited fields back to the task."""
        title = self.edit_title.strip()
        if not title:
            self.edit_error = "Task title is required."
            return
        updated = []
        for task in self.tasks:
            if task["id"] == self.edit_id:
                t = dict(task)
                t["title"] = title
                t["time"] = self.edit_time.strip() or "No time set"
                t["category"] = self.edit_category
                t["period"] = self.edit_period
                updated.append(t)
            else:
                updated.append(task)
        self._save(updated)
        self.edit_id = ""
        self.edit_error = ""
