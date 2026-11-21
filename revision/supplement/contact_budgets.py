"""Matched 4/5/6-endpoint probe comparisons. Full conic uses a direct elliptic fit."""

from pathlib import Path
import csv
import numpy as np
from run import shape, chord_map

OUT = Path(__file__).resolve().parent
D = np.array([[1.0, 0.0], [0.0, 1.0], [2**-0.5, 2**-0.5]])
N = 2000


def endpoints(c, q, origin, u, noise):
    v = origin - c
    a = u @ q @ u
    middle = -(v @ q @ u) / a
    sq = middle**2 - (np.einsum("ni,ij,nj->n", v, q, v) - 1) / a
    roots = middle[:, None] + np.sqrt(np.maximum(0, sq))[:, None] * np.array(
        [-1.0, 1.0]
    )
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


def record(rows, c, q, tracking, policy, k, est, visible):
    valid = visible & np.isfinite(est).all(axis=1)
    err = est + tracking - c
    rho = np.sqrt(np.einsum("ni,ij,nj->n", err, q, err))
    time = k * 0.22 + 0.42 + np.linalg.norm(est, axis=1) / 30.0
    for deadline in (1.8, 2.1):
        done = valid & (time <= deadline)
        success = done & (rho <= 0.08)
        rows.append(
            dict(
                touches=k,
                policy=policy,
                deadline_s=deadline,
                starts=N,
                scans_observable=int(visible.sum()),
                fit_valid=int(valid.sum()),
                within_time=int(done.sum()),
                geometry_only=int((valid & (rho <= 0.08)).sum()),
                seated=int(success.sum()),
                rms_center_error_mm=np.sqrt(
                    np.mean(np.sum((est[valid] - c[valid]) ** 2, axis=1))
                )
                if valid.any()
                else "",
            )
        )


def main():
    rng = np.random.default_rng(21707)
    ang = rng.uniform(0, 2 * np.pi, N)
    c = (4.5 * np.sqrt(rng.random(N)))[:, None] * np.column_stack(
        [np.cos(ang), np.sin(ang)]
    )
    q = shape((7.0, 3.5), 35)
    noise = rng.normal(0, 0.12, (N, 3, 2))
    tracking = rng.normal(0, 0.06, (N, 2))
    zero = np.zeros_like(c)
    a, o1 = endpoints(c, q, zero, D[0], noise[:, 0])
    b, o2 = endpoints(c, q, zero, D[1], noise[:, 1])
    mid = np.c_[a[:, :, 0].mean(axis=1), b[:, :, 1].mean(axis=1)]
    shifted = np.c_[mid[:, 0], np.zeros(N)]
    bseq, ok_seq = endpoints(c, q, shifted, D[1], noise[:, 1])
    seq = np.c_[mid[:, 0], bseq[:, :, 1].mean(axis=1)]
    dseq, oks = endpoints(c, q, seq, D[0], noise[:, 2])
    last, oi = endpoints(c, q, mid, D[2], noise[:, 2])
    points = np.concatenate([a, b, last], axis=1)
    ok = np.concatenate([o1, o2, oi], axis=1)
    rows = []
    four = ok[:, :4].all(axis=1)
    record(rows, c, q, tracking, "independent_midpoint", 4, mid, four)
    record(
        rows,
        c,
        q,
        tracking,
        "coupled_midpoint",
        4,
        np.linalg.solve(chord_map(q), mid.T).T,
        four,
    )
    record(
        rows,
        c,
        q,
        tracking,
        "sequential_midpoint",
        4,
        seq,
        o1.all(axis=1) & ok_seq.all(axis=1),
    )
    sixseq = np.c_[dseq[:, :, 0].mean(axis=1), seq[:, 1]]
    record(
        rows,
        c,
        q,
        tracking,
        "sequential_midpoint",
        6,
        sixseq,
        o1.all(axis=1) & ok_seq.all(axis=1) & oks.all(axis=1),
    )
    for k in (4, 5, 6):
        visible = ok[:, :k].all(axis=1)
        for label, fit in [
            ("known_shape_LS", lambda v: known_fit(v, q)),
            ("free_ellipse_LS", conic_fit),
        ]:
            if label == "free_ellipse_LS" and k == 4:
                continue
            pred = np.full_like(c, np.nan)
            for i in np.flatnonzero(visible):
                try:
                    pred[i] = fit(points[i, :k])
                except (ValueError, np.linalg.LinAlgError):
                    pass
            record(rows, c, q, tracking, label, k, pred, visible)
    with (OUT / "contact_budgets.csv").open("w", newline="") as f:
        out = csv.DictWriter(f, fieldnames=rows[0])
        out.writeheader()
        out.writerows(rows)
    for k in (5, 6):
        # Independent exact-boundary check on noncollinear examples.
        center = np.array([0.73, -1.1])
        t = np.arange(k) * 2 * np.pi / k
        p = center + np.column_stack([np.cos(t), np.sin(t)]) @ np.linalg.inv(
            np.linalg.cholesky(q)
        )
        np.testing.assert_allclose(conic_fit(p), center, atol=1e-10)
        np.testing.assert_allclose(known_fit(p, q), center, atol=1e-10)


if __name__ == "__main__":
    main()
