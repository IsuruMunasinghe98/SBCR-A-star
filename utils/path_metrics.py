import numpy as np
from typing import List, Tuple, Sequence
from math import hypot, isclose
from math import inf, floor

def calculate_path_length(path):
    if len(path) < 2:
        return 0.0
    total_length = 0.0
    for i in range(len(path) - 1):
        current_point = np.array(path[i])
        next_point = np.array(path[i + 1])
        distance = np.linalg.norm(next_point - current_point)
        total_length += distance
    return total_length

def _remove_near_duplicates(path: List[Tuple[float, float]], eps: float = 1e-9) -> List[Tuple[float, float]]:
    out: List[Tuple[float, float]] = []
    for p in path:
        if not out or hypot(p[0]-out[-1][0], p[1]-out[-1][1]) > eps:
            out.append(p)
    return out

def _remove_collinear(path: List[Tuple[float, float]], area_eps: float = 1e-9) -> List[Tuple[float, float]]:
    if len(path) <= 2:
        return path[:]
    out = [path[0]]
    for i in range(1, len(path)-1):
        ax, ay = out[-1]
        bx, by = path[i]
        cx, cy = path[i+1]
        # Twice the area of triangle ABC
        area2 = abs((bx-ax)*(cy-ay) - (by-ay)*(cx-ax))
        if area2 > area_eps:
            out.append(path[i])
    out.append(path[-1])
    return out