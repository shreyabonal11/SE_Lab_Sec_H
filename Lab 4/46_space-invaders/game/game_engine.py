import pygame
import random
from .player import Player
from .enemy import EnemyGrid
from .bullet import Bullet

# Game Engine

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (220, 60, 60)


class GameEngine:
    def __init__(self, width, height, difficulty="Medium"):
        self.width = width
        self.height = height
        self.difficulty = difficulty

        # Initialize sound system
        pygame.mixer.init()

        # Create sound effects
        self.fire_sound = self.create_sound(600, 80)
        self.enemy_destroyed_sound = self.create_sound(300, 120)
        self.game_over_sound = self.create_sound(150, 400)

        self.player = Player(
            width // 2 - 20,
            height - 50,
            40,
            20
        )

        # Difficulty settings
        difficulty_settings = {
            "Easy": {
                "enemy_speed": 1.0,
                "fire_chance": 0.005
            },
            "Medium": {
                "enemy_speed": 1.5,
                "fire_chance": 0.01
            },
            "Hard": {
                "enemy_speed": 2.5,
                "fire_chance": 0.02
            }
        }

        settings = difficulty_settings[difficulty]

        self.enemy_grid = EnemyGrid(
            width,
            speed=settings["enemy_speed"]
        )

        self.enemy_fire_chance = settings["fire_chance"]

        self.player_bullets = []
        self.enemy_bullets = []

        self._shoot_cooldown = 0

        self.score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        self.game_over = False
        self.game_over_sound_played = False

    def create_sound(self, frequency, duration):
        """Create a simple sound effect."""

        sample_rate = 44100
        samples = int(sample_rate * duration / 1000)

        sound_buffer = bytearray()

        for i in range(samples):
            value = int(
                127 * (
                    1 + 0.5 *
                    random.choice([-1, 1])
                )
            )

            sound_buffer.append(value)

        sound = pygame.mixer.Sound(
            buffer=bytes(sound_buffer)
        )

        return sound

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if self.game_over:
                return

            if event.key == pygame.K_SPACE:

                if self._shoot_cooldown <= 0:

                    bullet_x = (
                        self.player.center_x() - 2
                    )

                    self.player_bullets.append(
                        Bullet(
                            bullet_x,
                            self.player.y,
                            direction=-1
                        )
                    )

                    # Task 4: firing sound
                    self.fire_sound.play()

                    self._shoot_cooldown = 15

    def handle_input(self):

        if self.game_over:
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:

            self.player.move(
                -self.player.speed,
                self.width
            )

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:

            self.player.move(
                self.player.speed,
                self.width
            )

    def update(self):

        if self.game_over:
            return

        if self._shoot_cooldown > 0:
            self._shoot_cooldown -= 1

        # Move enemies
        self.enemy_grid.move()

        # Enemy shooting
        for enemy in self.enemy_grid.alive_enemies():

            if random.random() < self.enemy_fire_chance:

                bullet_x = (
                    enemy.x + enemy.width // 2
                )

                self.enemy_bullets.append(
                    Bullet(
                        bullet_x,
                        enemy.y + enemy.height,
                        direction=1
                    )
                )

        # Move player bullets
        for bullet in self.player_bullets:
            bullet.move()

        # Move enemy bullets
        for bullet in self.enemy_bullets:
            bullet.move()

        # Remove off-screen bullets
        self.player_bullets = [
            b for b in self.player_bullets
            if not b.off_screen(self.height)
        ]

        self.enemy_bullets = [
            b for b in self.enemy_bullets
            if not b.off_screen(self.height)
        ]

        # Player bullet collision
        remaining_bullets = []

        for bullet in self.player_bullets:

            hit_enemy = False

            for enemy in self.enemy_grid.alive_enemies():

                if bullet.rect().colliderect(enemy.rect()):

                    enemy.alive = False
                    self.score += 1
                    hit_enemy = True

                    # Task 4: enemy destroyed sound
                    self.enemy_destroyed_sound.play()

                    break

            if not hit_enemy:
                remaining_bullets.append(bullet)

        self.player_bullets = remaining_bullets

        # Enemy bullet hits player
        for bullet in self.enemy_bullets:

            if bullet.rect().colliderect(
                self.player.rect()
            ):

                self.game_over = True
                break

        # Enemies reach bottom
        if self.enemy_grid.reached_bottom(
            self.player.y
        ):
            self.game_over = True

        # All enemies destroyed
        if not self.enemy_grid.alive_enemies():
            self.game_over = True

        # Task 4: game-over sound
        if self.game_over and not self.game_over_sound_played:

            self.game_over_sound.play()
            self.game_over_sound_played = True

    def render(self, screen):

        # Player
        pygame.draw.rect(
            screen,
            GREEN,
            self.player.rect()
        )

        # Enemies
        for enemy in self.enemy_grid.alive_enemies():

            pygame.draw.rect(
                screen,
                WHITE,
                enemy.rect()
            )

        # Player bullets
        for bullet in self.player_bullets:

            pygame.draw.rect(
                screen,
                WHITE,
                bullet.rect()
            )

        # Enemy bullets
        for bullet in self.enemy_bullets:

            pygame.draw.rect(
                screen,
                RED,
                bullet.rect()
            )

        # Score
        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            WHITE
        )

        screen.blit(
            score_text,
            (10, 10)
        )

        # Game Over screen
        if self.game_over:

            game_over_font = pygame.font.SysFont(
                "Arial",
                50
            )

            final_score_font = pygame.font.SysFont(
                "Arial",
                30
            )

            game_over_text = game_over_font.render(
                "GAME OVER",
                True,
                WHITE
            )

            final_score_text = final_score_font.render(
                f"Final Score: {self.score}",
                True,
                WHITE
            )

            screen.blit(
                game_over_text,
                (
                    self.width // 2
                    - game_over_text.get_width() // 2,
                    self.height // 2 - 100
                )
            )

            screen.blit(
                final_score_text,
                (
                    self.width // 2
                    - final_score_text.get_width() // 2,
                    self.height // 2 - 40
                )
            )