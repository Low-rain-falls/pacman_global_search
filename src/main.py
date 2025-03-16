import pygame

# import modules
from board import boards

# import objects
from ghost import Ghost
from player import Player

pygame.init()

# constant
width = 900
height = 1040
PI = 3.14159265358979323846264338327950288419716939937510

# button
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 100
start_button = pygame.Rect(width // 2 - BUTTON_WIDTH // 2, height // 2 - BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT)
exit_button = pygame.Rect(width // 2 - BUTTON_WIDTH // 2, height // 2 + 100, BUTTON_WIDTH, BUTTON_HEIGHT)
levels = [f"Level {i+1}" for i in range(6)]
selected_level = None

# color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


# game global parameter
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("PacMan by team AI")
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font("freesansbold.ttf", 20)
game_board = boards
original_board = [row[:] for row in game_board]

# player object
player = Player(450, 720)

# ghost object
blue_image = pygame.transform.scale(
    pygame.image.load(f"./assets/ghost_images/blue.png"), (30, 30)
)
orange_image = pygame.transform.scale(
    pygame.image.load(f"./assets/ghost_images/orange.png"), (30, 30)
)
pink_image = pygame.transform.scale(
    pygame.image.load(f"./assets/ghost_images/pink.png"), (30, 30)
)
red_image = pygame.transform.scale(
    pygame.image.load(f"./assets/ghost_images/red.png"), (30, 30)
)

# case 1: 60, 60
# case 2: 810, 60
# case 3: 810, 900
# case 4: 60, 900
# case 5: 420, 450

ghosts = [
    Ghost(60, 60, blue_image, 1),
    Ghost(810, 60, pink_image, 2),
    Ghost(60, 900, orange_image, 3),
    Ghost(810, 900, red_image, 4),
]


# functions
# draw game board function
def draw_board(game_board):
    # calculate the coordinate arcording to the size of the game window
    y = 30
    x = 30

    for i in range(len(game_board)):
        for j in range(len(game_board[0])):
            # pygame.draw.rect(window, WHITE, (j * 30, i * 30, 30, 30), 1)
            match game_board[i][j]:
                case 1:
                    pygame.draw.circle(window, WHITE, ((j + 0.5) * x, (i + 0.5) * y), 4)
                case 2:
                    pygame.draw.circle(
                        window, WHITE, ((j + 0.5) * x, (i + 0.5) * y), 10
                    )
                case 3:
                    pygame.draw.line(
                        window,
                        BLUE,
                        ((j + 0.5) * x, i * y),
                        ((j + 0.5) * x, i * y + y),
                        3,
                    )
                case 4:
                    pygame.draw.line(
                        window,
                        BLUE,
                        (j * x, (i + 0.5) * y),
                        (j * x + x, (i + 0.5) * y),
                        3,
                    )
                # the gate
                case 9:
                    pygame.draw.line(
                        window,
                        WHITE,
                        (j * x, (i + 0.5) * y),
                        (j * x + x, (i + 0.5) * y),
                        3,
                    )
                # top right corner
                case 5:
                    pygame.draw.arc(
                        window,
                        BLUE,
                        (((j - 0.5) * x + 2), ((i + 0.5) * y), x, y),
                        0,
                        PI / 2,
                        3,
                    )
                # top left corner
                case 6:
                    pygame.draw.arc(
                        window,
                        BLUE,
                        (((j + 0.5) * x), ((i + 0.5) * y), x, y),
                        PI / 2,
                        PI,
                        3,
                    )
                # bottom left corner
                case 7:
                    pygame.draw.arc(
                        window,
                        BLUE,
                        (((j + 0.5) * x), ((i - 0.5) * y), x, y),
                        PI,
                        3 * PI / 2,
                        3,
                    )
                # bottom right corner
                case 8:
                    pygame.draw.arc(
                        window,
                        BLUE,
                        (((j - 0.5) * x), ((i - 0.5) * y), x, y),
                        3 * PI / 2,
                        2 * PI,
                        3,
                    )

# draw status function
def draw_status(player):
    score_text = font.render(f"Score: {player.score}", True, WHITE)
    window.blit(score_text, (10, 990))

    for i in range(player.life):
        window.blit(
            pygame.transform.scale(player.images[0], (30, 30)), (650 + i * 40, 985)
        )

    if player.powerup:
        pygame.draw.circle(window, BLUE, (150, 1000), 10)

# draw menu function
def draw_menu():
    window.fill(BLACK)
    text_font = pygame.font.Font("freesansbold.ttf", 100)
    text = text_font.render("PACMAN", True, YELLOW)
    window.blit(text, (width // 2 - text.get_width() // 2, 100))

    pygame.draw.rect(window, BLUE, start_button)
    start_text = font.render("Start", True, WHITE)
    window.blit(start_text, (start_button.x + (start_button.width - start_text.get_width()) // 2, start_button.y + (start_button.height - start_text.get_height()) // 2))

    pygame.draw.rect(window, BLUE, exit_button)
    exit_text = font.render("Exit", True, WHITE)
    window.blit(exit_text, (exit_button.x + (exit_button.width - exit_text.get_width()) // 2, exit_button.y + (exit_button.height - exit_text.get_height()) // 2))

    pass

# draw level selection screen function
def draw_level_selection():
    window.fill(BLACK)
    text_font = pygame.font.Font("freesansbold.ttf", 50)
    text = text_font.render("Select Level", True, YELLOW)
    window.blit(text, (width // 2 - text.get_width() // 2, 100))

    for i, level in enumerate(levels):
        level_button = pygame.Rect(width // 2 - BUTTON_WIDTH // 2, 250 + i * (BUTTON_HEIGHT+ 30), BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(window, BLUE, level_button)
        level_text = font.render(level, True, WHITE)
        window.blit(level_text, (level_button.x + (BUTTON_WIDTH - level_text.get_width()) // 2, level_button.y + (BUTTON_HEIGHT - level_text.get_height()) // 2))

# game menu function
def menu():
    global selected_level
    level_selection = False

    while True:
        if level_selection:
            draw_level_selection()
        else:
            draw_menu()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not level_selection:
                    if start_button.collidepoint(event.pos):
                        level_selection = True

                    if exit_button.collidepoint(event.pos):
                        pygame.quit()
                        exit()
                else:
                     for i in range(len(levels)):
                        level_button = pygame.Rect(width // 2 - BUTTON_WIDTH // 2, 250 + i * (BUTTON_HEIGHT + 30), BUTTON_WIDTH, BUTTON_HEIGHT)
                        if level_button.collidepoint(event.pos):
                            selected_level = i + 1
                            return

def draw_end_game():
    window.fill(BLACK)
    text_font = pygame.font.Font("freesansbold.ttf", 100)
    game_over_image = pygame.transform.scale(pygame.image.load("./assets/game_over.png"), (700, 300))
    window.blit(game_over_image, (100, 100))

    exit_button = pygame.Rect(width // 2 - BUTTON_WIDTH // 2, height // 2 + 100, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(window, BLUE, exit_button)
    exit_text = font.render("Exit", True, WHITE)
    window.blit(exit_text, (exit_button.x + (exit_button.width - exit_text.get_width()) // 2, exit_button.y + (exit_button.height - exit_text.get_height()) // 2))

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()

# main game function
def main():
    global selected_level

    #menu screen
    menu()

    # choose active ghosts for each levels
    active_ghosts = []
    if selected_level in {1, 2, 3, 4}:
        active_ghosts.append(ghosts[selected_level - 1])
    else:
        active_ghosts = ghosts

    run = True
    promise = [False, False, False, False]

    while run:
        # print_board(boards)
        timer.tick(fps)
        window.fill(BLACK)
        draw_board(game_board)
        draw_status(player)

        # player actions
        player.draw_player(window)
        player.update(ghosts)
        if selected_level == 6:
            player.move()
        for ghost in ghosts:
            if player.check_collision(ghost):
                if selected_level == 6:
                    player.life -= 1
                    for i in range(len(game_board)):
                        for j in range(len(game_board[i])):
                            if original_board[i][j] in {1, 2} and game_board[i][j] == 0:
                                continue
                            game_board[i][j] = original_board[i][j]
                    if player.life > 0:
                        player.x = 450
                        player.y = 720
                        player.set_direction(0)

                        for ghost in active_ghosts:
                            ghost.x = ghost.spawn_x
                            ghost.y = ghost.spawn_y
                            ghost.can_move = False
                        break

            # end game
            if player.can_move == False and selected_level == 6:
                ghost.can_move = False

        # ghost actions
        new_target = (player.x, player.y)
        for ghost in active_ghosts:
            ghost.draw_ghost(window)
            if ghost.dead:
                new_target = (ghost.spawn_x, ghost.spawn_y)
            ghost.update_path(new_target)
            ghost.move()

        # check end game
        if selected_level < 6:
            complete = all(ghost.x == player.x and ghost.y == player.y for ghost in active_ghosts)
            if complete:
                draw_end_game()
                run = False

        else:
            if player.life == 0:
                draw_end_game()
                run = False

        # control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.can_move = True
                    isStart = True
                    for ghost in ghosts:
                        ghost.can_move = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if player.direction == 0 or player.direction == 1:
                        player.set_direction(0)
                    elif player.direction == 2 or player.direction == 3:
                        promise[0] = True
                        promise[1] = False
                        promise[2] = False
                        promise[3] = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if player.direction == 0 or player.direction == 1:
                        player.set_direction(1)
                    elif player.direction == 2 or player.direction == 3:
                        promise[1] = True
                        promise[0] = False
                        promise[2] = False
                        promise[3] = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if player.direction == 2 or player.direction == 3:
                        player.set_direction(2)
                    elif player.direction == 0 or player.direction == 1:
                        promise[2] = True
                        promise[0] = False
                        promise[1] = False
                        promise[3] = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if player.direction == 2 or player.direction == 3:
                        player.set_direction(3)
                    elif player.direction == 0 or player.direction == 1:
                        promise[3] = True
                        promise[0] = False
                        promise[1] = False
                        promise[2] = False

        if promise[0] and player.x % 30 == 0 and player.y % 30 == 0:
            player.set_direction(0)
            promise[0] = False
        elif promise[1] and player.x % 30 == 0 and player.y % 30 == 0:
            player.set_direction(1)
            promise[1] = False
        elif promise[2] and player.x % 30 == 0 and player.y % 30 == 0:
            player.set_direction(2)
            promise[2] = False
        elif promise[3] and player.x % 30 == 0 and player.y % 30 == 0:
            player.set_direction(3)
            promise[3] = False
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
