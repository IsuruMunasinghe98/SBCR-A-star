import numpy as np

def rational_quadratic_bezier_curve(P0, P1, P2, w0=1, w1=0.9, w2=1, num_points=100):
    curve = []
    for t in np.linspace(0, 1, num_points):
        numerator = (
            (1 - t)**2 * w0 * np.array(P0) + 2 * (1 - t) * t * w1 * np.array(P1) + t**2 * w2 * np.array(P2)
        )
        denominator = (1 - t)**2 * w0 + 2 * (1 - t) * t * w1 + t**2 * w2
        if denominator != 0:
            point = numerator / denominator
            curve.append(point.tolist())
        else:
            curve.append(numerator.tolist())

    return curve
