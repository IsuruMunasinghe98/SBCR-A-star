from math import hypot, ceil

def densify_path(points, max_step=0.5):
    if not points:
        return []

    dense = [points[0]]

    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        dx = x1 - x0
        dy = y1 - y0
        dist = hypot(dx, dy)

        if dist == 0:
            continue

        n_steps = int(ceil(dist / max_step))

        for k in range(1, n_steps + 1):
            t = k / n_steps
            x = x0 + t * dx
            y = y0 + t * dy
            dense.append((x, y))

    return dense
