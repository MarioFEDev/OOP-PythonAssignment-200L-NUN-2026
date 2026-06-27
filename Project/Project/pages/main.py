# =============================================================================
# MEMORY MATCHING CARD GAME
# Built with Python, Tkinter, and Object-Oriented Programming
# =============================================================================
# PROJECT FOLDER STRUCTURE:
#
#   memory_game/
#   ├── main.py              ← This file
#   └── images/
#       ├── card_back.png    ← Shown when card is face-down
#       ├── dog.png
#       ├── cat.png
#       ├── bird.png
#       ├── tree.png
#       ├── flower.png
#       ├── heart.png
#       ├── star.png
#       └── sun.png
#
# All images should be 100x100 pixels (PNG format recommended).
# Place the images/ folder in the SAME directory as main.py.
# =============================================================================

import tkinter as tk
from tkinter import messagebox
import random
import os
import time


# =============================================================================
# CLASS: Card
# Represents a single card on the game board.
# Stores the card's image, position, and state (flipped/matched).
# =============================================================================
class Card:
    def __init__(self, image_name, position):
        """
        Initialize a Card object.

        Args:
            image_name (str): The filename of the card's image (e.g., 'dog.png')
            position (tuple): The (row, col) position of the card on the board
        """
        self.image_name = image_name       # Name of the image file this card holds
        self.position = position           # (row, col) on the 4x4 grid
        self.is_flipped = False            # True if card is face-up
        self.is_matched = False            # True if this card has been matched
        self.button = None                 # The Tkinter Button widget for this card
        self.photo_image = None            # The loaded PhotoImage object (face image)


# =============================================================================
# CLASS: Board
# Manages the arrangement, creation, and shuffling of all 16 cards.
# =============================================================================
class Board:
    # The 8 unique image names — each will appear twice on the board
    IMAGE_NAMES = [
        "dog.png", "cat.png", "bird.png", "tree.png",
        "flower.png", "heart.png", "star.png", "sun.png"
    ]

    def __init__(self, images_folder="images"):
        """
        Initialize the Board.

        Args:
            images_folder (str): Path to the folder containing all PNG images
        """
        self.images_folder = images_folder  # Folder where images are stored
        self.cards = []                     # 2D list of Card objects (4 rows x 4 cols)
        self.card_back_image = None         # PhotoImage for the card back

    def load_card_back(self):
        """
        Load the card back image from disk.
        This image is displayed when a card is face-down.
        """
        path = os.path.join(self.images_folder, "card_back.png")
        try:
            # Load and resize the card back image to 90x90 pixels
            from PIL import Image, ImageTk
            img = Image.open(path).resize((90, 90), Image.LANCZOS)
            self.card_back_image = ImageTk.PhotoImage(img)
        except Exception:
            # If PIL is not available or image missing, use a blank placeholder
            self.card_back_image = None

    def create_and_shuffle_cards(self):
        """
        Create 16 Card objects (8 pairs), shuffle them randomly,
        and arrange them into a 4x4 grid.
        """
        # Duplicate each image name to create 8 pairs = 16 cards
        image_list = self.IMAGE_NAMES * 2

        # Shuffle the list randomly so cards appear in random positions
        random.shuffle(image_list)

        # Reset the cards list
        self.cards = []

        # Arrange cards into a 4x4 grid (4 rows, 4 columns)
        index = 0
        for row in range(4):
            row_cards = []
            for col in range(4):
                # Create a Card for this position with its assigned image
                card = Card(image_name=image_list[index], position=(row, col))
                row_cards.append(card)
                index += 1
            self.cards.append(row_cards)

    def load_card_images(self):
        """
        Pre-load all face images for every card from disk.
        Each Card's photo_image attribute is populated here.
        """
        try:
            from PIL import Image, ImageTk
            for row in self.cards:
                for card in row:
                    path = os.path.join(self.images_folder, card.image_name)
                    img = Image.open(path).resize((90, 90), Image.LANCZOS)
                    card.photo_image = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Image loading error: {e}")

    def get_card(self, row, col):
        """
        Retrieve a specific Card by its row and column position.

        Args:
            row (int): Row index (0–3)
            col (int): Column index (0–3)

        Returns:
            Card: The card at the given position
        """
        return self.cards[row][col]


# =============================================================================
# CLASS: Player
# Stores the player's score and move count.
# =============================================================================
class Player:
    def __init__(self):
        """Initialize the player with zero score and zero moves."""
        self.score = 0    # Points earned (1 point per matched pair)
        self.moves = 0    # Total number of move attempts (pairs flipped)

    def increment_moves(self):
        """Add one to the move counter each time two cards are flipped."""
        self.moves += 1

    def increment_score(self):
        """Add one to the score each time a pair is successfully matched."""
        self.score += 1

    def reset(self):
        """Reset the player's score and moves back to zero (for restart)."""
        self.score = 0
        self.moves = 0


# =============================================================================
# CLASS: MemoryGame
# The main controller: handles clicks, matching logic, timer, GUI, and win state.
# =============================================================================
class MemoryGame:
    # ─── Color Palette (Soft Pastel Pink + Lavender Theme) ───────────────────
    BG_COLOR        = "#F9F0FF"   # Light lavender-white background
    TITLE_BG        = "#E8D5F5"   # Soft lavender title bar
    TITLE_FG        = "#7B4FA6"   # Deep purple title text
    CARD_BG         = "#F5C6E0"   # Pastel pink card face
    CARD_BACK_BG    = "#D8B4F8"   # Lavender card back
    MATCHED_BG      = "#B5EAD7"   # Soft mint green for matched cards
    BUTTON_BG       = "#C9A8E0"   # Lavender restart button
    BUTTON_FG       = "#4A235A"   # Dark purple button text
    STATS_BG        = "#F0E6FF"   # Very light lavender stats bar
    STATS_FG        = "#5A3A7A"   # Medium purple stats text
    BORDER_COLOR    = "#D8A8E8"   # Soft pink-purple border

    def __init__(self, root):
        """
        Initialize the full game: window, board, player, and GUI.

        Args:
            root (tk.Tk): The root Tkinter window
        """
        self.root = root
        self.root.title("✨ Memory Matching Card Game ✨")
        self.root.configure(bg=self.BG_COLOR)
        self.root.resizable(False, False)

        # ── Game Objects ──────────────────────────────────────────────────────
        self.board = Board(images_folder="images")  # Manages the 4x4 card grid
        self.player = Player()                       # Tracks score and moves

        # ── Game State Variables ──────────────────────────────────────────────
        self.first_card = None       # First card flipped in current turn
        self.second_card = None      # Second card flipped in current turn
        self.can_click = True        # Prevents clicks during the "flip back" delay
        self.matches_found = 0       # Number of pairs matched so far (max 8)

        # ── Timer Variables ───────────────────────────────────────────────────
        self.elapsed_seconds = 0     # Seconds since game started
        self.timer_running = False   # Whether the timer is currently ticking
        self.timer_job = None        # Reference to the scheduled timer callback

        # ── Build the GUI ─────────────────────────────────────────────────────
        self._build_gui()

        # ── Start a Fresh Game ────────────────────────────────────────────────
        self._start_game()

    # ─────────────────────────────────────────────────────────────────────────
    # GUI CONSTRUCTION
    # ─────────────────────────────────────────────────────────────────────────

    def _build_gui(self):
        """Build all GUI sections: title bar, stats bar, card grid, and footer."""
        self._build_title_bar()
        self._build_stats_bar()
        self._build_card_grid()
        self._build_footer()

    def _build_title_bar(self):
        """Create the decorative title banner at the top of the window."""
        title_frame = tk.Frame(self.root, bg=self.TITLE_BG, pady=12)
        title_frame.pack(fill=tk.X)

        tk.Label(
            title_frame,
            text="✨ Memory Matching Game ✨",
            font=("Georgia", 22, "bold"),
            bg=self.TITLE_BG,
            fg=self.TITLE_FG
        ).pack()

        tk.Label(
            title_frame,
            text="Find all matching pairs to win!",
            font=("Georgia", 11, "italic"),
            bg=self.TITLE_BG,
            fg="#9B72CF"
        ).pack()

    def _build_stats_bar(self):
        """Create the stats bar showing Moves, Score, and Timer."""
        stats_frame = tk.Frame(self.root, bg=self.STATS_BG, pady=8,
                               highlightbackground=self.BORDER_COLOR,
                               highlightthickness=1)
        stats_frame.pack(fill=tk.X, padx=10, pady=(6, 0))

        # Moves Counter
        moves_frame = tk.Frame(stats_frame, bg=self.STATS_BG)
        moves_frame.pack(side=tk.LEFT, expand=True)
        tk.Label(moves_frame, text="🎯 Moves", font=("Georgia", 10, "bold"),
                 bg=self.STATS_BG, fg=self.STATS_FG).pack()
        self.moves_label = tk.Label(moves_frame, text="0",
                                    font=("Georgia", 16, "bold"),
                                    bg=self.STATS_BG, fg=self.TITLE_FG)
        self.moves_label.pack()

        # Divider
        tk.Frame(stats_frame, bg=self.BORDER_COLOR, width=2).pack(
            side=tk.LEFT, fill=tk.Y, padx=10)

        # Score Counter
        score_frame = tk.Frame(stats_frame, bg=self.STATS_BG)
        score_frame.pack(side=tk.LEFT, expand=True)
        tk.Label(score_frame, text="⭐ Score", font=("Georgia", 10, "bold"),
                 bg=self.STATS_BG, fg=self.STATS_FG).pack()
        self.score_label = tk.Label(score_frame, text="0",
                                    font=("Georgia", 16, "bold"),
                                    bg=self.STATS_BG, fg=self.TITLE_FG)
        self.score_label.pack()

        # Divider
        tk.Frame(stats_frame, bg=self.BORDER_COLOR, width=2).pack(
            side=tk.LEFT, fill=tk.Y, padx=10)

        # Timer Display
        timer_frame = tk.Frame(stats_frame, bg=self.STATS_BG)
        timer_frame.pack(side=tk.LEFT, expand=True)
        tk.Label(timer_frame, text="⏱ Time", font=("Georgia", 10, "bold"),
                 bg=self.STATS_BG, fg=self.STATS_FG).pack()
        self.timer_label = tk.Label(timer_frame, text="00:00",
                                    font=("Georgia", 16, "bold"),
                                    bg=self.STATS_BG, fg=self.TITLE_FG)
        self.timer_label.pack()

    def _build_card_grid(self):
        """
        Create the 4x4 grid of card buttons.
        Each button represents one card and is bound to _on_card_click().
        """
        self.grid_frame = tk.Frame(self.root, bg=self.BG_COLOR, padx=14, pady=14)
        self.grid_frame.pack()

        # We'll populate the buttons after loading images in _start_game()

    def _build_footer(self):
        """Create the footer area with the Restart button."""
        footer_frame = tk.Frame(self.root, bg=self.BG_COLOR, pady=10)
        footer_frame.pack(fill=tk.X)

        restart_btn = tk.Button(
            footer_frame,
            text="🔄  Restart Game",
            font=("Georgia", 12, "bold"),
            bg=self.BUTTON_BG,
            fg=self.BUTTON_FG,
            activebackground="#B58FD0",
            activeforeground=self.BUTTON_FG,
            relief=tk.FLAT,
            padx=20, pady=8,
            cursor="hand2",
            command=self._restart_game
        )
        restart_btn.pack()

    # ─────────────────────────────────────────────────────────────────────────
    # GAME SETUP
    # ─────────────────────────────────────────────────────────────────────────

    def _start_game(self):
        """
        Set up a complete new game:
        - Reset player stats
        - Create and shuffle cards
        - Load images
        - Render the card buttons on the grid
        - Start the timer
        """
        # Reset game state
        self.first_card = None
        self.second_card = None
        self.can_click = True
        self.matches_found = 0

        # Reset player counters
        self.player.reset()
        self._update_stats_display()

        # Reset and restart the timer
        self._stop_timer()
        self.elapsed_seconds = 0
        self.timer_label.config(text="00:00")

        # Prepare the board: create cards and load all images
        self.board.load_card_back()
        self.board.create_and_shuffle_cards()
        self.board.load_card_images()

        # Clear any old buttons in the grid frame
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        # Create a button for each card in the 4x4 grid
        for row in range(4):
            for col in range(4):
                card = self.board.get_card(row, col)
                self._create_card_button(card, row, col)

        # Start the countdown timer
        self._start_timer()

    def _create_card_button(self, card, row, col):
        """
        Create a Tkinter Button for a single card and place it in the grid.

        Args:
            card (Card): The Card object
            row (int): Grid row
            col (int): Grid column
        """
        btn = tk.Button(
            self.grid_frame,
            image=self.board.card_back_image,  # Show back of card initially
            bg=self.CARD_BACK_BG,
            activebackground=self.CARD_BACK_BG,
            relief=tk.RAISED,
            bd=3,
            cursor="hand2",
            width=100, height=100,
            # Use default argument trick to capture card reference in lambda
            command=lambda c=card: self._on_card_click(c)
        )
        btn.grid(row=row, column=col, padx=5, pady=5)

        # Store the button reference inside the Card object
        card.button = btn

    # ─────────────────────────────────────────────────────────────────────────
    # CLICK & MATCHING LOGIC
    # ─────────────────────────────────────────────────────────────────────────

    def _on_card_click(self, card):
        """
        Handle a card click event.

        Rules:
        - Ignore clicks if animation/delay is in progress (can_click = False)
        - Ignore clicks on already-matched or already-flipped cards
        - First click: flip the card face-up and store as first_card
        - Second click: flip the card, store as second_card, then check match

        Args:
            card (Card): The card that was clicked
        """
        # Block clicks during the "flip-back" delay or if game is locked
        if not self.can_click:
            return

        # Ignore clicks on cards that are already matched
        if card.is_matched:
            return

        # Ignore clicks on the first card that was already flipped this turn
        if card is self.first_card:
            return

        # Flip this card face-up (show its image)
        self._flip_card_face_up(card)

        # ── First Card Selection ──────────────────────────────────────────────
        if self.first_card is None:
            # No card flipped yet this turn — this becomes the first card
            self.first_card = card
            return

        # ── Second Card Selection ─────────────────────────────────────────────
        self.second_card = card

        # Count this as one full move (a pair of flips)
        self.player.increment_moves()
        self._update_stats_display()

        # Lock further clicks while we process the match
        self.can_click = False

        # Check if the two flipped cards are a matching pair
        self._check_match()

    def _flip_card_face_up(self, card):
        """
        Display the card's face image on its button.

        Args:
            card (Card): The card to reveal
        """
        card.is_flipped = True
        card.button.config(
            image=card.photo_image,
            bg=self.CARD_BG,
            activebackground=self.CARD_BG
        )

    def _flip_card_face_down(self, card):
        """
        Display the card back image on its button (hide the face).

        Args:
            card (Card): The card to hide
        """
        card.is_flipped = False
        card.button.config(
            image=self.board.card_back_image,
            bg=self.CARD_BACK_BG,
            activebackground=self.CARD_BACK_BG
        )

    def _check_match(self):
        """
        Compare the two currently flipped cards.

        - If they have the same image → it's a match!
        - If not → schedule a delay then flip both back over
        """
        if self.first_card.image_name == self.second_card.image_name:
            # ✅ It's a match!
            self._handle_match()
        else:
            # ❌ Not a match — wait 900ms then flip both cards back
            self.root.after(900, self._handle_no_match)

    def _handle_match(self):
        """
        Mark both cards as matched, update score, and check for win condition.
        """
        # Mark both cards as permanently matched
        self.first_card.is_matched = True
        self.second_card.is_matched = True

        # Style matched cards with a green background to indicate success
        self.first_card.button.config(bg=self.MATCHED_BG, activebackground=self.MATCHED_BG)
        self.second_card.button.config(bg=self.MATCHED_BG, activebackground=self.MATCHED_BG)

        # Award a point to the player
        self.player.increment_score()
        self.matches_found += 1
        self._update_stats_display()

        # Reset card selection for the next turn
        self.first_card = None
        self.second_card = None
        self.can_click = True

        # Check if all 8 pairs have been found → game over!
        if self.matches_found == 8:
            self._handle_win()

    def _handle_no_match(self):
        """
        Flip both cards back face-down and allow the player to try again.
        Called after the brief delay following a failed match attempt.
        """
        # Hide both cards again
        self._flip_card_face_down(self.first_card)
        self._flip_card_face_down(self.second_card)

        # Clear card selection for the next turn
        self.first_card = None
        self.second_card = None

        # Restore click ability
        self.can_click = True

    # ─────────────────────────────────────────────────────────────────────────
    # STATS DISPLAY UPDATE
    # ─────────────────────────────────────────────────────────────────────────

    def _update_stats_display(self):
        """Refresh the Moves and Score labels to reflect current player data."""
        self.moves_label.config(text=str(self.player.moves))
        self.score_label.config(text=str(self.player.score))

    # ─────────────────────────────────────────────────────────────────────────
    # TIMER LOGIC
    # ─────────────────────────────────────────────────────────────────────────

    def _start_timer(self):
        """Begin the timer, ticking every second."""
        self.timer_running = True
        self._tick_timer()

    def _tick_timer(self):
        """
        Increment elapsed time by 1 second and update the timer label.
        Schedules itself to run again after 1000ms if timer is still running.
        """
        if self.timer_running:
            self.elapsed_seconds += 1

            # Format as MM:SS
            minutes = self.elapsed_seconds // 60
            seconds = self.elapsed_seconds % 60
            time_str = f"{minutes:02d}:{seconds:02d}"
            self.timer_label.config(text=time_str)

            # Schedule the next tick 1 second from now
            self.timer_job = self.root.after(1000, self._tick_timer)

    def _stop_timer(self):
        """Stop the timer from ticking (used on win or restart)."""
        self.timer_running = False
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

    # ─────────────────────────────────────────────────────────────────────────
    # WIN CONDITION
    # ─────────────────────────────────────────────────────────────────────────

    def _handle_win(self):
        """
        Called when all 8 pairs are matched.
        Stops the timer and shows a congratulatory popup window.
        """
        self._stop_timer()

        # Format the final time nicely
        minutes = self.elapsed_seconds // 60
        seconds = self.elapsed_seconds % 60
        time_str = f"{minutes:02d}:{seconds:02d}"

        # Build the win message
        win_message = (
            f"🎉 Congratulations! You Won! 🎉\n\n"
            f"⭐ Final Score:  {self.player.score} / 8\n"
            f"🎯 Total Moves:  {self.player.moves}\n"
            f"⏱ Time Taken:   {time_str}\n\n"
            f"Would you like to play again?"
        )

        # Show the win dialog — ask if they want to restart
        play_again = messagebox.askyesno(
            title="🌟 You Won! 🌟",
            message=win_message,
            icon=messagebox.INFO
        )

        if play_again:
            self._restart_game()
        else:
            self.root.quit()

    # ─────────────────────────────────────────────────────────────────────────
    # RESTART FUNCTIONALITY
    # ─────────────────────────────────────────────────────────────────────────

    def _restart_game(self):
        """
        Restart the game from scratch:
        - Stop the current timer
        - Reset all state
        - Re-shuffle and re-render the board
        """
        self._stop_timer()
        self._start_game()


# =============================================================================
# ENTRY POINT
# This block runs only when the script is executed directly (not imported).
# =============================================================================
if __name__ == "__main__":
    # Try importing Pillow — it's required for image handling
    try:
        from PIL import Image, ImageTk
    except ImportError:
        print("=" * 60)
        print("ERROR: Pillow library is not installed!")
        print("Please run:  pip install Pillow")
        print("=" * 60)
        exit(1)

    # Create the main Tkinter window
    root = tk.Tk()

    # Center the window on screen
    window_width = 500
    window_height = 680
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Launch the game
    game = MemoryGame(root)

    # Start the Tkinter event loop (keeps the window open and responsive)
    root.mainloop()
