"""Rim intersections and constrained ellipse fitting (adapted from the study repository)."""

import numpy as np


def endpoints(c, q, origin, u, noise):
    v = origin - c
    a = u @ q @ u
    middle = -(v @ q @ u) / a
    sq = middle**2 - (np.einsum("ni,ij,nj->n", v, q, v) - 1) / a
    roots = middle[:, None] + np.sqrt(np.maximum(0, sq))[:, None] * np.array([-1.0, 1.0])
    ok = (sq >= 0)[:, None] & (np.abs(roots) <= 12)
    return origin[:, None, :] + (roots + noise)[:, :, None] * u, ok


def known_fit(p, q):
    # Subtract each centered quadratic equation from the mean, then solve for center.
    v = p - p.mean(axis=0)
    rhs = np.einsum("ni,ij,nj->n", p, q, p)
    return np.linalg.lstsq(2 * v @ q, rhs - rhs.mean(), rcond=None)[0]


def conic_fit(p):
    if len(p) < 5:
        raise ValueError("five independent point constraints are required")
    center = p.mean(axis=0)
    scale = np.sqrt(np.mean((p - center) ** 2))
    x, y = ((p - center) / scale).T
    d1 = np.column_stack([x * x, x * y, y * y])
    d2 = np.column_stack([x, y, np.ones_like(x)])
    if np.linalg.matrix_rank(np.column_stack([d1, d2])) < 5:
        raise ValueError("underdetermined conic")
    t = -np.linalg.lstsq(d2, d1, rcond=None)[0]
    reduced = d1 + d2 @ t
    constrain = np.array([[0, 0, 2], [0, -1, 0], [2, 0, 0]])
    _, vectors = np.linalg.eig(np.linalg.solve(constrain, reduced.T @ reduced))
    options = []
    for v in vectors.T:
        if np.max(np.abs(v.imag)) > 1e-8:
            continue
        a, b, c = v.real
        if 4 * a * c - b * b <= 1e-12:
            continue
        d, e, f = t @ v.real
        q = np.array([[a, b / 2], [b / 2, c]])
        off = -np.linalg.solve(2 * q, [d, e])
        level = off @ q @ off - f
        if np.min(np.linalg.eigvalsh(q / level)) <= 0:
            continue
        options.append(
            (
                np.mean((reduced @ v.real) ** 2) / (4 * a * c - b * b),
                center + scale * off,
            )
        )
    if not options:
        raise ValueError("no usable elliptic center")
    return min(options, key=lambda item: item[0])[1]
