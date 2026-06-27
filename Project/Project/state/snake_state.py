"""
snake_state.py — State for the Snake Game.
"""

import reflex as rx
import random
import asyncio
from Project.state.user_state import UserState

GRID_SIZE = 15

class SnakeState(rx.State):
    snake: list[int] = [112, 111, 110] # e.g. 7*15+7, 7*15+6, 7*15+5
    food: int = 48 # 3*15+3
    direction: str = "RIGHT"
    score: int = 0
    game_over: bool = False
    is_playing: bool = False
    ai_message: str = "Ready to play Snake? Use the controls below!"
    
    def start_game(self):
        self.snake = [112, 111, 110]
        self.direction = "RIGHT"
        self.score = 0
        self.game_over = False
        self.is_playing = True
        self._spawn_food()
        self.ai_message = "Here we go! Good luck!"
        return SnakeState.tick
        
    def stop_game(self):
        self.is_playing = False

    async def tick(self):
        if not self.is_playing or self.game_over:
            return
            
        # Calculate new head
        head_idx = self.snake[0]
        head_x = head_idx // GRID_SIZE
        head_y = head_idx % GRID_SIZE
        
        if self.direction == "UP":
            head_x -= 1
        elif self.direction == "DOWN":
            head_x += 1
        elif self.direction == "LEFT":
            head_y -= 1
        elif self.direction == "RIGHT":
            head_y += 1
                    
        # Check wall collision
        if head_x < 0 or head_x >= GRID_SIZE or head_y < 0 or head_y >= GRID_SIZE:
            self.game_over = True
            self.is_playing = False
            self.ai_message = "Ouch! You hit the wall."
            yield
            return
            
        new_head_idx = head_x * GRID_SIZE + head_y
        
        # Check self collision
        if new_head_idx in self.snake:
            self.game_over = True
            self.is_playing = False
            self.ai_message = "Oh no, you bit your own tail!"
            yield
            return
            
        self.snake.insert(0, new_head_idx)
        
        # Check food
        if new_head_idx == self.food:
            self.score += 10
            self._spawn_food()
            phrases = ["Yum!", "Delicious!", "Keep it going!", "Nice!"]
            self.ai_message = random.choice(phrases)
        else:
            self.snake.pop()

        if self.is_playing:
            yield
            await asyncio.sleep(0.3)
            yield SnakeState.tick

    def _spawn_food(self):
        while True:
            idx = random.randint(0, GRID_SIZE * GRID_SIZE - 1)
            if idx not in self.snake:
                self.food = idx
                break

    def change_direction(self, new_dir: str):
        opposites = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        if self.direction != opposites.get(new_dir):
            self.direction = new_dir

    def handle_key(self, key: str):
        if key in ["ArrowUp", "w", "W", "up"]:
            self.change_direction("UP")
        elif key in ["ArrowDown", "s", "S", "down"]:
            self.change_direction("DOWN")
        elif key in ["ArrowLeft", "a", "A", "left"]:
            self.change_direction("LEFT")
        elif key in ["ArrowRight", "d", "D", "right"]:
            self.change_direction("RIGHT")
