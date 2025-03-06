import heapq

import pygame

from board import boards
from search import astar, bfs, dfs, heuristic, ucs

# scare_image = pygame.transform.scale(pygame.image.load('../assets/ghost_images/powerup.png'), (45, 45))
# dead_image = pygame.transform.scale(pygame.image.load('../assets/ghost_images/dead.png'), (45, 45))

direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]


# grid to pixel
def grid_to_pixel(row, col):
    return col * 30, row * 30


# pixel to grid
def pixel_to_grid(x, y):
    return y // 30, x // 30


# def ucs(boards, start, end):
#     rows, cols = len(boards), len(boards[0])
#     pq = [(0, start)]
#     parent = {}
#     cost = {start: 0}
#     visited = set()

#     while pq:

#         cur_cost, (x, y) = heapq.heappop(pq)

#         if (x, y) in visited:
#             continue
#         visited.add((x, y))

#         if (x, y) == end:
#             path = []
#             while (x, y) in parent:
#                 path.append((x, y))
#                 x, y = parent[(x, y)]
#             path.append(start)
#             path.reverse()
#             return path

#         for dx, dy in direction:
#             nx, ny = x + dx, y + dy

#             if 0 <= nx < rows and 0 <= ny < cols and boards[nx][ny] <= 2:
#                 new_cost = cur_cost + 1

#                 if (nx, ny) not in cost or new_cost < cost[(nx, ny)]:
#                     cost[(nx, ny)] = new_cost
#                     heapq.heappush(pq, (new_cost, (nx, ny)))
#                     parent[(nx, ny)] = (x, y)

#     return None


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

    def update_path(self, new_target):
        if self.prev_target != new_target:
            new_path = ucs(
                boards,
                pixel_to_grid(self.x, self.y),
                pixel_to_grid(new_target[0], new_target[1]),
            )
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
