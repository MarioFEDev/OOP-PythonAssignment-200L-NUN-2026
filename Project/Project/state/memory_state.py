"""
memory_state.py — State for the Memory Match Game.
"""

import reflex as rx
import random
import asyncio
from Project.state.user_state import UserState

# 8 distinct emojis for pairs
ICONS = ["🍎", "🐛", "🚗", "🐶", "🌸", "🌙", "⭐", "☀️"]

class MemoryState(rx.State):
    # A list of dictionaries representing the cards
    # Structure: {"id": int, "icon": str, "is_flipped": bool, "is_matched": bool}
    cards: list[dict] = []
    
    flipped_indices: list[int] = []
    is_processing: bool = False
    moves: int = 0
    matches: int = 0
    game_over: bool = False
    ai_message: str = "Ready to test your memory?"
    
    def start_game(self):
        """Initialize and shuffle the board."""
        self.moves = 0
        self.matches = 0
        self.game_over = False
        self.is_processing = False
        self.flipped_indices = []
        self.ai_message = "Let's find those pairs!"
        
        # Create pairs
        deck = ICONS * 2
        random.shuffle(deck)
        
        self.cards = [
            {"id": i, "icon": icon, "is_flipped": False, "is_matched": False}
            for i, icon in enumerate(deck)
        ]

    async def flip_card(self, index: int):
        """Handle a card click."""
        if self.is_processing or self.game_over:
            return
            
        card = self.cards[index]
        if card["is_flipped"] or card["is_matched"]:
            return
            
        # Flip the card
        self.cards[index]["is_flipped"] = True
        self.flipped_indices.append(index)
        
        user_state = await self.get_state(UserState)
        name = user_state.user_name if user_state.user_name else "buddy"
        
        # If two cards are flipped, check for match
        if len(self.flipped_indices) == 2:
            self.is_processing = True
            yield # Update UI to show the second flipped card
            
            await asyncio.sleep(0.8) # Wait for player to see both cards
            
            idx1, idx2 = self.flipped_indices
            if self.cards[idx1]["icon"] == self.cards[idx2]["icon"]:
                # Match
                self.cards[idx1]["is_matched"] = True
                self.cards[idx2]["is_matched"] = True
                self.matches += 1
                
                phrases = [
                    f"Great memory, {name}!",
                    "You found a match!",
                    "Spot on!",
                    "Nice one!"
                ]
                self.ai_message = random.choice(phrases)
                
                if self.matches == len(ICONS):
                    self.game_over = True
                    self.ai_message = f"Incredible! You finished in {self.moves + 1} moves!"
            else:
                # No match
                self.cards[idx1]["is_flipped"] = False
                self.cards[idx2]["is_flipped"] = False
                
                phrases = [
                    "Oops, try again!",
                    "Not quite!",
                    "Those don't match.",
                    f"Keep trying, {name}!"
                ]
                self.ai_message = random.choice(phrases)
                
            self.flipped_indices = []
            self.moves += 1
            self.is_processing = False
