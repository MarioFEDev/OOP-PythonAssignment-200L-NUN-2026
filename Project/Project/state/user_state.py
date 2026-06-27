"""
user_state.py — Persistent user profile state.

Stores the user's name, chosen city (with lat/lon for Open-Meteo),
chosen assistant (0-4), and whether onboarding has been completed.

All vars use rx.LocalStorage so they survive browser refreshes.
"""

import reflex as rx


# ---------------------------------------------------------------------------
# ASSISTANT DEFINITIONS
# Each assistant has a name, personality tag, accent colour, and image path.
# All images currently use the same placeholder — replace paths when PNGs
# are ready.
# ---------------------------------------------------------------------------
ASSISTANTS: list[dict] = [
    {
        "id": "0",
        "name": "Maya",
        "short_desc": "Warm, approachable, stylish",
        "personality": "The Creative & Lifestyle Coach. Warm, approachable, and stylish. Perfect for brainstorming, creative writing, health and wellness tips, or daily motivation. She’s the empathetic listener and idea generator.",
        "accent": "#C75B12",
        "accent_light": "#FFE0C0",
        "image": "/maya.png",
        "greeting_image": "/maya_greeting.png",
        "icon": "smile",
    },
    {
        "id": "1",
        "name": "Dev",
        "short_desc": "Modern, focused, tech-savvy",
        "personality": "The Tech & Coding Guru. Modern, focused, and tech-savvy. Your go-to for programming help, troubleshooting software issues, explaining complex tech concepts, or managing data architecture.",
        "accent": "#1976D2",
        "accent_light": "#E3F2FD",
        "image": "/devin.png",
        "greeting_image": "/devin_greeting.png",
        "icon": "terminal",
    },
    {
        "id": "2",
        "name": "Riley",
        "short_desc": "Quirky, expressive, trendy",
        "personality": "The Social Media & Design Strategist. Quirky, expressive, and trend-focused. Ideal for generating marketing copy, brainstorming graphic design ideas, keeping up with pop culture trends, or planning social media calendars.",
        "accent": "#9C27B0",
        "accent_light": "#F3E5F5",
        "image": "/riley.png",
        "greeting_image": "/riley_greeting.png",
        "icon": "sparkles",
    },
    {
        "id": "3",
        "name": "Eleanor",
        "short_desc": "Wise, professional, reliable",
        "personality": "The Researcher & Academic Tutor. Wise, professional, and reliable. The expert for deep-dive research, historical facts, language translation, proofreading, and studying for exams.",
        "accent": "#455A64",
        "accent_light": "#CFD8DC",
        "image": "/eleanor.png",
        "greeting_image": "/eleanor_greeting.png",
        "icon": "book-open",
    },
    {
        "id": "4",
        "name": "Kenji",
        "short_desc": "Futuristic, precise, efficient",
        "personality": "The Data & Automation Specialist. Futuristic, precise, and highly efficient. Best for crunching numbers, generating spreadsheets, analyzing financial data, or creating optimized daily schedules and logic puzzles.",
        "accent": "#00796B",
        "accent_light": "#E0F2F1",
        "image": "/kenji.png",
        "greeting_image": "/kenji_greeting.png",
        "icon": "cpu",
    },
    {
        "id": "5",
        "name": "Aisha",
        "short_desc": "Relaxed, youthful, plugged-in",
        "personality": "The Entertainment & Focus Buddy. Relaxed, youthful, and plugged-in. Great for recommending music, movies, or video games. She can also act as a 'body double' for studying, setting Pomodoro timers, or casual, friendly chatting.",
        "accent": "#E91E63",
        "accent_light": "#FCE4EC",
        "image": "/aisha.png",
        "greeting_image": "/aisha_greeting.png",
        "icon": "headphones",
    },
]

# ---------------------------------------------------------------------------
# CITY CATALOGUE — pre-baked lat/lon for Open-Meteo
# Format: "City, Country" → (lat_str, lon_str)
# ---------------------------------------------------------------------------
CITIES: list[dict] = [
    # ---- Nigeria ----
    {"name": "Abuja, Nigeria",           "lat": "9.0579",   "lon": "7.4951"},
    {"name": "Lagos, Nigeria",           "lat": "6.5244",   "lon": "3.3792"},
    {"name": "Kano, Nigeria",            "lat": "12.0022",  "lon": "8.5920"},
    {"name": "Port Harcourt, Nigeria",   "lat": "4.8156",   "lon": "7.0498"},
    {"name": "Ibadan, Nigeria",          "lat": "7.3775",   "lon": "3.9470"},
    {"name": "Enugu, Nigeria",           "lat": "6.4584",   "lon": "7.5464"},
    {"name": "Kaduna, Nigeria",          "lat": "10.5105",  "lon": "7.4165"},
    {"name": "Benin City, Nigeria",      "lat": "6.3350",   "lon": "5.6270"},
    # ---- Rest of Africa ----
    {"name": "Nairobi, Kenya",           "lat": "-1.2921",  "lon": "36.8219"},
    {"name": "Accra, Ghana",             "lat": "5.6037",   "lon": "-0.1870"},
    {"name": "Cairo, Egypt",             "lat": "30.0444",  "lon": "31.2357"},
    {"name": "Johannesburg, South Africa","lat": "-26.2041","lon": "28.0473"},
    {"name": "Cape Town, South Africa",  "lat": "-33.9249", "lon": "18.4241"},
    {"name": "Dakar, Senegal",           "lat": "14.7167",  "lon": "-17.4677"},
    {"name": "Addis Ababa, Ethiopia",    "lat": "9.1450",   "lon": "40.4897"},
    {"name": "Kampala, Uganda",          "lat": "0.3476",   "lon": "32.5825"},
    {"name": "Dar es Salaam, Tanzania",  "lat": "-6.7924",  "lon": "39.2083"},
    # ---- Europe ----
    {"name": "London, UK",              "lat": "51.5074",  "lon": "-0.1278"},
    {"name": "Paris, France",           "lat": "48.8566",  "lon": "2.3522"},
    {"name": "Berlin, Germany",         "lat": "52.5200",  "lon": "13.4050"},
    {"name": "Madrid, Spain",           "lat": "40.4168",  "lon": "-3.7038"},
    {"name": "Rome, Italy",             "lat": "41.9028",  "lon": "12.4964"},
    {"name": "Amsterdam, Netherlands",  "lat": "52.3676",  "lon": "4.9041"},
    # ---- Americas ----
    {"name": "New York, USA",           "lat": "40.7128",  "lon": "-74.0060"},
    {"name": "Los Angeles, USA",        "lat": "34.0522",  "lon": "-118.2437"},
    {"name": "Chicago, USA",            "lat": "41.8781",  "lon": "-87.6298"},
    {"name": "Toronto, Canada",         "lat": "43.6532",  "lon": "-79.3832"},
    {"name": "São Paulo, Brazil",       "lat": "-23.5505", "lon": "-46.6333"},
    {"name": "Buenos Aires, Argentina", "lat": "-34.6037", "lon": "-58.3816"},
    {"name": "Mexico City, Mexico",     "lat": "19.4326",  "lon": "-99.1332"},
    # ---- Asia & Middle East ----
    {"name": "Dubai, UAE",              "lat": "25.2048",  "lon": "55.2708"},
    {"name": "Mumbai, India",           "lat": "19.0760",  "lon": "72.8777"},
    {"name": "Delhi, India",            "lat": "28.6139",  "lon": "77.2090"},
    {"name": "Singapore",               "lat": "1.3521",   "lon": "103.8198"},
    {"name": "Tokyo, Japan",            "lat": "35.6762",  "lon": "139.6503"},
    {"name": "Beijing, China",          "lat": "39.9042",  "lon": "116.4074"},
    {"name": "Seoul, South Korea",      "lat": "37.5665",  "lon": "126.9780"},
    {"name": "Bangkok, Thailand",       "lat": "13.7563",  "lon": "100.5018"},
    # ---- Oceania ----
    {"name": "Sydney, Australia",       "lat": "-33.8688", "lon": "151.2093"},
    {"name": "Melbourne, Australia",    "lat": "-37.8136", "lon": "144.9631"},
]

# Build a flat list of city name strings for the dropdown options
CITY_NAMES: list[str] = [c["name"] for c in CITIES]

# Build a lookup dict: name -> {lat, lon}
CITY_LOOKUP: dict[str, dict] = {c["name"]: c for c in CITIES}


class UserState(rx.State):
    """
    Persistent user profile.

    All vars backed by rx.LocalStorage — they survive page refreshes
    and browser restarts for the same browser/device.
    """

    # ---- Profile fields (persisted) ----
    user_name: str = rx.LocalStorage("", name="buddy_user_name")
    location_name: str = rx.LocalStorage("Abuja, Nigeria", name="buddy_location_name")
    location_lat: str = rx.LocalStorage("9.0579", name="buddy_location_lat")
    location_lon: str = rx.LocalStorage("7.4951", name="buddy_location_lon")
    assistant_id: str = rx.LocalStorage("0", name="buddy_assistant_id")
    # setup_complete stored as "1" (done) or "" (not done) for Cookie compat
    _setup_flag: str = rx.Cookie("", name="buddy_setup_flag")

    # ---- Onboarding form fields (not persisted) ----
    form_name: str = ""
    form_location: str = "Abuja, Nigeria"
    form_assistant_id: str = "0"

    # ---- Validation ----
    name_error: str = ""

    # ---- Computed vars ----

    @rx.var
    def setup_complete(self) -> bool:
        """True if the user has completed onboarding."""
        return self._setup_flag == "1"

    @rx.var
    def assistant_info(self) -> dict:
        """Return the full assistant dict for the currently chosen assistant."""
        try:
            idx = int(self.assistant_id)
            if 0 <= idx < len(ASSISTANTS):
                return ASSISTANTS[idx]
        except (ValueError, IndexError):
            pass
        return ASSISTANTS[0]

    @rx.var
    def assistant_image(self) -> str:
        """Return the image path for the current assistant."""
        return self.assistant_info["image"]

    @rx.var
    def assistant_name(self) -> str:
        """Return the display name of the current assistant."""
        return self.assistant_info["name"]

    @rx.var
    def display_city(self) -> str:
        """Return just the city portion of location_name (before the comma)."""
        parts = self.location_name.split(",")
        return parts[0].strip() if parts else self.location_name

    # ---- Event Handlers ----

    @rx.event
    def set_form_name(self, value: str):
        self.form_name = value
        self.name_error = ""

    @rx.event
    def set_form_location(self, value: str):
        self.form_location = value

    @rx.event
    def set_form_assistant(self, assistant_id: str):
        self.form_assistant_id = assistant_id

    @rx.event
    def complete_setup(self):
        """
        Validate form, save profile to localStorage, and redirect to home.
        Called when user taps 'Let's Go!' on the setup page.
        """
        # Validate name
        name = self.form_name.strip()
        if not name:
            self.name_error = "Please enter your name to continue."
            return

        # Save profile
        self.user_name = name

        # Look up lat/lon from selected city
        city_data = CITY_LOOKUP.get(self.form_location)
        if city_data:
            self.location_name = city_data["name"]
            self.location_lat = city_data["lat"]
            self.location_lon = city_data["lon"]
        else:
            # Fallback to Abuja
            self.location_name = "Abuja, Nigeria"
            self.location_lat = "9.0579"
            self.location_lon = "7.4951"

        self.assistant_id = self.form_assistant_id
        self._setup_flag = "1"
        self.name_error = ""

        return rx.redirect("/")

    @rx.event
    def check_setup(self):
        """
        Called on_mount for every main page.
        Redirects to /setup if the user has not completed onboarding.
        """
        if not self.setup_complete:
            return rx.redirect("/setup")

    @rx.event
    def reset_setup(self):
        """
        Clear the saved profile (for testing / re-onboarding).
        """
        self.user_name = ""
        self.location_name = "Abuja, Nigeria"
        self.location_lat = "9.0579"
        self.location_lon = "7.4951"
        self.assistant_id = "0"
        self._setup_flag = ""
        self.form_name = ""
        self.form_location = "Abuja, Nigeria"
        self.form_assistant_id = "0"
        return rx.redirect("/setup")
