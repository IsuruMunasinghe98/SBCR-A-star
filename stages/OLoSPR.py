import math
from typing import List, Tuple, Sequence

def _all_free(grid: Sequence[Sequence[int]], cells: List[Tuple[int, int]]) -> bool:
    H, W = len(grid), len(grid[0])
    for (r, c) in cells:
        if not (0 <= r < H and 0 <= c < W) or grid[r][c] != 1:
            return False
    return True

def _cells_on_segment_supercover_dda(a: Tuple[float,float],
                                     b: Tuple[float,float],
                                     H: int, W: int) -> List[Tuple[int,int]]:
    ar, ac = a; br, bc = b
    r = int(math.floor(ar)); c = int(math.floor(ac))
    r_end = int(math.floor(br)); c_end = int(math.floor(bc))

    dr = br - ar
    dc = bc - ac

    if dr == 0 and dc == 0:
        return [(r, c)] if 0 <= r < H and 0 <= c < W else []

    step_r = 1 if dr > 0 else -1 if dr < 0 else 0
    step_c = 1 if dc > 0 else -1 if dc < 0 else 0

    inv_dr = 1.0 / dr if dr != 0 else float('inf')
    inv_dc = 1.0 / dc if dc != 0 else float('inf')

    def first_t_max(p, dp, cell, step):
        if dp == 0:
            return float('inf')
        next_boundary = cell + (1 if step > 0 else 0)
        return (next_boundary - p) / dp

    def t_delta(dp):
        return abs(1.0 / dp) if dp != 0 else float('inf')

    t = 0.0
    t_end = 1.0

    tMaxR = first_t_max(ar, dr, r, step_r)
    tMaxC = first_t_max(ac, dc, c, step_c)
    tDeltaR = t_delta(dr)
    tDeltaC = t_delta(dc)

    out = []

    if 0 <= r < H and 0 <= c < W:
        out.append((r, c))

    while t <= t_end:
        if tMaxR < tMaxC:
            # step in r
            r += step_r
            t = tMaxR
            tMaxR += tDeltaR
        else:
            # step in c
            c += step_c
            t = tMaxC
            tMaxC += tDeltaC

        if t > t_end:
            break

        if 0 <= r < H and 0 <= c < W:
            # avoid duplicates
            if not out or out[-1] != (r, c):
                out.append((r, c))

    if 0 <= r_end < H and 0 <= c_end < W and (r_end, c_end) not in out:
        out.append((r_end, c_end))

    return out

def segment_is_free(grid: List[List[int]], a: Tuple[float, float], b: Tuple[float, float]) -> bool:
    H, W = len(grid), len(grid[0])
    cells = _cells_on_segment_supercover_dda(a, b, H, W)
    return bool(cells) and _all_free(grid, cells)

def OLoSPR(grid: List[List[int]],
                 path: List[Tuple[float, float]],
                 eps: float = 1e-9) -> List[Tuple[float, float]]:
    n = len(path)
    if n <= 1:
        return [tuple(p) for p in path]

    out: List[Tuple[float, float]] = [path[0]]
    i = 0
    while i < len(path) - 1:
        chosen = i + 1
        for j in range(len(path) - 1, i, -1):
            if segment_is_free(grid, path[i], path[j]):
                chosen = j
                break
        out.append(path[chosen])
        i = chosen

    return out
