"""Check the aperture study's archived condition summaries using the standard library."""
import csv
from itertools import product
from math import isclose, sqrt
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    with Path(__file__).with_name("results.csv").open(newline="") as stream:
        records = list(csv.DictReader(stream))
    radii = (0.5, 2.5, 4.5, 6.5)
    friction = (0.12, 0.55)
    methods = ("direct", "x_only", "midpoints", "recenter", "cad", "cad_plus15")
    expected = set(product(radii, ("round", "oval"), friction, methods))
    indexed = {(float(r["radius_mm"]), r["shape"], float(r["mu"]), r["method"]): r for r in records}
    require(len(records) == len(expected) and indexed.keys() == expected, "Condition grid differs")
    for key, row in indexed.items():
        trials, visible, attempted, seated = map(int, (row["trials"], row["observable"], row["attempted"],
                                                      row["successful"]))
        require(0 <= seated <= attempted <= visible <= trials == 2000, f"Denominators: {key}")
        if row["gains_vs_midpoint"] != "":
            reference = int(indexed[key[:3] + ("midpoints",)]["successful"])
            gain, loss = int(row["gains_vs_midpoint"]), int(row["losses_vs_midpoint"])
            require(0 <= gain <= min(seated, trials-reference) and 0 <= loss <= min(reference, trials-seated),
                    f"Paired reversal bounds: {key}")
            require(seated - reference == gain - loss, f"Paired counts: {key}")
    for radius, mu in product(radii, friction):
        circle = [indexed[radius, "round", mu, method] for method in ("midpoints", "cad")]
        require(all(row["gains_vs_midpoint"] == "0" and row["losses_vs_midpoint"] == "0" for row in circle),
                f"Circle decision disagreement: radius {radius}, friction {mu}")
    study = [indexed[4.5, "oval", 0.55, method] for method in methods]
    require([int(row["successful"]) for row in study] == [14, 207, 39, 333, 1962, 286], "Seating counts differ")
    require([round(float(row["mean_cycle_s"]), 3) for row in study] == [.420, .938, 1.410, 1.396, 1.401, 1.404],
            "Cycle times differ")
    matched = indexed[4.5, "oval", 0.55, "cad"]
    n = int(matched["trials"])
    gains, losses = int(matched["gains_vs_midpoint"]), int(matched["losses_vs_midpoint"])
    diff = (gains - losses) / n
    se = sqrt(((gains + losses) / n - diff**2) / (n - 1))
    require(isclose(diff, 0.9615) and round(100*(diff-1.96*se), 2) == 95.30
            and round(100*(diff+1.96*se), 2) == 97.00, "Paired interval differs")
    wider = indexed[6.5, "oval", 0.55, "cad"]
    require((int(wider["successful"]), int(wider["attempted"])) == (1688, 1718), "Wide-offset outcomes differ")
    print("Verified 96 conditions, equal circle decisions, and a paired oval gain of 96.15 percentage points.")


if __name__ == "__main__":
    main()
