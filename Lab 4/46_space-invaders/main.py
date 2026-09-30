import pygame
from game.game_engine import GameEngine

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 700

SCREEN = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "Space Invaders - Pygame Version"
)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Clock
clock = pygame.time.Clock()
FPS = 60


def show_difficulty_menu():

    font = pygame.font.SysFont(
        "Arial",
        35
    )

    title_font = pygame.font.SysFont(
        "Arial",
        45
    )

    while True:

        SCREEN.fill(BLACK)

        title = title_font.render(
            "SELECT DIFFICULTY",
            True,
            WHITE
        )

        easy = font.render(
            "1 - Easy",
            True,
            WHITE
        )

        medium = font.render(
            "2 - Medium",
            True,
            WHITE
        )

        hard = font.render(
            "3 - Hard",
            True,
            WHITE
        )

        exit_text = font.render(
            "4 - Exit",
            True,
            WHITE
        )

        SCREEN.blit(
            title,
            (
                WIDTH // 2 - title.get_width() // 2,
                100
            )
        )

        SCREEN.blit(
            easy,
            (
                WIDTH // 2 - easy.get_width() // 2,
                220
            )
        )

        SCREEN.blit(
            medium,
            (
                WIDTH // 2 - medium.get_width() // 2,
                280
            )
        )

        SCREEN.blit(
            hard,
            (
                WIDTH // 2 - hard.get_width() // 2,
                340
            )
        )

        SCREEN.blit(
            exit_text,
            (
                WIDTH // 2 - exit_text.get_width() // 2,
                400
            )
        )

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:
                    return "Easy"

                elif event.key == pygame.K_2:
                    return "Medium"

                elif event.key == pygame.K_3:
                    return "Hard"

                elif event.key == pygame.K_4:
                    return None


def show_game_over_menu(score):

    font = pygame.font.SysFont(
        "Arial",
        30
    )

    title_font = pygame.font.SysFont(
        "Arial",
        50
    )

    while True:

        SCREEN.fill(BLACK)

        game_over = title_font.render(
            "GAME OVER",
            True,
            WHITE
        )

        score_text = font.render(
            f"Final Score: {score}",
            True,
            WHITE
        )

        replay_text = font.render(
            "Press R to Replay",
            True,
            WHITE
        )

        exit_text = font.render(
            "Press Q to Exit",
            True,
            WHITE
        )

        SCREEN.blit(
            game_over,
            (
                WIDTH // 2
                - game_over.get_width() // 2,
                180
            )
        )

        SCREEN.blit(
            score_text,
            (
                WIDTH // 2
                - score_text.get_width() // 2,
                260
            )
        )

        SCREEN.blit(
            replay_text,
            (
                WIDTH // 2
                - replay_text.get_width() // 2,
                340
            )
        )

        SCREEN.blit(
            exit_text,
            (
                WIDTH // 2
                - exit_text.get_width() // 2,
                400
            )
        )

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    return True

                elif event.key == pygame.K_q:
                    return False


def play_game(difficulty):

    engine = GameEngine(
        WIDTH,
        HEIGHT,
        difficulty
    )

    running = True

    while running:

        SCREEN.fill(BLACK)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            engine.handle_event(event)

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)

        pygame.display.flip()

        clock.tick(FPS)

        # Game over
        if engine.game_over:

            pygame.time.delay(500)

            replay = show_game_over_menu(
                engine.score
            )

            if replay:
                return True

            return False

    return False


def main():

    running = True

    while running:

        difficulty = show_difficulty_menu()

        if difficulty is None:
            break

        running = play_game(
            difficulty
        )

    pygame.quit()


if __name__ == "__main__":
    main()