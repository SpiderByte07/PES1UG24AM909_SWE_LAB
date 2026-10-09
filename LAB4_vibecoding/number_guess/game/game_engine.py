import random
import pygame
from game.text_box import TextBox

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.secret_number = random.randint(1, 100)
        self.max_attempts = 10
        self.attempts = 0
        self.min_guess = 1
        self.max_guess = 100
        self.guess_history = []
        self.feedback_msg = "Enter a number between 1 and 100"
        self.feedback_color = (220, 220, 220)
        self.game_won = False
        self.game_over = False

        # Keep the controls in the left column so the history panel has its own space.
        self.input_box = TextBox(int(width * 0.08), 150, 120, 48)
        self.submit_btn = pygame.Rect(int(width * 0.30), 150, 100, 48)

        self.font_title = pygame.font.SysFont(None, 42)
        self.font_medium = pygame.font.SysFont(None, 28)
        self.font_btn = pygame.font.SysFont(None, 26)

    def submit_guess(self):
        if self.game_won or self.game_over:
            return

        if not self.input_box.text.strip():
            self.feedback_msg = "Please enter a number before submitting."
            self.feedback_color = (240, 190, 80)
            return

        guess = int(self.input_box.text)

        if not self.min_guess <= guess <= self.max_guess:
            self.feedback_msg = f"Guess must be between {self.min_guess} and {self.max_guess}."
            self.feedback_color = (240, 190, 80)
            self.input_box.clear()
            return
        
        self.attempts += 1
        self.input_box.clear()

        if guess < self.secret_number:
            self.min_guess = guess + 1
            self._add_history(guess, "TOO LOW", (80, 160, 240))
            self.feedback_msg = f"TOO LOW! (Guess was {guess})"
            self.feedback_color = (80, 160, 240)
        elif guess > self.secret_number:
            self.max_guess = guess - 1
            self._add_history(guess, "TOO HIGH", (240, 100, 80))
            self.feedback_msg = f"TOO HIGH! (Guess was {guess})"
            self.feedback_color = (240, 100, 80)
        else:
            self._add_history(guess, "CORRECT", (80, 220, 90))
            self.feedback_msg = f"CORRECT! Found in {self.attempts} attempts."
            self.feedback_color = (80, 220, 90)
            self.game_won = True

        if not self.game_won and self.attempts >= self.max_attempts:
            self.game_over = True
            self.feedback_msg = f"GAME OVER! The number was {self.secret_number}."
            self.feedback_color = (240, 100, 80)

    def _add_history(self, guess, result, color):
        self.guess_history.append((guess, result, color))
        self.guess_history = self.guess_history[-5:]

    def reset(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.min_guess = 1
        self.max_guess = 100
        self.guess_history.clear()
        self.feedback_msg = "Enter a number between 1 and 100"
        self.feedback_color = (220, 220, 220)
        self.game_won = False
        self.game_over = False
        self.input_box.clear()

    def handle_event(self, event):
        if not (self.game_won or self.game_over):
            self.input_box.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.submit_guess()
            elif event.key == pygame.K_r and (self.game_won or self.game_over):
                self.reset()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.submit_btn.collidepoint(event.pos):
                self.submit_guess()

    def update(self):
        pass

    def render(self, screen):
        screen.fill((30, 34, 42))

        left_center = int(self.width * 0.31)
        history_left = int(self.width * 0.63)
        panel = pygame.Rect(history_left, 88, self.width - history_left - 18, self.height - 108)
        pygame.draw.rect(screen, (39, 44, 54), panel, border_radius=10)
        pygame.draw.rect(screen, (65, 72, 84), panel, width=1, border_radius=10)

        title_surf = self.font_title.render("Number Guessing Arena", True, (245, 245, 245))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 35))

        attempts_surf = self.font_medium.render(
            f"Attempts: {self.attempts}/{self.max_attempts}", True, (180, 185, 195)
        )
        screen.blit(attempts_surf, (left_center - attempts_surf.get_width() // 2, 95))

        range_surf = self.font_medium.render(
            f"Possible range: {self.min_guess} - {self.max_guess}", True, (180, 185, 195)
        )
        screen.blit(range_surf, (left_center - range_surf.get_width() // 2, 120))
        self.input_box.render(screen)

        pygame.draw.rect(screen, (50, 150, 80), self.submit_btn, border_radius=6)
        pygame.draw.rect(screen, (220, 220, 220), self.submit_btn, width=2, border_radius=6)
        btn_text = self.font_btn.render("SUBMIT", True, (255, 255, 255))
        screen.blit(
            btn_text,
            (self.submit_btn.centerx - btn_text.get_width() // 2, self.submit_btn.centery - btn_text.get_height() // 2),
        )

        history_title = self.font_medium.render("Recent guesses", True, (220, 220, 220))
        screen.blit(history_title, (history_left + 12, 103))
        for index, (guess, result, color) in enumerate(reversed(self.guess_history)):
            history_surf = self.font_btn.render(f"{guess}: {result}", True, color)
            screen.blit(history_surf, (history_left + 12, 143 + index * 34))

        feedback_surf = self.font_medium.render(self.feedback_msg, True, self.feedback_color)
        screen.blit(feedback_surf, (left_center - feedback_surf.get_width() // 2, 225))

        if self.game_won or self.game_over:
            restart_surf = self.font_medium.render("Press [R] to Start a New Game", True, (255, 220, 80))
            screen.blit(restart_surf, (left_center - restart_surf.get_width() // 2, 285))
