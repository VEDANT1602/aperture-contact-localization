# Four rim contacts — revision supplement

The primary six-policy simulation uses seed 1707. The archived program and 96-row results are at [commit 71f76e7](https://github.com/VEDANT1602/aperture-contact-localization/tree/71f76e74192e47e6b9f4c19350aa7b4fb924cb4a). For the original data, follow its README and run its verification script.

This supplement uses a separate implementation of the scan intersections (a Schur complement) and clearance conversion. The default run uses seed 2207 for a second set of 2,000 simulated starts per radius. It writes 96 rows of replication results and 21 rows of matched-angle/noise sensitivity results. The endpoint noise standard deviation changes in the latter grid while the tracking noise remains fixed at 0.06 mm per axis. The same normally distributed draws and center coordinates are reused across sensitivity cells. These are simulations without measured robot data.

From this directory:

```sh
python -m pip install -r requirements.txt
python run.py
```

To check the independent formulas against every primary condition, use a local checkout of the pinned repository:

```sh
python run.py --compare-archive /path/to/aperture-contact-localization/results.csv
```

The comparison checks every observability, attempt and seating count, and mean duration and force proxy to the precision recorded in the archived CSV. The script also tests exact reconstruction without endpoint noise and identical fixed-axis decisions for circular openings. The seed-2207 results are supplementary, independently generated quantities. Input physical tolerances and synthetically generated loads are assumptions.

Verified in Python 3.12.14 with NumPy 2.3.5. The original repository pins NumPy 1.26.0 for its original workflow.

## Environment lock

Create separate Linux x86_64 virtual environments with CPython 3.12.14 for the revision and 3.11.9 for the baseline. In the activated revision environment run `python -m pip install --require-hashes -r revision-cp312-linux-x86_64.lock`. For the original checkout, install `baseline-cp311-linux-x86_64.lock` the same way in the baseline environment, then run the commands above. The baseline lock applies to the public simulator. The revision lock covers every numerical revision script and the optical image replay. The lock headers identify the platform; the baseline transitive pins reconstruct a compatible environment for the published direct requirements.

## Fixed contact budgets and optical rim replay

Run `python contact_budgets.py` to compare fixed and sequential scans, known-shape algebraic least squares and a direct ellipse-specific fit on 2,000 paired starts. The same draws are used for the four-, five- and six-contact budgets. The output separates observable scans, numerical fits, time-limited attempts and geometric successes; the five-contact policy reads the first end of the oblique chord. The original 0.22 s/contact budget makes many sixth contacts uneconomic at 1.8 s, so both a 1.8 s and a 2.1 s deadline are reported.

For the optical check, obtain [Calibration.zip at the pinned mirror commit](https://raw.githubusercontent.com/zikai1/Awesome-Ellipse-Detection/4003bef55e929db0797a4586cf352a21c64e3ab1/Calibration.zip). SHA-256 `a41f0566347036aec88cd3e58e3fcd029850bdfc912038654259bf3af2b25c7f`. Run `python photo_rims.py /path/to/Calibration.zip` in this directory. The script checks the archive hash, reads all 20 ring-board JPEGs in memory, and writes per-reference and per-image summaries. The package distributes calculation results only. The upstream [annotation project](https://github.com/viorik/ELSDc) credits Higuchi and colleagues for the camera calibration photographs. Each result refers to an annotated, projected inner contour. Multiple rings and viewpoints share targets; there is no experiment on touch or insertion.
