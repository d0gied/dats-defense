import numpy as np
from matplotlib import pyplot as plt


matrix = np.zeros((20, 20))

matrix[10:12, 10:12] = 1


def step(matrix):
    weights = np.zeros_like(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 1:
                for x in range(-4, 4):
                    for y in range(-4, 4):
                        dst = abs(x) ** 2 + abs(y) ** 2
                        if dst == 0:
                            continue
                        if matrix[i + x][j + y] == 0:
                            weights[i + x][j + y] += 1 / dst



    return new_matrix


plt.imshow(matrix, cmap="hot", interpolation="nearest")

plt.show()
