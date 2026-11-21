"""Matched free-ellipse trials, analytically timed, with the contact order counterbalanced."""

import csv
from pathlib import Path
import numpy as np
from aperture_geometry import conic_fit, endpoints

OUT = Path(__file__).resolve().parent
N, BLOCKS = 400, 8
TOLERANCES = [0.10, 0.25, 0.50]
DURATION = np.round(np.arange(0.10, 0.261, 0.01), 2)
DEADLINES = [1.8, 2.1]
RADIUS = 4.5


def save(name, rows):
    with (OUT / name).open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def shape(angle):
    u = np.radians(angle)
    rot = np.array([[np.cos(u), -np.sin(u)], [np.sin(u), np.cos(u)]])
    return rot @ np.diag(1 / np.square([7, 3.5])) @ rot.T


def trials():
    rows = []
    for b in range(BLOCKS):
        rng = np.random.default_rng(21770 + b)
        az = rng.uniform(0, 2 * np.pi, N)
        center = (RADIUS * np.sqrt(rng.random(N)))[:, None] * np.c_[np.cos(az), np.sin(az)]
        q = shape(35)
        noise = rng.normal(0, 0.12, (N, 3, 2))
        near = rng.integers(0, 2, N)
        for j, direction in enumerate(([1.0, 0.0], [0.0, 1.0])):
            chord, seen = endpoints(
                center, q, np.zeros_like(center), np.array(direction), noise[:, j]
            )
            if j == 0:
                horiz, h_ok = chord, seen
            else:
                vert, v_ok = chord, seen
        mid = np.c_[horiz[:, :, 0].mean(axis=1), vert[:, :, 1].mean(axis=1)]
        diag, d_ok = endpoints(center, q, mid, np.array([1.0, 1.0]) / np.sqrt(2), noise[:, 2])
        sel = np.arange(N)
        p = np.concatenate(
            [horiz, vert, diag[sel, near, None, :], diag[sel, 1 - near, None, :]], axis=1
        )
        visible = np.c_[h_ok, v_ok, d_ok[sel, near], d_ok[sel, 1 - near]]
        for i in range(N):
            row = {
                "seed_block": b + 1,
                "fixture": i + 1,
                "fifth_sign": (-1, 1)[near[i]],
                "true_x": center[i, 0],
                "true_y": center[i, 1],
            }
            for k in [5, 6]:
                row[f"visible_{k}"] = int(visible[i, :k].all())
                estimate = np.full(2, np.nan)
                if row[f"visible_{k}"]:
                    try:
                        estimate = conic_fit(p[i, :k])
                    except (ValueError, np.linalg.LinAlgError):
                        pass
                row[f"error_{k}"] = np.linalg.norm(estimate - center[i])
                row[f"travel_{k}"] = np.linalg.norm(estimate)
            rows.append(row)
    return rows


def summaries(rows):
    totals = []
    for b in [0, *range(1, BLOCKS + 1)]:
        chosen = [r for r in rows if b == 0 or r["seed_block"] == b]
        error, travel = (
            np.array([[r[f"{name}_{k}"] for k in (5, 6)] for r in chosen])
            for name in ("error", "travel")
        )
        for tol in TOLERANCES:
            geo = error <= tol
            for deadline in DEADLINES:
                for tau in DURATION:
                    timely = 0.42 + np.array([5, 6]) * tau + travel / 30 <= deadline + 1e-12
                    success = geo & timely
                    five, six = success.T
                    totals.append(
                        dict(
                            block=b,
                            tolerance_mm=tol,
                            deadline_s=deadline,
                            contact_s=tau,
                            fixtures=len(chosen),
                            geom5=geo[:, 0].sum(),
                            geom6=geo[:, 1].sum(),
                            timely5=timely[:, 0].sum(),
                            timely6=timely[:, 1].sum(),
                            both=(five & six).sum(),
                            only5=(five & ~six).sum(),
                            only6=(six & ~five).sum(),
                            neither=(~five & ~six).sum(),
                            pass5=five.sum(),
                            pass6=six.sum(),
                        )
                    )
    return totals


if __name__ == "__main__":
    rows = trials()
    save("fixtures.csv", rows)
    save("timing_frontier.csv", summaries(rows))
