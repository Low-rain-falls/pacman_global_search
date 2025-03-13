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
        self.powerup_counter = 0

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

    def update(self, ghosts):
        if self.counter < 19:
            self.counter += 1
        else:
            self.counter = 0
        self.cal_score(ghosts)
        self.cal_powerup_time(ghosts)

    def set_direction(self, direction):
        self.direction = direction

    def move(self):
        if self.can_move:
            if self.x > 900:
                self.x = -30
            elif self.x < -30:
                self.x = 900

            speed = 5
            if self.direction == 0:
                if boards[(self.y // 30) % 33][(self.x // 30 + 1) % 30] < 3 or boards[(self.y // 30) % 33][(self.x // 30 + 1) % 30] > 10:
                    self.x += speed
            elif self.direction == 1:
                if boards[(self.y // 30) % 33][((self.x - 1) // 30) % 30] < 3 or boards[(self.y // 30) % 33][((self.x - 1) // 30) % 30] > 10:
                    self.x -= speed
            elif self.direction == 2:
                if boards[((self.y - 1) // 30) % 33][(self.x // 30) % 30] < 3 or boards[((self.y - 1) // 30) % 33][(self.x // 30) % 30] > 10:
                    self.y -= speed
            elif self.direction == 3:
                if boards[((self.y) // 30 + 1) % 33][(self.x // 30) % 30] < 3 or boards[((self.y + 1) // 30) % 33][(self.x // 30) % 30] > 10:
                    self.y += speed

    def cal_score(self, ghosts):
        if boards[(self.y // 30) % 33][(self.x // 30) % 30] == 1:
            boards[(self.y // 30) % 33][(self.x // 30) % 30] = 0
            self.score += 5
        elif boards[(self.y // 30) % 33][(self.x // 30) % 30] == 2:
            boards[(self.y // 30) % 33][(self.x // 30) % 30] = 0
            self.score += 20
            self.powerup = True
            self.powerup_counter = 0
            for ghost in ghosts:
                ghost.can_be_eaten = True

    def check_collision(self, ghost):
        if -15 < self.x - ghost.x < 15 and -15 < self.y - ghost.y < 15 and not ghost.dead:
            if boards[(self.y + 15) // 30][self.x // 30] > 10:
                boards[(self.y + 15) // 30][self.x // 30] = 0
            if boards[(self.y - 15) // 30][self.x // 30] > 10:
                boards[(self.y - 15) // 30][self.x // 30] = 0
            if boards[(self.y) // 30][(self.x + 15) // 30] > 10:
                boards[(self.y) // 30][(self.x + 15) // 30] = 0
            if boards[(self.y) // 30][(self.x - 15) // 30] > 10:
                boards[(self.y) // 30][(self.x - 15) // 30] = 0
            if not self.powerup:
                self.can_move = False
                self.life -= 1
            elif self.powerup and ghost.can_be_eaten:
                ghost.dead = True
                ghost.can_be_eaten = False
                self.score += 200
    
    def cal_powerup_time(self, ghosts):
        if self.powerup and self.powerup_counter < 600:
            self.powerup_counter += 1
        elif self.powerup and self.powerup_counter >= 600:
            self.powerup = False
            self.powerup_counter = 0
            for ghost in ghosts:
                ghost.can_be_eaten = False