from board import boards
from convert import pixel_to_grid, grid_to_pixel
from performance import Performance


direction = [(-1, 0), (0, 1), (1, 0), (0, -1)]

class Ghost:
    def __init__(self, x, y, image, id, search_func):
        self.image = image
        self.x, self.y = x, y
        self.id = id + 10
        self.search_func = search_func
        self.can_move = False
        self.target = None
        self.path = []
        self.performance = Performance()

    def update_path(self, new_target):
        if self.target != new_target:
            countNodes = [0]
        
            new_path = self.search_func(boards,
                                        pixel_to_grid(self.x, self.y),
                                        countNodes)
            
            print("New path: ", new_path)

            if new_path != self.path:
                self.path = new_path
            self.target = new_target

    def move(self):
        print("move")
        print(self.x, self.y)
        boards[(self.y // 30) % 33][(self.x // 30) % 30] = 0

        if self.can_move:
            if not self.path:
                return

            cur_x, cur_y = self.path[0]
            target_x, target_y = grid_to_pixel(cur_x, cur_y)

            speed = 2

            if self.x < target_x:
                self.x += speed
            elif self.x > target_x:
                self.x -= speed

            if self.y < target_y:
                self.y += speed
            elif self.y > target_y:
                self.y -= speed

            if self.x == target_x and self.y == target_y:
                self.path.pop(0)
        print(self.x, self.y)
        boards[(self.y // 30) % 33][(self.x // 30) % 30] = self.id

    def draw_ghost(self, window):
        window.blit(self.image, (self.x, self.y))
