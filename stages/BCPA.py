from typing import List, Tuple

def obstacle_corner_contacts(grid, path):
    H, W = len(grid), len(grid[0])
    contacts = []

    def _ri(x):
        return int(round(float(x)))

    def is_obstacle(r, c):
        ri, ci = _ri(r), _ri(c)
        return 0 <= ri < H and 0 <= ci < W and grid[ri][ci] == 0

    if not path or len(path) < 2:
        return contacts

    for (r1, c1), (r2, c2) in zip(path, path[1:]):
        r1i, c1i = _ri(r1), _ri(c1)
        r2i, c2i = _ri(r2), _ri(c2)
        dr, dc = r2i - r1i, c2i - c1i

        if abs(dr) == 1 and abs(dc) == 1:
            corner_r = min(r1i, r2i) + 0.5
            corner_c = min(c1i, c2i) + 0.5
            cellA = (r1i, c2i)
            cellB = (r2i, c1i)
            if is_obstacle(*cellA) or is_obstacle(*cellB):
                contacts.append(((r1, c1), (corner_r, corner_c), (r2, c2)))
            else:
                contacts.append(((r1, c1), None, (r2, c2)))
        else:
            contacts.append(((r1, c1), None, (r2, c2)))

    return contacts

def BCPA(grid: List[List[int]], path: List[Tuple[int,int]]):
    new_path: List[Tuple[float, float]] = []
    if not path:
        return new_path
    new_path.append(((path[0][0]), (path[0][1])))

    pieces = obstacle_corner_contacts(grid, path)
    for (_a, maybe_corner, b) in pieces:
        if maybe_corner is not None:
            new_path.append(maybe_corner)
        new_path.append(((b[0]), (b[1])))

    deduped = [new_path[0]]
    for p in new_path[1:]:
        if p != deduped[-1]:
            deduped.append(p)
    return deduped
