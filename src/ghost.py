import pygame
import time

from board import boards
from search import astar, bfs, dfs, heuristic, ucs
from performance import Performance

direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]


# grid to pixel
def grid_to_pixel(row, col):
    return col * 30, row * 30


# pixel to grid
def pixel_to_grid(x, y):
    return y // 30, x // 30

class Ghost:
    def __init__(self, x, y, player):
        self.image = pygame.transform.scale(
            pygame.image.load(f"./assets/ghost_images/blue.png"), (30, 30)
        )
        self.x = x
        self.y = y
        self.player = player
        self.prev_target = None
        self.speed = 2
        self.path = []
        self.performance = Performance()

    def update_path(self, new_target):
        if self.prev_target != new_target:
            countNodes = [0]
            startTime = time.perf_counter_ns()
            new_path = bfs(
                boards,
                pixel_to_grid(self.x, self.y),
                pixel_to_grid(new_target[0], new_target[1]),
                countNodes
            )
            endTime =  time.perf_counter_ns()
            self.performance.update("searchTime", (endTime - startTime) / 1000000)
            self.performance.update("expandedNodes", countNodes[0])
            self.performance.printPer()
            if new_path != self.path:
                self.path = new_path
            self.prev_target = new_target

    def move(self):
        if not self.path:
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

    def draw_ghost(self, window):
        window.blit(self.image, (self.x, self.y))
