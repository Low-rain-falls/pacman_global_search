import time
import pygame
import threading

from board import boards
from search import astar, bfs, dfs, ucs
from performance import Performance

# left - down - right - up
direction = [(-1, 0), (0, -1), (1, 0), (0, 1)]

scared_image = pygame.transform.scale(
    pygame.image.load(f"./assets/ghost_images/powerup.png"), (30, 30)
)
dead_image = pygame.transform.scale(
    pygame.image.load(f"./assets/ghost_images/dead.png"), (30, 30)
)

# Converter to draw
def grid_to_pixel(row, col):
    return col * 30, row * 30


# Converter to calculate path and move
def pixel_to_grid(x, y):
    return (y // 30) % 33, (x // 30) % 30

class Ghost():
    def __init__(self, x, y, image, player, id):
        self.image = image
        self.x = x
        self.y = y
        self.player = player
        self.id = id
        self.can_move = False
        self.running = True
        self.target = None
        self.can_be_eaten = False
        self.speed = 2
        self.path = []
        self.performance = Performance()
        self.lock = threading.Lock()
        self.spawn_x, self.spawn_y = x, y
        self.dead = False

    def update_path(self):
        while self.running:
            with self.lock:
                if self.dead:
                    new_target = (self.spawn_x, self.spawn_y)
                else:
                    new_target = (self.player.x, self.player.y)
                
                if self.target != new_target:   
                    self.target = new_target
                
                if (self.x % 30 == 0 and self.y % 30 == 0):
                    countNodes = [0]

                    if self.dead:
                        new_path = astar(
                            boards,
                            pixel_to_grid(self.x, self.y),
                            pixel_to_grid(self.target[0], self.target[1]),
                            countNodes
                        )

                    elif self.id == 1:
                        new_path = bfs(
                            boards,
                            pixel_to_grid(self.x, self.y),
                            pixel_to_grid(self.target[0], self.target[1]),
                            countNodes
                        )
                    
                    elif self.id == 2:
                        new_path = dfs(
                            boards,
                            pixel_to_grid(self.x, self.y),
                            pixel_to_grid(self.target[0], self.target[1]),
                            countNodes
                        )
                    
                    elif self.id == 3:
                        new_path = ucs(
                            boards,
                            pixel_to_grid(self.x, self.y),
                            pixel_to_grid(self.target[0], self.target[1]),
                            countNodes
                        )
                    
                    else:
                        new_path = astar(
                            boards,
                            pixel_to_grid(self.x, self.y),
                            pixel_to_grid(self.target[0], self.target[1]),
                            countNodes
                        )
                    
                    if new_path != self.path:
                        self.path = new_path
            time.sleep(0.5)                  
            

    def move(self):
        with self.lock:
            if not self.can_move or not self.path:
                return

            cur_x, cur_y = self.path[0]
            target_x, target_y = grid_to_pixel(cur_x, cur_y)

            if self.x < target_x:
                self.x += self.speed
            elif self.x > target_x:
                self.x -= self.speed

            if self.y < target_y:
                self.y += self.speed
            elif self.y > target_y:
                self.y -= self.speed

            if self.x == target_x and self.y == target_y:
                self.path.pop(0)
            if self.x == self.spawn_x and self.y == self.spawn_y:
                self.dead = False


    def draw_ghost(self, window):
        if self.dead:
            window.blit(dead_image, (self.x, self.y))
        elif self.can_be_eaten:
            window.blit(scared_image, (self.x, self.y))
        else:
            window.blit(self.image, (self.x, self.y))
