# Four rim contacts can mislocate a rotated aperture

**Vedant Thaker**  
Working paper · 18 November 2026

## Abstract

Two opposite touches locate the center of a circular aperture along the scan axis. Does the midpoint of a horizontal chord and the midpoint of a vertical chord also give the center of a rotated ellipse? Six insertion strategies face the same simulated part displacements and tracking errors. On a circle, independent midpoints and a shape-aware method give identical seating decisions. On an ellipse rotated 35 degrees, with offsets within a 4.5 mm disk, combining the two midpoints seated 39 of 2,000 pegs under the high-friction rule. Solving two coupled equations seated 1,962 with the same four contacts. An orientation assumption wrong by 15 degrees reduced that count to 286. With offsets spanning a 6.5 mm disk, a scan could miss the opening altogether. The calculation distinguishes a mistaken interpretation of a touch from the failure to obtain a touch in the first place.

## What does a pair of touches measure?

A robot can obtain an excellent reading of the wrong coordinate. Imagine a horizontal scan across a long diagonal slot. A probe finds the left rim, crosses the opening and finds the right rim. Their average lies halfway along that chord. Moving the scan line up changes its midpoint even though the slot never moves. If the aperture is circular, the midpoint's horizontal coordinate happens to stay fixed. A tactile routine tested only on round holes can therefore appear more general than it is.

Chen and colleagues use collision-inclusive interaction and compliance to localize a hole and refine insertion under uncertainty [1]. Kim and Rodriguez actively estimate environmental contact and use the resulting evidence in a policy for different peg shapes [2]. Whitney analyzes geometric and force equilibrium in the mating of compliantly supported rigid parts [3]. This paper investigates one smaller observation problem. Given the positions where two known scan lines cross a rim, which information about the aperture center is present, and which assumptions must the estimator supply? The benchmark neither implements those published robot systems nor evaluates their performance. Its contribution is a controlled counterexample and a same-contact correction with a known answer.

## Geometry of a displaced opening

Write the boundary as (p-c)ᵀ Q (p-c) = 1. The aperture center c is unknown. Q is a positive-definite matrix formed by rotating diag(1/a², 1/b²) into the world frame. A horizontal line through y = 0 intersects the ellipse at two roots of a quadratic in x. Averaging those roots cancels the square-root term. The horizontal midpoint is c_x + (Q_xy/Q_xx)c_y. The analogous vertical midpoint is c_y + (Q_xy/Q_yy)c_x. Thus the midpoint vector equals A c, where A has diagonal entries one and the two corresponding off-diagonal ratios. Since det(A) = det(Q)/(Q_xx Q_yy) is positive, both chords determine the center when Q is known and both scans intersect.

For the test ellipse, a = 7 mm, b = 3.5 mm and the major axis is rotated 35 degrees. The two cross-axis coefficients are approximately -0.709 and -0.468. A center displaced 2 mm vertically and zero horizontally therefore yields a horizontal midpoint near -1.42 mm. Repeating the same scan with a quieter sensor cannot eliminate that error. Solving A c = m can, although the matrix's two-norm condition number of 3.81 means that endpoint noise is also transformed. The circular control has a = b = 5 mm and A is the identity.

## Paired scans and a fixed insertion budget

For each of four offset radii (0.5, 2.5, 4.5 and 6.5 mm), 2,000 centers are drawn uniformly by area inside a disk. Each simulated probe searches within ±12 mm of its local scan origin. An axis is observed only if the line intersects the aperture and both endpoints lie in range. Each reported endpoint has independent Gaussian noise of standard deviation 0.12 mm. The peg tracking error adds an independent 0.06 mm standard deviation per coordinate. The same center, endpoint errors and tracking error are reused across policies, geometries and friction settings within a radius. These are matched comparisons using artificial parts. The oval is a geometry transfer test, with no fitted parameters.

The direct policy inserts at the nominal center. The one-axis policy uses two contacts to correct x alone. Independent midpoints combines four contacts on fixed nominal axes. Sequential recentering takes the same horizontal pair, moves the vertical scan to that estimated x and uses its new midpoint for y. The CAD policy solves the two equations using the known aperture shape and orientation. A calibration stress test gives this estimator an orientation 15 degrees too large. In the circular control that perturbation has no geometric effect.

The peg section is the target ellipse scaled by 0.92, with its orientation aligned to the actual aperture. For a center displacement e, clearance is exact when rho = sqrt(eᵀ Q e) is at most 0.08. This follows by transforming both sections to circles: a circle of radius 0.92 inside a unit circle can move its center by at most 0.08. A deliberately simple lead-in model also seats a peg at rho up to 0.18 when the friction coefficient is below 0.35. The two test coefficients are 0.12 and 0.55. Only this seating rule depends on friction. A single scalar threshold omits the multilateral contact mechanics treated in [3].

All policies have 1.8 simulated seconds. Each probe costs 0.22 s. An insertion attempt costs 0.42 s plus the length of the estimated correction divided by 30 mm/s. A missing required chord ends the trial after the allocated probe time. The force proxy is the larger of the probe load (0.75 N when used) and a first-approach load of 0.65 N plus 1.4 N/mm times radial interference beyond clearance, capped at 5 N. Radial interference is the world-space distance from the commanded offset to the clearance ellipse along that ray. This stylized spring law does not predict peaks during a real sliding insertion. A trial can finish quickly by failing.

## Which error survives equal contact counts?

Table 1 gives results for the oval, 4.5 mm offset radius and friction 0.55. Every trial had both required chords in range. The times and forces are modeled quantities, averaged over all 2,000 trials.

| Estimate | Touches | Seated / 2000 | Mean cycle, s | Mean peak proxy, N |
|---|---|---|---|---|
| Direct | 0 | 14 | 0.420 | 4.038 |
| Horizontal only | 2 | 207 | 0.938 | 3.097 |
| Independent midpoints | 4 | 39 | 1.410 | 2.626 |
| Recenter second scan | 4 | 333 | 1.396 | 2.128 |
| Known geometry | 4 | 1962 | 1.401 | 0.751 |
| Geometry rotated 15° too far | 4 | 286 | 1.404 | 1.387 |

Adding a second midpoint to the one-axis estimate decreased the seat count from 207 to 39. Its lower mean force still indicates that it often reduced radial interference. The two summaries answer different questions. Repositioning the second scan recovered some seats, while the remaining bias in the first coordinate limited the gain. Solving the coupled equations converted 1,924 failures of the independent-midpoint policy to successes and reversed one success. The paired difference is 96.15 percentage points, with an approximate 95% Monte Carlo interval of 95.30 to 97.00 points. The interval uses the standard error of the trial-wise success difference and reflects only sampling under this generator.

Two checks locate the failure more precisely. On the circle, both four-contact fixed-axis estimators seated the same 1,997 of 2,000 high-friction trials at 4.5 mm. On the oval at the same radius, allowing passive capture at friction 0.12 raised the independent-midpoint count to 234 and the known-geometry count to 2,000. Under high friction, moving from a 4.5 to a 6.5 mm offset radius left only 1,718 of 2,000 four-contact fixed-axis trials observable. The geometry-aware policy seated 1,688 of the 1,718 attempted pegs. Its conditional success of 98.3% would hide 282 missing observations if reported alone.

## Limitations and replication

The estimator assumes a rigid aperture with known axis lengths, an aligned peg, planar scans and distinct observable endpoints. The 15-degree mismatch experiment changes the estimator alone. Real peg yaw would also alter clearance. Surface bevels, tactile compliance, ambiguous edges and pose-dependent probing delays could invalidate the observation model before the algebra is applied. Exact conic intersections with Gaussian endpoint noise make the simulator particularly favorable to a matched conic estimator. A useful hardware test would fit the matrix from a measured rim, withhold a rotated aperture from calibration, and compare predicted and measured chord midpoints before attempting insertion.

Run python run.py using Python 3.10 or newer and NumPy. The script writes 96 rows to results.csv, including attempted and successful counts, mean estimation error on observable trials, and paired reversals. In a separate noise-free assertion the center reconstructed from every valid pair of chords agrees with the generating center within 2 × 10^-12 mm. The narrow conclusion is that the number of touches alone says little about the quality of a tactile estimate. The geometry assigned to those touches can decide whether the fourth reading helps.

## Research and writing assistance

Vedant Thaker supplied the research brief and source materials. OpenAI Codex assisted with study design, implementation, execution, literature review and drafting. Clever Humanizer suggested edits to the abstract. The final wording was checked against the analysis.

## References

[1] Y. Chen, K. Kimble, H. H. Qian, P. Chanrungmaneekul, R. Seney and K. Hang. Robust peg-in-hole assembly under uncertainties via compliant and interactive contact-rich manipulation. Robotics: Science and Systems XXI, 2025. https://www.roboticsproceedings.org/rss21/p060.html

[2] S. Kim and A. Rodriguez. Active extrinsic contact sensing: Application to general peg-in-hole insertion. IEEE International Conference on Robotics and Automation, 2022. https://arxiv.org/abs/2110.03555

[3] D. E. Whitney. Quasi-static assembly of compliantly supported rigid parts. Journal of Dynamic Systems, Measurement, and Control 104, 65–77, 1982. https://doi.org/10.1115/1.3149634
