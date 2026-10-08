import random
import pygame
from game.text_box import TextBox


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.min_guess = 1
        self.max_guess = 100
        self.guess_history = []
        self.feedback_msg = "Enter a number between 1 and 100"
        self.feedback_color = (220, 220, 220)
        self.game_won = False

        self.input_box = TextBox(width // 2 - 110, 150, 120, 48)
        self.submit_btn = pygame.Rect(width // 2 + 25, 150, 100, 48)

        self.font_title = pygame.font.SysFont(None, 42)
        self.font_medium = pygame.font.SysFont(None, 28)
        self.font_btn = pygame.font.SysFont(None, 26)
        self.history_title_font = pygame.font.SysFont(None, 24)
        self.history_font = pygame.font.SysFont(None, 22)

    def submit_guess(self):
        if self.game_won:
            return

        if not self.input_box.text:
            self.feedback_msg = "Please enter a number before submitting."
            self.feedback_color = (240, 190, 80)
            return

        guess = int(self.input_box.text)

        self.attempts += 1
        self.input_box.clear()

        if guess < self.secret_number:
            self.min_guess = max(self.min_guess, guess + 1)
            self.feedback_msg = f"TOO LOW! (Guess was {guess})"
            self.feedback_color = (80, 160, 240)
            self.guess_history.append((guess, "TOO LOW (UP)", (80, 160, 240)))
        elif guess > self.secret_number:
            self.max_guess = min(self.max_guess, guess - 1)
            self.feedback_msg = f"TOO HIGH! (Guess was {guess})"
            self.feedback_color = (240, 100, 80)
            self.guess_history.append((guess, "TOO HIGH (DOWN)", (240, 100, 80)))
        else:
            self.feedback_msg = f"CORRECT! Found in {self.attempts} attempts."
            self.feedback_color = (80, 220, 90)
            self.guess_history.append((guess, "CORRECT", (80, 220, 90)))
            self.game_won = True

    def reset(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.min_guess = 1
        self.max_guess = 100
        self.guess_history.clear()
        self.feedback_msg = "Enter a number between 1 and 100"
        self.feedback_color = (220, 220, 220)
        self.game_won = False
        self.input_box.clear()

    def handle_event(self, event):
        self.input_box.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.submit_guess()
            elif event.key == pygame.K_r and self.game_won:
                self.reset()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.submit_btn.collidepoint(event.pos):
                self.submit_guess()

    def update(self):
        pass

    def render(self, screen):
        screen.fill((30, 34, 42))

        title_surf = self.font_title.render("Number Guessing Arena", True, (245, 245, 245))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 35))

        attempts_surf = self.font_medium.render(f"Attempts: {self.attempts}", True, (180, 185, 195))
        screen.blit(attempts_surf, (self.width // 2 - attempts_surf.get_width() // 2, 95))

        range_surf = self.font_medium.render(
            f"Possible range: {self.min_guess} - {self.max_guess}",
            True,
            (180, 210, 190),
        )
        screen.blit(range_surf, (self.width // 2 - range_surf.get_width() // 2, 118))

        self.input_box.render(screen)

        pygame.draw.rect(screen, (50, 150, 80), self.submit_btn, border_radius=6)
        pygame.draw.rect(screen, (220, 220, 220), self.submit_btn, width=2, border_radius=6)
        btn_text = self.font_btn.render("SUBMIT", True, (255, 255, 255))
        screen.blit(
            btn_text,
            (self.submit_btn.centerx - btn_text.get_width() // 2, self.submit_btn.centery - btn_text.get_height() // 2),
        )

        feedback_surf = self.font_medium.render(self.feedback_msg, True, self.feedback_color)
        screen.blit(feedback_surf, (self.width // 2 - feedback_surf.get_width() // 2, 235))

        self.render_guess_history(screen)

        if self.game_won:
            restart_surf = self.font_medium.render("Press [R] to Start a New Game", True, (255, 220, 80))
            screen.blit(restart_surf, (self.width // 2 - restart_surf.get_width() // 2, 295))

    def render_guess_history(self, screen):
        panel = pygame.Rect(self.width - 165, 80, 155, 270)
        pygame.draw.rect(screen, (39, 44, 54), panel, border_radius=8)
        pygame.draw.rect(screen, (100, 110, 125), panel, width=1, border_radius=8)

        title = self.history_title_font.render("Recent Guesses", True, (245, 245, 245))
        screen.blit(title, (panel.centerx - title.get_width() // 2, panel.y + 12))

        recent_guesses = self.guess_history[-8:]
        for index, (guess, result, color) in enumerate(reversed(recent_guesses)):
            row_text = self.history_font.render(f"{guess} - {result}", True, color)
            screen.blit(row_text, (panel.x + 10, panel.y + 44 + index * 26))
