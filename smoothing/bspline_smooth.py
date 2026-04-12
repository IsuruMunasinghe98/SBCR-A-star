import numpy as np
from scipy.interpolate import splprep, splev, make_interp_spline

def bspline_smooth(waypoints, degree=3, smoothing=0.0, num=200, periodic=False):
    P = np.asarray(waypoints, dtype=float)
    if P.ndim != 2 or P.shape[1] != 2:
        raise ValueError("Waypoints must be an (N,2) array.")

    # 1) Drop NaN/Inf
    P = P[np.isfinite(P).all(axis=1)]
    if len(P) < 2:
        return P.copy()

    # 2) Drop consecutive duplicates / tiny segments
    eps = 1e-9
    keep = [0]
    for i in range(1, len(P)):
        if np.linalg.norm(P[i] - P[keep[-1]]) > eps:
            keep.append(i)
    P = P[keep]
    m = len(P)
    if m < 2:
        return P.copy()

    k = int(min(max(1, degree), m - 1, 5))

    # 4) Strictly increasing chord-length parameter
    seg = np.linalg.norm(np.diff(P, axis=0), axis=1)
    # If any zero-length remains, compress again
    if np.any(seg <= eps):
        mask = np.r_[True, seg > eps]
        P = P[mask]
        m = len(P)
        if m < 2:
            return P.copy()
        k = int(min(max(1, degree), m - 1, 5))
        seg = np.linalg.norm(np.diff(P, axis=0), axis=1)

    u = np.concatenate(([0.0], np.cumsum(seg)))
    if u[-1] == 0.0:
        return P.copy()
    u /= u[-1]

    per = 1 if periodic else 0

    # 5) Try splprep; if it fails, reduce k; final fallback to make_interp_spline
    last_err = None
    for k_try in range(k, 0, -1):
        try:
            tck, _ = splprep([P[:, 0], P[:, 1]], u=u, s=float(smoothing),
                             k=k_try, per=per)
            us = np.linspace(0, 1, num, endpoint=not periodic)
            xs, ys = splev(us, tck)
            return np.column_stack([xs, ys])
        except Exception as e:
            last_err = e
            continue

    # Fallback: interpolating spline (no smoothing), still robust and won’t error
    t = np.linspace(0, 1, len(P))
    k2 = min(3, len(P) - 1)
    sx = make_interp_spline(t, P[:, 0], k=k2)
    sy = make_interp_spline(t, P[:, 1], k=k2)
    ts = np.linspace(0, 1, num, endpoint=True)
    return np.column_stack([sx(ts), sy(ts)])
