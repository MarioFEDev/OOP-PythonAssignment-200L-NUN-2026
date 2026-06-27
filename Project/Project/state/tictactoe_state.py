"""
tictactoe_state.py — State for the Tic-Tac-Toe game.
"""

import reflex as rx
import random
import asyncio
from Project.state.user_state import UserState

class TicTacToeState(rx.State):
    board: list[str] = [""] * 9
    game_over: bool = False
    winner: str = ""
    ai_message: str = "Let's play Tic-Tac-Toe! You go first as X."

    def start_game(self):
        self.board = [""] * 9
        self.game_over = False
        self.winner = ""
        self.ai_message = "Your move, X!"

    async def make_move(self, index: int):
        if self.game_over or self.board[index] != "":
            return

        # User move
        self.board[index] = "X"
        
        user_state = await self.get_state(UserState)
        name = user_state.user_name if user_state.user_name else "buddy"
        
        if self._check_win("X"):
            self.game_over = True
            self.winner = "X"
            self.ai_message = f"You won, {name}! Good job!"
            return
            
        if "" not in self.board:
            self.game_over = True
            self.winner = "Draw"
            self.ai_message = "It's a draw!"
            return
            
        # Give the AI a moment to think to feel more human
        yield
        await asyncio.sleep(0.7)
            
        # AI move
        self._ai_turn(name)
        
        if self._check_win("O"):
            self.game_over = True
            self.winner = "O"
            # ai_message set in _ai_turn
            return
            
        if "" not in self.board:
            self.game_over = True
            self.winner = "Draw"
            self.ai_message = "It's a draw!"

    def _ai_turn(self, name: str):
        # 1. Check if we need to block X
        block_idx = self._find_blocking_move("X")
        if block_idx != -1:
            self.board[block_idx] = "O"
            self.ai_message = random.choice([
                "Not so fast!",
                "I saw that!",
                "Blocked you!",
                f"Nice try, {name}!"
            ])
        else:
            # 2. Pick random
            empty_spots = [i for i, val in enumerate(self.board) if val == ""]
            if empty_spots:
                idx = random.choice(empty_spots)
                self.board[idx] = "O"
                self.ai_message = random.choice([
                    "My turn!",
                    "Hmm, let's see...",
                    "I'll go here.",
                    "Your move!"
                ])
                
        # Check if AI just won
        if self._check_win("O"):
            self.ai_message = random.choice([
                "I win!",
                "Gotcha!",
                f"Better luck next time, {name}!"
            ])

    def _find_blocking_move(self, player: str) -> int:
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], # cols
            [0, 4, 8], [2, 4, 6]             # diagonals
        ]
        for line in lines:
            vals = [self.board[i] for i in line]
            if vals.count(player) == 2 and vals.count("") == 1:
                return line[vals.index("")]
        return -1
        
    def _check_win(self, player: str) -> bool:
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for line in lines:
            if self.board[line[0]] == player and self.board[line[1]] == player and self.board[line[2]] == player:
                return True
        return False
