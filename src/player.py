import pygame

from board import boards


class Player:
    def __init__(self, x, y):
        self.images = [
            pygame.transform.scale(
                pygame.image.load(f"./assets/player_images/{i}.png"), (30, 30)
            )
            for i in range(1, 5)
        ]
        self.x = x
        self.y = y
        self.can_move = False
        self.direction = 1
        self.counter = 0
        self.score = 0
        self.life = 3
        self.powerup = False

    def draw_player(self, window):
        # 0 - right, 1 - left, 2 - up, 3 - down
        if self.direction == 0:
            window.blit(self.images[self.counter // 5], (self.x, self.y))
        elif self.direction == 1:
            window.blit(
                pygame.transform.rotate(self.images[self.counter // 5], 180),
                (self.x, self.y),
            )
        elif self.direction == 2:
            window.blit(
                pygame.transform.rotate(self.images[self.counter // 5], 90),
                (self.x, self.y),
            )
        elif self.direction == 3:
            window.blit(
                pygame.transform.rotate(self.images[self.counter // 5], -90),
                (self.x, self.y),
            )

    def update(self):
        if self.counter < 19:
            self.counter += 1
        else:
            self.counter = 0

    def set_direction(self, direction):
        self.direction = direction

    def move(self):
        if self.can_move:
            if self.x > 900:
                self.x = -30
            elif self.x < -30:
                self.x = 900

            speed = 2
            if self.direction == 0:
                if boards[(self.y // 30) % 33][(self.x // 30 + 1) % 30] < 3:
                    self.x += speed
            elif self.direction == 1:
                if boards[(self.y // 30) % 33][((self.x - 1) // 30) % 30] < 3:
                    self.x -= speed
            elif self.direction == 2:
                if boards[((self.y - 1) // 30) % 33][(self.x // 30) % 30] < 3:
                    self.y -= speed
            elif self.direction == 3:
                if boards[((self.y) // 30 + 1) % 33][(self.x // 30) % 30] < 3:
                    self.y += speed

    def cal_score(self):
        if boards[(self.y // 30) % 33][(self.x // 30) % 30] == 1:
            boards[(self.y // 30) % 33][(self.x // 30) % 30] = 0
            self.score += 5
        elif boards[(self.y // 30) % 33][(self.x // 30) % 30] == 2:
            boards[(self.y // 30) % 33][(self.x // 30) % 30] = 0
            self.score += 20

    def check_collision(self, ghost):
        if not self.powerup:
            if self.x == ghost.x and self.y == ghost.y:
                self.can_move == False
                self.life -= 1

