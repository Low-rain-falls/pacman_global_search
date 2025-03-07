import pygame

# import objects
from ghost import Ghost
from board import boards
from player import Player

pygame.init()

# constant
width = 900
height = 1040
PI = 3.14159265358979323846264338327950288419716939937510

# color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


# game global parameter
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("PacMan by team AI")
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font("freesansbold.ttf", 20)
game_board = boards

# player object
player = Player(450, 720)

#ghost object
blue_image = pygame.transform.scale(pygame.image.load(f'../Assets/ghost_images/blue.png'), (30, 30))
orange_image = pygame.transform.scale(pygame.image.load(f'../Assets/ghost_images/orange.png'), (30, 30))
pink_image = pygame.transform.scale(pygame.image.load(f'../Assets/ghost_images/pink.png'), (30, 30))
red_image = pygame.transform.scale(pygame.image.load(f'../Assets/ghost_images/red.png'), (30, 30))
ghosts = [
    Ghost(60, 60, blue_image, player, 1),
    Ghost(810, 60, orange_image, player, 2),
    Ghost(60, 900, pink_image, player, 3),
    Ghost(810, 900, red_image, player, 4),
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
                    pygame.draw.circle(window, WHITE, ((j + 0.5) * x, (i + 0.5) * y), 10)
                case 3:
                    pygame.draw.line(window, BLUE, ((j + 0.5) * x, i * y), ((j + 0.5) * x, i * y + y), 3,)
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
    score_text = font.render(f'Score: {player.score}', True, WHITE)
    window.blit(score_text, (10, 990))

    for i in range(player.life):
        window.blit(pygame.transform.scale(player.images[0], (30, 30)), (650 + i * 40, 985))
# main game function
def main():
    run = True
    promise = [False, False, False, False]

    while run:
        timer.tick(fps)
        window.fill(BLACK)
        draw_board(game_board)
        draw_status(player)

        #player actions
        player.draw_player(window)
        player.update()
        player.move()
        player.cal_score()
        for ghost in ghosts:
            player.check_collision(ghost)

        #ghost actions
        new_target = (player.x, player.y)
        for ghost in ghosts:
            ghost.draw_ghost(window)
            ghost.update_path(new_target)
            ghost.move()

        # control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                #  and player.x % 30 == 0 and player.y % 30 == 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.can_move = True 
                    for ghost in ghosts:
                        ghost.can_move = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if (player.direction == 0 or player.direction == 1): 
                        player.set_direction(0)
                    elif (player.direction == 2 or player.direction == 3):
                        promise[0] = True
                        promise[1] = False
                        promise[2] = False
                        promise[3] = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if (player.direction == 0 or player.direction == 1): 
                        player.set_direction(1)
                    elif (player.direction == 2 or player.direction == 3):
                        promise[1] = True
                        promise[0] = False
                        promise[2] = False
                        promise[3] = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if (player.direction == 2 or player.direction == 3): 
                        player.set_direction(2)
                    elif (player.direction == 0 or player.direction == 1):
                        promise[2] = True
                        promise[0] = False
                        promise[1] = False
                        promise[3] = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if (player.direction == 2 or player.direction == 3): 
                        player.set_direction(3)
                    elif (player.direction == 0 or player.direction == 1):
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