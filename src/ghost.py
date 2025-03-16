import pygame
import time
import tracemalloc

from board import boards
from search import astar, bfs, ids, ucs, dfs
from performance import Performance

direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]
scared_image = pygame.transform.scale(
    pygame.image.load(f"./assets/ghost_images/powerup.png"), (30, 30)
)
dead_image = pygame.transform.scale(
    pygame.image.load(f"./assets/ghost_images/dead.png"), (30, 30)
)

# grid to pixel
def grid_to_pixel(row, col):
    return col * 30, row * 30


# pixel to grid
def pixel_to_grid(x, y):
    return (y // 30) % 33, (x // 30) % 30

class Ghost:
    def __init__(self, x, y, image, id, value):
        self.image = image
        self.x = x
        self.y = y
        self.id = id
        self.can_move = False
        self.target = None
        self.path = []
        self.can_be_eaten = False
        self.dead = False
        self.last_value = value
        self.performance = Performance()
        self.spawn_x, self.spawn_y = x, y

    def update_path(self, new_target):
        if self.target != new_target:
            countNodes = [0]
            tracemalloc.start()

            memStart = tracemalloc.take_snapshot()
            startTime = time.perf_counter_ns()

            if self.dead:
                new_path = astar(
                    boards,
                    pixel_to_grid(self.x, self.y),
                    pixel_to_grid(self.spawn_x, self.spawn_y),
                    countNodes
                )

            elif self.id == 1:
                new_path = bfs(
                    boards,
                    pixel_to_grid(self.x, self.y),
                    pixel_to_grid(new_target[0], new_target[1]),
                    countNodes
                )
            elif self.id == 2 and self.x % 90 == 0 and self.y % 90 == 0:
                new_path = dfs(
                    boards,
                    pixel_to_grid(self.x, self.y),
                    pixel_to_grid(new_target[0], new_target[1]),
                    countNodes
                )
            elif self.id == 3:
                new_path = ucs(
                    boards,
                    pixel_to_grid(self.x, self.y),
                    pixel_to_grid(new_target[0], new_target[1]),
                    countNodes
                )
            else:
                new_path = astar(
                    boards,
                    pixel_to_grid(self.x, self.y),
                    pixel_to_grid(new_target[0], new_target[1]),
                    countNodes
                )

            endTime =  time.perf_counter_ns()
            memEnd = tracemalloc.take_snapshot()
            memRes = memEnd.compare_to(memStart, 'lineno')
            self.performance.update("searchTime", (endTime - startTime) / 1000000)
            self.performance.update("expandedNodes", countNodes[0])
            self.performance.update("memory",  sum(stat.size for stat in memRes if "search.py" in stat.traceback[0].filename))
            tracemalloc.stop()
            self.performance.printPer(self.id)
            if new_path and new_path != self.path:
                new_path.pop(0)
                self.path = new_path
            self.target = new_target

    def move(self):
        if not self.path:
            return
        if not self.dead:
            if self.last_value < 3:
                boards[self.y // 30][self.x // 30] = self.last_value
            else:
                self.last_value = 0
                boards[self.y // 30][self.x // 30] = self.last_value
        if self.can_move:
            cur_x, cur_y = self.path[0]
            target_x, target_y = grid_to_pixel(cur_x, cur_y)

            speed = 2
            if self.x < target_x and self.y % 30 == 0:
                self.x += speed
            elif self.x > target_x and self.y % 30 == 0:
                self.x -= speed
            elif self.y < target_y and self.x % 30 == 0:
                self.y += speed
            elif self.y > target_y and self.x % 30 == 0:
                self.y -= speed

            if self.x == target_x and self.y == target_y:
                self.path.pop(0)
            if self.x == self.spawn_x and self.y == self.spawn_y:
                self.dead = False
            if not self.dead:
                if boards[self.y // 30][self.x // 30] < 3:
                    self.last_value = boards[self.y // 30][self.x // 30]
                else:
                    self.last_value = 0
                boards[self.y // 30][self.x // 30] = 10 + self.id


    def draw_ghost(self, window):
        if self.dead:
            window.blit(dead_image, (self.x, self.y))
        elif self.can_be_eaten:
            window.blit(scared_image, (self.x, self.y))
        else:
            window.blit(self.image, (self.x, self.y))
