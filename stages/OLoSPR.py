import math
from typing import List, Tuple, Sequence

def _all_free(grid: Sequence[Sequence[int]], cells: List[Tuple[int, int]]) -> bool:
    H, W = len(grid), len(grid[0])
    for (r, c) in cells:
        if not (0 <= r < H and 0 <= c < W):
            return False
        if grid[r][c] != 1:
            return False
    return True


def _append_unique(out: List[Tuple[int, int]], cell: Tuple[int, int], H: int, W: int):
    r, c = cell
    if 0 <= r < H and 0 <= c < W:
        if not out or out[-1] != cell:
            out.append(cell)


def _cells_on_segment_supercover_dda(a: Tuple[float, float],
                                     b: Tuple[float, float],
                                     H: int, W: int,
                                     eps: float = 1e-12) -> List[Tuple[int, int]]:

    ar, ac = float(a[0]) + 0.5, float(a[1]) + 0.5
    br, bc = float(b[0]) + 0.5, float(b[1]) + 0.5

    r = int(math.floor(ar))
    c = int(math.floor(ac))
    r_end = int(math.floor(br))
    c_end = int(math.floor(bc))

    dr = br - ar
    dc = bc - ac

    if abs(dr) < eps and abs(dc) < eps:
        return [(r, c)] if 0 <= r < H and 0 <= c < W else []

    step_r = 1 if dr > 0 else -1 if dr < 0 else 0
    step_c = 1 if dc > 0 else -1 if dc < 0 else 0

    def first_t_max(p, dp, cell, step):
        if abs(dp) < eps:
            return float("inf")
        next_boundary = cell + (1 if step > 0 else 0)
        return (next_boundary - p) / dp

    def t_delta(dp):
        return abs(1.0 / dp) if abs(dp) >= eps else float("inf")

    t = 0.0
    t_end = 1.0

    tMaxR = first_t_max(ar, dr, r, step_r)
    tMaxC = first_t_max(ac, dc, c, step_c)
    tDeltaR = t_delta(dr)
    tDeltaC = t_delta(dc)

    out: List[Tuple[int, int]] = []
    _append_unique(out, (r, c), H, W)

    while t <= t_end + eps:
        if abs(tMaxR - tMaxC) <= eps:
            nr = r + step_r
            nc = c + step_c

            _append_unique(out, (nr, c), H, W)
            _append_unique(out, (r, nc), H, W)

            r = nr
            c = nc
            t = tMaxR
            tMaxR += tDeltaR
            tMaxC += tDeltaC
            _append_unique(out, (r, c), H, W)

        elif tMaxR < tMaxC:
            r += step_r
            t = tMaxR
            tMaxR += tDeltaR
            _append_unique(out, (r, c), H, W)

        else:
            c += step_c
            t = tMaxC
            tMaxC += tDeltaC
            _append_unique(out, (r, c), H, W)

        if t > t_end + eps:
            break

    _append_unique(out, (r_end, c_end), H, W)
    return out


def segment_is_free(grid: List[List[int]],
                    a: Tuple[float, float],
                    b: Tuple[float, float],
                    eps: float = 1e-12) -> bool:
    H, W = len(grid), len(grid[0])
    cells = _cells_on_segment_supercover_dda(a, b, H, W, eps=eps)
    return bool(cells) and _all_free(grid, cells)


def OLoSPR(grid: List[List[int]],
           path: List[Tuple[float, float]],
           eps: float = 1e-12) -> List[Tuple[float, float]]:

    n = len(path)
    if n <= 1:
        return [tuple(p) for p in path]

    out: List[Tuple[float, float]] = [tuple(path[0])]
    i = 0

    while i < n - 1:
        chosen = i + 1

        for j in range(n - 1, i, -1):
            if segment_is_free(grid, path[i], path[j], eps=eps):
                chosen = j
                break

        out.append(tuple(path[chosen]))
        i = chosen

    return out