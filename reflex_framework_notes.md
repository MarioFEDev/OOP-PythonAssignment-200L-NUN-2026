# Reflex Python Framework — Reference Notes

## 1. What is Reflex?

Reflex is an **open-source Python framework** for building **full-stack web apps** entirely in pure Python. Under the hood:
- **Frontend** compiles to **React/Next.js** (runs in the browser)
- **Backend** runs on **FastAPI** (runs on the server)
- Communication between frontend ↔ backend is via **WebSockets** (automatic)

---

## 2. Project Structure

```
my_app/
├── .venv/                 # Virtual environment
├── .web/                  # Compiled JS (auto-generated, don't touch)
├── assets/                # Static files (images, fonts, etc.) — publicly served
├── my_app/
│   ├── __init__.py
│   └── my_app.py          # Main app code (pages, state, components)
├── rxconfig.py            # App configuration
└── pyproject.toml         # Python project metadata
```

### Setup commands:
```bash
pip install reflex
reflex init          # Scaffold the project
reflex run           # Start dev server (localhost:3000)
```

### Configuration (`rxconfig.py`):
```python
import reflex as rx
config = rx.Config(app_name="my_app")
```

---

## 3. Core Architecture: State → Events → Components

### 3.1 State (`rx.State`)
- Holds all mutable data (vars)
- Each user gets their own isolated copy
- All state lives on the server

```python
class State(rx.State):
    count: int = 0               # Base var (type-annotated)
    items: list[str] = []        # Lists, dicts, etc. are fine

    @rx.event
    def increment(self):         # Event handler — only way to modify vars
        self.count += 1

    @rx.var
    def doubled(self) -> int:    # Computed var — auto-updates when state changes
        return self.count * 2
```

**Key rules:**
- **Base Vars**: Declared as class attributes with type annotations. Modified only in event handlers.
- **Computed Vars**: Decorated with `@rx.var`. Return derived values. Cannot be set directly.
- **Event Handlers**: Decorated with `@rx.event`. Methods that modify base vars.
- **Helper Methods**: Start with `_` — backend-only, not callable from frontend.
- Never instantiate State directly — Reflex manages instances per-user.

### 3.2 Event Triggers & Handlers
- **Event Triggers**: Component props like `on_click`, `on_change`, `on_mouse_over`, etc.
- **Event Handlers**: State methods bound to triggers.
- Flow: User Action → Event Trigger → Event Handler (server) → State Update → UI Re-render

```python
rx.button("Click me", on_click=State.increment)
rx.input(on_change=State.set_name)  # Auto-generated setter for `name` var
```

### 3.3 Components (UI)
- Components are **Python functions** that return `rx.*` component trees
- Components are **nested** and **composed** like React
- They reference state vars reactively: `rx.heading(State.count)`

```python
def index():
    return rx.vstack(
        rx.heading(State.count, font_size="2em"),
        rx.button("Increment", on_click=State.increment),
        spacing="4",
    )
```

---

## 4. Built-in Component Library (60+)

### Layout
| Component | Use Case |
|-----------|----------|
| `rx.box` | Generic container, apply any CSS |
| `rx.flex` | Flexbox layout (responsive, dynamic sizing) |
| `rx.grid` | CSS Grid layout (rows & columns) |
| `rx.stack` / `rx.vstack` / `rx.hstack` | Vertical/Horizontal stacking with spacing |
| `rx.container` | Centered content with max-width |
| `rx.center` | Center content |
| `rx.card` | Card container |
| `rx.separator` | Visual divider |
| `rx.spacer` | Flexible space |

### Typography
`rx.heading`, `rx.text`, `rx.link`, `rx.code`, `rx.markdown`, `rx.blockquote`, `rx.em`, `rx.strong`, `rx.kbd`

### Forms
`rx.button`, `rx.input`, `rx.text_area`, `rx.select`, `rx.checkbox`, `rx.radio_group`, `rx.slider`, `rx.switch`, `rx.form`, `rx.upload`

### Data Display
`rx.avatar`, `rx.badge`, `rx.callout`, `rx.code_block`, `rx.data_list`, `rx.icon`, `rx.list`, `rx.progress`, `rx.scroll_area`, `rx.spinner`

### Overlay / Dialog
`rx.alert_dialog`, `rx.dialog`, `rx.drawer`, `rx.dropdown_menu`, `rx.context_menu`, `rx.popover`, `rx.hover_card`, `rx.tooltip`, `rx.toast`

### Disclosure
`rx.accordion`, `rx.tabs`, `rx.segmented_control`

### Media
`rx.image`, `rx.audio`, `rx.video`

### Charts / Graphing
`rx.recharts.*` (AreaChart, BarChart, LineChart, PieChart, RadarChart, etc.), `rx.plotly`, `rx.pyplot`

### Tables
`rx.table.*` (root, header, body, row, cell, etc.), `rx.data_table`, `rx.data_editor`

### Dynamic Rendering
- `rx.cond(condition, true_comp, false_comp)` — conditional rendering
- `rx.foreach(iterable, render_fn)` — render lists
- `rx.match(value, *cases)` — pattern matching

---

## 5. Styling

### 5.1 Three Levels (in order of precedence):
1. **Inline styles**: Props directly on components (`color="red"`, `font_size="2em"`)
2. **Component styles**: Default styles per component type in the app style dict
3. **Global styles**: Base styles for all components

### 5.2 Inline Styles
```python
rx.text("Hello", color="blue", font_size="1.5em", font_weight="bold")
```

### 5.3 Style Prop (reusable dicts)
```python
my_style = {"color": "green", "font_size": "1.2em"}
rx.text("Hello", style=my_style)
rx.text("World", style=[style1, style2])  # Merge multiple
```

### 5.4 Global / Component Styles
```python
style = {
    "font_family": "Inter",
    rx.text: {"font_family": "Roboto"},
    ".my-class": {"text_decoration": "underline"},
    "::selection": {"background_color": "violet"},
}
app = rx.App(style=style)
```

### 5.5 Pseudo Styles
```python
rx.text("Hover me", _hover={"color": "red"})
```

### 5.6 CSS Props
- All CSS properties work, using `snake_case` (e.g., `background_color`, `border_radius`, `margin_top`)
- Shorthand props also supported: `bg`, `p`, `m`, etc.

---

## 6. Theming (Radix UI based)

```python
app = rx.App(
    theme=rx.theme(
        appearance="light",      # "light" | "dark" | "inherit"
        has_background=True,
        radius="large",          # "none" | "small" | "medium" | "large" | "full"
        accent_color="teal",     # Any Radix color
        gray_color="mauve",
        panel_background="translucent",  # "solid" | "translucent"
        scaling="100%",
    )
)
```

### Color System
```python
rx.color("grass", 7)           # Radix color shade 1-12
rx.color("violet", 5, True)    # With alpha transparency
rx.color_mode_cond(light="black", dark="white")  # Light/dark conditional
```

### Color Scheme on Components
```python
rx.button("Submit", color_scheme="teal")
rx.badge("New", color_scheme="tomato")
```

### Toggle Dark/Light Mode
```python
from reflex.style import toggle_color_mode
rx.button("Toggle", on_click=toggle_color_mode)
```

---

## 7. Pages & Routing

```python
def index():
    return rx.text("Home page")

def about():
    return rx.text("About page")

app = rx.App()
app.add_page(index)                    # Route: /
app.add_page(about, route="/about")    # Route: /about
```

### Dynamic Routes
```python
app.add_page(user_page, route="/user/[user_id]")
# Access via: State.router.page.params
```

---

## 8. Key Patterns

### Conditional Rendering
```python
rx.cond(State.show, rx.text("Visible"), rx.text("Hidden"))
```

### Rendering Lists
```python
rx.foreach(State.items, lambda item: rx.text(item))
```

### Forms
```python
rx.form(
    rx.input(name="username", placeholder="Enter username"),
    rx.button("Submit", type="submit"),
    on_submit=State.handle_submit,
)
```

### Auto-generated Setters
For any base var `name: str`, Reflex auto-generates `State.set_name` as an event handler:
```python
rx.input(on_change=State.set_name)
```

### Background Tasks
```python
@rx.event(background=True)
async def long_task(self):
    # Runs without blocking UI
    async with self:
        self.result = await some_api_call()
```

---

## 9. Assets & Images
- Place in `assets/` directory
- Reference: `rx.image(src="/image.png")`

## 10. Database (built-in ORM)
- Based on SQLAlchemy
- Define models with `rx.Model`
- Query with `session.exec()`

---

## Quick Reference: Minimal App

```python
import reflex as rx

class State(rx.State):
    count: int = 0

    @rx.event
    def increment(self):
        self.count += 1

def index():
    return rx.center(
        rx.vstack(
            rx.heading(f"Count: {State.count}"),
            rx.button("Increment", on_click=State.increment),
            spacing="4",
        ),
        height="100vh",
    )

app = rx.App(
    theme=rx.theme(appearance="dark", accent_color="violet")
)
app.add_page(index)
```
