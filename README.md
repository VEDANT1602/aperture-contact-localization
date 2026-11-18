# Four rim contacts can mislocate a rotated aperture

A horizontal chord through a circle has the same horizontal midpoint wherever it crosses the circle. Rotate an elliptical aperture and that property disappears. This study asks whether four rim contacts still identify the center, and whether a robot can use them to guide a peg into the opening.

**Maintainer** · Vedant Thaker  
**Research materials** · [Manuscript (PDF)](manuscript.pdf) · [Editable manuscript](manuscript.md) · [Condition-level results](results.csv)

## What the probe measures

The simulated probe records two endpoints on a horizontal scan and two on a vertical scan. For a rotated ellipse, the horizontal midpoint depends on both coordinates of the center. The vertical midpoint does too. With two observable chords and a known ellipse matrix, a two-equation linear system recovers the center exactly in the noise-free case.

The experiment draws 2,000 centers per offset radius. The policies share center positions, endpoint noise, tracking noise and a 1.8 s time limit. Four radii, two shapes, two friction settings and six methods give 96 condition summaries. Direct insertion and one-axis probing provide baselines. Recentering the second scan, solving with the known geometry and deliberately rotating that geometry by another 15 degrees test different uses of the contacts.

## Same four contacts, different outcomes

The oval has semiaxes 7 and 3.5 mm and is rotated 35 degrees. All 2,000 trials in the following comparison have offset radius at most 4.5 mm. The simulated high-friction rule requires a direct geometric fit.

| Estimate | Touches | Seated / 2,000 | Mean modeled cycle |
|---|---:|---:|---:|
| Direct | 0 | 14 | 0.420 s |
| Horizontal only | 2 | 207 | 0.938 s |
| Independent midpoints | 4 | 39 | 1.410 s |
| Recenter second scan | 4 | 333 | 1.396 s |
| Solve with known geometry | 4 | 1,962 | 1.401 s |
| Assumed rotation off by 15° | 4 | 286 | 1.404 s |

The circle provides a geometric control. Both four-contact fixed-axis estimators seated the same 1,997 pegs under equivalent conditions. On the oval, enlarging the offset radius to 6.5 mm made some chords impossible to observe. The geometry-aware estimate then seated 1,688 pegs out of 1,718 observable cases and 2,000 total starts. The different denominators matter when comparing a sensing policy that can abort with a direct policy that always attempts insertion.

## Reproduce and check

Run in the repository root with Python 3.11 and the dependency listed in [requirements.txt](requirements.txt).

```shell
python -m pip install -r requirements.txt
python run.py
python verify.py
```

[run.py](run.py) generates all test cases locally and writes the condition summaries to [results.csv](results.csv). [verify.py](verify.py) reads those summaries with the standard library, checks the condition grid and denominators, and recomputes the paired success difference. The verifier also compares the two circle estimators over every radius and friction setting. It runs on the archived CSV without installing NumPy.

## Limits of the experiment

The simulator supplies idealized scan lines with Gaussian endpoint errors. The ellipse orientation used by the peg is fixed, and the force column is an assigned spring-load proxy. The aperture geometry, probe calibration, actual seating and contact load would need independent measurement on physical parts before using these values to design an insertion process.
