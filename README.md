# What four, five and six rim contacts identify about an elliptical aperture

Vedant Thaker · November 21, 2026

Four endpoints on perpendicular scan lines can localize an elliptical opening if the shape is known. With an unknown shape, even its center can be ambiguous.

- [Revised manuscript (PDF)](manuscript.pdf) · [Editable manuscript](manuscript.md)
- [Revision code, results and reproduction instructions](revision/supplement/) · [Preparation record](revision/PREPARATION.md)
- [Baseline software and results at the study commit](https://github.com/VEDANT1602/aperture-contact-localization/tree/71f76e74192e47e6b9f4c19350aa7b4fb924cb4a) · [Software license](LICENSE) · [Third-party terms](LICENSING.md)

## Earlier study and reproduction instructions

The following instructions and results describe the original study. The revised paper and its supplemental tests are linked above.

### Locating a rotated oval from four rim contacts

On a circle, the midpoint of a horizontal chord gives the center's horizontal coordinate even when the scan misses the centerline. With a rotated oval, that coordinate depends on the height of the scan. Four contacts can therefore produce a repeatable but seriously misplaced center estimate.

In the high-friction simulation, the same 2,000 starts were drawn within 4.5 mm of the nominal center of a 35-degree oval. Independent horizontal and vertical midpoints seated 39 pegs. Solving the two chord equations with the known shape seated 1,962. Getting the assumed angle wrong by 15 degrees dropped that to 286. The two fixed-axis estimators seated the same 1,997 pegs on the circular control. [Six methods on the oval](results.csv?plain=1#L68) · [Noise-free center check](run.py#L52)

## Which attempts belong in the denominator?

Enlarging the offset radius to 6.5 mm sometimes puts a scan line outside the aperture. The geometry-aware method seated 1,688 pegs. That is 98.3% of its 1,718 observable, attempted cases, and 84.4% of all 2,000 starts. Counting only attempts would conceal the cost of missing a chord.

The simulator uses noisy probe endpoints, a fixed peg orientation and an assigned load proxy. Assessing fit and contact force on a part would require independent physical measurements. [Condition summaries](results.csv) · [Geometry and assumptions](https://github.com/VEDANT1602/aperture-contact-localization/blob/71f76e74192e47e6b9f4c19350aa7b4fb924cb4a/manuscript.md) · [Paper PDF](https://github.com/VEDANT1602/aperture-contact-localization/blob/71f76e74192e47e6b9f4c19350aa7b4fb924cb4a/manuscript.pdf)

## Reproduce and check

Run in the repository root with Python 3.11 and the dependency listed in [requirements.txt](requirements.txt).

```shell
python -m pip install -r requirements.txt
python run.py
python verify.py
```

[run.py](run.py) generates all test cases locally and writes the condition summaries to [results.csv](results.csv). [verify.py](verify.py) reads those summaries with the standard library, checks the condition grid and denominators, and recomputes the paired success difference. The verifier also compares the two circle estimators over every radius and friction setting. It runs on the archived CSV without installing NumPy.

Maintained by Vedant Thaker.
