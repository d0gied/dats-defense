import numpy as np
from matplotlib import pyplot as plt


matrix = np.zeros((30, 30))

matrix[10:12, 10:12] = 1


start = (10, 10)

def draw_circle(center, radius):
    x_min = center[0] - radius
    x_max = center[0] + radius
    y_min = center[1] - radius
    y_max = center[1] + radius
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            if (x - center[0]) ** 2 + (y - center[1]) ** 2 <= radius ** 2:
                matrix[y, x] = 1

def brezenham(x0, y0, x1, y1):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    if dx > dy:
        err = dx / 2.0
        while x != x1:
            draw_circle((x, y), 3)
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y1:
            draw_circle((x, y), 3)
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    draw_circle((x, y), 3)

brezenham(10, 10, 16, 18)


plt.imshow(matrix, cmap="hot", interpolation="nearest")

plt.show()
