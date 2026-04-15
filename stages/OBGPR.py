import math
from math import hypot, ceil
import numpy as np


def OBGPR(grid, path):
    rows, cols = len(grid), len(grid[0])

    def is_free(x, y):
        return 0 <= y < rows and 0 <= x < cols and grid[x][y] == 1

    def has_horizontal_los(x1, x2, y_float):
        y_low = max(int(y_float - 0.5), 0)
        y_high = y_low + 1
        x_start, x_end = sorted((int(x1 + 0.5), int(x2 + 0.5)))

        y_low = min(y_low, len(grid) - 1)
        y_high = min(y_high, len(grid) - 1)
        x_start = max(x_start, 0)
        x_end = min(x_end, len(grid[0]) - 1)

        _is_free = is_free
        for x in range(x_start, x_end + 1):
            if not (_is_free(x, y_low) or _is_free(x, y_high)):
                return False
        return True

    def has_vertical_los(y1, y2, x_float):
        x_low = int(x_float - 0.5)
        x_high = x_low + 1
        y_start, y_end = sorted((int(y1 + 0.5), int(y2 + 0.5)))

        x_low = max(0, min(x_low, len(grid[0]) - 1))
        x_high = max(0, min(x_high, len(grid[0]) - 1))
        y_start = max(0, min(y_start, len(grid) - 1))
        y_end = max(0, min(y_end, len(grid) - 1))

        _is_free = is_free
        for y in range(y_start, y_end + 1):
            if not (_is_free(x_low, y) or _is_free(x_high, y)):
                return False

        return True

    simplified = [path[0]]
    n = len(path)
    i = 0

    while i < n - 1:
        extended = False
        for j in range(n - 1, i, -1):
            x1, y1 = path[i]
            x2, y2 = path[j]

            if y1 == y2 and ((y1 - int(y1)) != 0):
                if has_horizontal_los(x1, x2, y1):
                    simplified.append(path[j])
                    i = j
                    extended = True
                    break

            elif x1 == x2 and ((x1 - int(x1)) != 0):
                if has_vertical_los(y1, y2, x1):
                    simplified.append(path[j])
                    i = j
                    extended = True
                    break

        if not extended:
            simplified.append(path[i + 1])
            i += 1

    return simplified
