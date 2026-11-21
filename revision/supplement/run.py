"""Independent reconstruction of the paired planar insertion benchmark."""
from pathlib import Path
import csv
import argparse
import math
import numpy as np

OUT = Path(__file__).resolve().parent
SEED = 2207
N = 2_000
RADIUS = (0.5, 2.5, 4.5, 6.5)
POLICIES = ("direct", "horizontal", "independent", "recenter", "known", "misaligned")


def shape(axes, angle):
    theta = math.radians(angle)
    rotation = np.array([[math.cos(theta), -math.sin(theta)],
                         [math.sin(theta), math.cos(theta)]])
    return rotation @ np.diag(np.reciprocal(np.square(axes))) @ rotation.T


def chord_map(q):
    return np.array([[1.0, q[0, 1] / q[0, 0]], [q[1, 0] / q[1, 1], 1.0]])


def chord(centers, q, axis, fixed_coordinate, errors):
    # Solve the quadratic in the free scan coordinate, relative to center.
    other = 1 - axis
    delta = fixed_coordinate - centers[:, other]
    midpoint = centers[:, axis] - q[axis, other] / q[axis, axis] * delta
    radicand = (1.0 - np.linalg.det(q) / q[axis, axis] * delta**2) / q[axis, axis]
    half = np.sqrt(np.maximum(0, radicand))
    observable = (radicand >= 0) & (midpoint - half >= -12) & (midpoint + half <= 12)
    # Search range is applied to physical endpoints, before sensing noise.
    return midpoint + errors.mean(axis=1), observable


def solve(axes, angle, centers, noises, tracking, friction, mismatch=15):
    q = shape(axes, angle)
    m = chord_map(q)
    x, seen_x = chord(centers, q, 0, 0, noises[:, :2])
    y, seen_y = chord(centers, q, 1, 0, noises[:, 2:])
    y_shift, seen_shift = chord(centers, q, 1, x, noises[:, 2:])
    mids = np.column_stack([x, y])
    noise_free = mids - np.column_stack([noises[:, :2].mean(axis=1), noises[:, 2:].mean(axis=1)])
    seen = seen_x & seen_y
    np.testing.assert_allclose(np.linalg.solve(m, noise_free[seen].T).T,
                               centers[seen], rtol=0, atol=2e-12)
    estimates = (
        (np.zeros_like(mids), np.ones(len(x), dtype=bool), 0),
        (np.column_stack([x, np.zeros_like(x)]), seen_x, 2),
        (mids, seen, 4),
        (np.column_stack([x, y_shift]), seen_x & seen_shift, 4),
        (np.linalg.solve(m, mids.T).T, seen, 4),
        (np.linalg.solve(chord_map(shape(axes, angle + mismatch)), mids.T).T, seen, 4),
    )
    details = {}
    for name, (estimate, observed, count) in zip(POLICIES, estimates):
        error = estimate - centers + tracking
        rho = np.sqrt(np.einsum("ni,ij,nj->n", error, q, error))
        duration = count * .22 + np.where(observed, .42 + np.linalg.norm(estimate, axis=1) / 30, 0)
        completed = observed & (duration <= 1.8)
        success = completed & (rho <= (.18 if friction < .35 else .08))
        world_overlap = np.linalg.norm(error, axis=1) * np.maximum(0, 1 - .08 / np.maximum(rho, 1e-100))
        approach = np.where(completed, np.minimum(5, .65 + 1.4 * world_overlap), 0)
        peak = np.maximum(.75 if count else 0, approach)
        details[name] = (observed, completed, success, np.minimum(duration, 1.8), peak)
    if axes[0] == axes[1]:
        assert np.array_equal(details["independent"][2], details["known"][2])
    return details


def write(name, rows):
    with (OUT / name).open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def simulate(seed):
    rng = np.random.default_rng(seed)
    summary, sensitivity = [], []
    for radius in RADIUS:
        theta = rng.uniform(-np.pi, np.pi, N) if seed == 1707 else rng.uniform(0, 2*np.pi, N)
        centers = (radius*np.sqrt(rng.random(N)))[:,None] * np.column_stack([np.cos(theta), np.sin(theta)])
        noises = rng.normal(0, .12, (N, 4))
        tracking = rng.normal(0, .06, (N, 2))
        for geometry, axes, angle in (("circle", (5., 5.), 0), ("ellipse", (7., 3.5), 35)):
            for friction in (.12, .55):
                result = solve(axes, angle, centers, noises, tracking, friction)
                baseline = result["independent"][2]
                for name, (seen, completed, success, duration, peak) in result.items():
                    summary.append(dict(radius_mm=radius, geometry=geometry, friction=friction, policy=name,
                        total=N, observed=seen.sum(), within_budget_and_observed=completed.sum(), seated=success.sum(),
                        gains_vs_independent=(success & ~baseline).sum(), losses_vs_independent=(~success & baseline).sum(),
                        mean_s=duration.mean(), mean_force_proxy_N=peak.mean()))
                if radius == 4.5 and geometry == "ellipse" and friction == .55:
                    for offset in (-30, -15, -5, 0, 5, 15, 30):
                        trial = solve(axes, angle, centers, noises, tracking, friction, mismatch=offset)
                        for scale in (.5, 1., 2.):
                            if scale != 1.:
                                trial_scaled = solve(axes, angle, centers, noises*scale, tracking, friction, mismatch=offset)
                            else:
                                trial_scaled = trial
                            seen, _, success, _, _ = trial_scaled["misaligned"]
                            sensitivity.append(dict(assumed_minus_true_deg=offset, endpoint_sd_mm=.12 * scale,
                                tracking_sd_mm=.06, total=N, observed=seen.sum(), seated=success.sum()))
    return summary, sensitivity


def compare(primary_csv):
    rows, _ = simulate(1707)
    names = dict(direct="direct", horizontal="x_only", independent="midpoints", recenter="recenter", known="cad", misaligned="cad_plus15")
    with primary_csv.open(newline="") as stream:
        old_rows = list(csv.DictReader(stream))
    assert len(old_rows) == len(rows) == 96
    for a, b in zip(rows, old_rows):
        assert names[a["policy"]] == b["method"]
        assert ("round" if a["geometry"] == "circle" else "oval") == b["shape"]
        assert a["radius_mm"] == float(b["radius_mm"]) and a["friction"] == float(b["mu"])
        for new, old in (("observed", "observable"), ("within_budget_and_observed", "attempted"), ("seated", "successful")):
            assert a[new] == int(b[old])
        for new, old in (("mean_s","mean_cycle_s"), ("mean_force_proxy_N","mean_peak_N")):
            assert abs(a[new] - float(b[old])) <= 5.01e-7
    print("Independent formula matched observed, attempted, seated counts and mean time/load across all 96 archived cells.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--compare-archive", type=Path, help="Optional archived primary results.csv (seed 1707)")
    args = parser.parse_args()
    if args.compare_archive:
        compare(args.compare_archive)
    summary, sensitivity = simulate(SEED)
    write("replication.csv", summary)
    write("sensitivity.csv", sensitivity)


if __name__ == "__main__":
    main()
