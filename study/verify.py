"""Check geometry with explicit substitution and timing from per-fit critical durations."""

import csv
from pathlib import Path
import numpy as np
from aperture_geometry import conic_fit

here = Path(__file__).resolve().parent
p = np.array([[-1, 0], [3, 0], [0, -1], [0, 3]])
for beta in [0, 0.5]:
    Q = np.array([[1, beta], [beta, 1]])
    center = np.linalg.solve(Q, [1, 1])
    np.testing.assert_allclose(center, np.ones(2) / (1 + beta))
    assert np.all(np.einsum("ij,jk,ik->i", p, Q, p) - 2 * p.sum(axis=1) - 3 == 0)
for k in (5, 6):
    angles = 2 * np.pi * np.arange(k) / k
    pts = np.c_[np.cos(angles), np.sin(angles)] @ np.array([[0.8, 1.1], [3.1, 0.2]]) + [1, 2]
    np.testing.assert_allclose(conic_fit(pts), [1, 2], atol=1e-9)
with (here / "fixtures.csv").open() as f:
    fixtures = list(csv.DictReader(f))
assert len(fixtures) == 3200
for row in csv.DictReader((here / "timing_frontier.csv").open()):
    b = int(row["block"])
    subset = fixtures if b == 0 else fixtures[400 * (b - 1) : 400 * b]
    t, tau, eps = [float(row[key]) for key in ["deadline_s", "contact_s", "tolerance_mm"]]
    counts = dict(both=0, only5=0, only6=0, neither=0)
    for trial in subset:
        passes = [
            float(trial[f"error_{k}"]) <= eps
            and tau <= (t - 0.42 - float(trial[f"travel_{k}"]) / 30) / k + 1e-12
            for k in (5, 6)
        ]
        counts[
            {
                (True, True): "both",
                (False, False): "neither",
                (True, False): "only5",
                (False, True): "only6",
            }[tuple(passes)]
        ] += 1
    assert all(v == int(row[key]) for key, v in counts.items())
    assert counts["both"] + counts["only5"] == int(row["pass5"])
    assert counts["both"] + counts["only6"] == int(row["pass6"])
print("Four-point ambiguity, clean conic centers, and all timing contingency tables verified.")
