import math
import numpy as np


def _points_equal(p1, p2, eps=1e-9):
    return abs(float(p1[0]) - float(p2[0])) < eps and abs(float(p1[1]) - float(p2[1])) < eps


def _append_if_new(path_out, pt, eps=1e-9):
    if not path_out or not _points_equal(path_out[-1], pt, eps):
        path_out.append((float(pt[0]), float(pt[1])))


def _cell_intersects_horizontal_segment(cell_r, cell_c, r_const, c1, c2, eps=1e-9):
    cell_r_min = cell_r - 0.5
    cell_r_max = cell_r + 0.5
    cell_c_min = cell_c - 0.5
    cell_c_max = cell_c + 0.5

    row_hits = (cell_r_min - eps) <= r_const <= (cell_r_max + eps)
    col_hits = not (c2 < cell_c_min - eps or c1 > cell_c_max + eps)
    return row_hits and col_hits


def _cell_intersects_vertical_segment(cell_r, cell_c, c_const, r1, r2, eps=1e-9):
    cell_r_min = cell_r - 0.5
    cell_r_max = cell_r + 0.5
    cell_c_min = cell_c - 0.5
    cell_c_max = cell_c + 0.5

    col_hits = (cell_c_min - eps) <= c_const <= (cell_c_max + eps)
    row_hits = not (r2 < cell_r_min - eps or r1 > cell_r_max + eps)
    return col_hits and row_hits


def corridor_los(grid, p1, p2, eps=1e-9):
    if grid is None:
        raise ValueError("grid must not be None")

    grid = np.asarray(grid)
    if grid.ndim != 2:
        raise ValueError("grid must be a 2D array")

    r1, c1 = float(p1[0]), float(p1[1])
    r2, c2 = float(p2[0]), float(p2[1])

    same_row = abs(r1 - r2) < eps
    same_col = abs(c1 - c2) < eps

    if not (same_row or same_col):
        return False

    rows, cols = grid.shape

    if same_row:
        r_const = r1
        c_min, c_max = sorted([c1, c2])

        row_start = max(0, int(math.floor(r_const - 0.5 - eps)))
        row_end   = min(rows - 1, int(math.ceil(r_const + 0.5 + eps) - 1))

        col_start = max(0, int(math.floor(c_min - 0.5 - eps)))
        col_end   = min(cols - 1, int(math.ceil(c_max + 0.5 + eps) - 1))

        for rr in range(row_start, row_end + 1):
            for cc in range(col_start, col_end + 1):
                if _cell_intersects_horizontal_segment(rr, cc, r_const, c_min, c_max, eps):
                    if grid[rr, cc] == 0:
                        return False
        return True

    if same_col:
        c_const = c1
        r_min, r_max = sorted([r1, r2])

        row_start = max(0, int(math.floor(r_min - 0.5 - eps)))
        row_end   = min(rows - 1, int(math.ceil(r_max + 0.5 + eps) - 1))

        col_start = max(0, int(math.floor(c_const - 0.5 - eps)))
        col_end   = min(cols - 1, int(math.ceil(c_const + 0.5 + eps) - 1))

        for rr in range(row_start, row_end + 1):
            for cc in range(col_start, col_end + 1):
                if _cell_intersects_vertical_segment(rr, cc, c_const, r_min, r_max, eps):
                    if grid[rr, cc] == 0:
                        return False
        return True

    return False


def OBGPR(grid, path, eps=1e-9):
    if path is None or len(path) == 0:
        return []

    if len(path) == 1:
        return [(float(path[0][0]), float(path[0][1]))]

    path = [(float(p[0]), float(p[1])) for p in path]

    refined = [path[0]]
    i = 0
    n = len(path)

    while i < n - 1:
        extended = False

        for j in range(n - 1, i, -1):
            if corridor_los(grid, path[i], path[j], eps=eps):
                _append_if_new(refined, path[j], eps=eps)
                i = j
                extended = True
                break

        if not extended:
            _append_if_new(refined, path[i + 1], eps=eps)
            i += 1

    return refined