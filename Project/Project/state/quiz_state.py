"""
quiz_state.py — State for the Quiz Game.
"""

import reflex as rx
import httpx
import random
import html
from Project.state.user_state import UserState

class QuizState(rx.State):
    questions: list[dict] = []
    current_index: int = 0
    score: int = 0
    game_over: bool = False
    is_loading: bool = False
    ai_message: str = "Welcome to the Daily Quiz! Ready to play?"
    
    _correct_answer: str = ""
    options: list[str] = []
    current_question_text: str = ""

    async def start_game(self):
        self.is_loading = True
        self.game_over = False
        self.score = 0
        self.current_index = 0
        self.ai_message = "Let's see what you've got!"
        yield
        
        try:
            async with httpx.AsyncClient(timeout=1.5) as client:
                response = await client.get("https://opentdb.com/api.php?amount=5&type=multiple")
                response.raise_for_status()
                data = response.json()
                
            if data.get("response_code") == 0:
                self.questions = data["results"]
                self._load_question()
            else:
                raise ValueError("API returned no results")
        except Exception:
            # Fallback questions if offline or API fails
            self.questions = [
                {
                    "question": "What is the capital of France?",
                    "correct_answer": "Paris",
                    "incorrect_answers": ["London", "Berlin", "Madrid"]
                },
                {
                    "question": "Which planet is known as the Red Planet?",
                    "correct_answer": "Mars",
                    "incorrect_answers": ["Venus", "Jupiter", "Saturn"]
                },
                {
                    "question": "Who painted the Mona Lisa?",
                    "correct_answer": "Leonardo da Vinci",
                    "incorrect_answers": ["Vincent van Gogh", "Pablo Picasso", "Michelangelo"]
                },
                {
                    "question": "What is the largest ocean on Earth?",
                    "correct_answer": "Pacific Ocean",
                    "incorrect_answers": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean"]
                },
                {
                    "question": "What is the chemical symbol for Gold?",
                    "correct_answer": "Au",
                    "incorrect_answers": ["Ag", "Fe", "Cu"]
                }
            ]
            self._load_question()
            
        self.is_loading = False

    def _load_question(self):
        if self.current_index < len(self.questions):
            q = self.questions[self.current_index]
            self.current_question_text = html.unescape(q["question"])
            self._correct_answer = html.unescape(q["correct_answer"])
            
            opts = [html.unescape(opt) for opt in q["incorrect_answers"]]
            opts.append(self._correct_answer)
            random.shuffle(opts)
            self.options = opts
        else:
            self.game_over = True
            self.ai_message = f"Game Over! You scored {self.score} out of {len(self.questions)}."

    async def submit_answer(self, answer: str):
        user_state = await self.get_state(UserState)
        name = user_state.user_name if user_state.user_name else "buddy"
        
        if answer == self._correct_answer:
            self.score += 1
            phrases = [
                f"That's right, {name}!",
                "Spot on!",
                "Excellent work!",
                f"You got it, {name}!"
            ]
            self.ai_message = random.choice(phrases)
        else:
            phrases = [
                f"Not quite! The correct answer was {self._correct_answer}.",
                f"Oops! It was actually {self._correct_answer}.",
                f"Nice try {name}, but the answer is {self._correct_answer}."
            ]
            self.ai_message = random.choice(phrases)
            
        self.current_index += 1
        self._load_question()
