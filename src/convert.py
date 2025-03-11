# grid to pixel
def grid_to_pixel(row, col):
    return col * 30, row * 30


# pixel to grid
def pixel_to_grid(x, y):
    return (y // 30) % 33, (x // 30) % 30