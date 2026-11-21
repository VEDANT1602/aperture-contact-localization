# What four, five and six rim contacts identify about an elliptical aperture

**Vedant Thaker**  
Independent Researcher, Jeffersonville, Indiana, United States  
Correspondence: vthaker1@asu.edu  
21 November 2026

## Abstract

Four endpoints on perpendicular scan lines can localize an elliptical opening if the shape is known. With an unknown shape, even its center can be ambiguous. On a simulated 35° ellipse, independent chord midpoints seated 39 of 2,000 pegs and the shape-corrected midpoint seated 1,962. A fresh comparison held time and contact budgets fixed. Under a 1.8 s deadline, a known-shape least-squares estimate seated 1,998 pegs with five contacts and 335 with six. The sixth reading often exhausted the correction time. When the deadline rose to 2.1 s, known-shape and freely fitted six-point ellipses seated 2,000 and 1,758, respectively. A separate optical check used intensity crossings on 20 photographed ring-board frames. The median of per-image median center errors was 0.460 pixels for independent midpoints and 0.435 for the annotation-shape correction. The photographs test rim geometry with a privileged shape prior. They provide no tactile or insertion outcomes.

## What four endpoints identify

An off-center horizontal chord in a circle has the same horizontal midpoint as the circle center. For a rotated ellipse, motion across the scan line also changes the midpoint along the scan. This study asks which errors can be removed by interpreting the same contacts differently and when an extra contact is worth its time cost.

Contact-rich assembly systems can use compliance and active observations to handle uncertain part location [1,2]. Whitney’s analysis links geometric and force equilibria in rigid-part mating [3]. This simulation isolates an observation problem upstream of that mechanics: how to infer the center from two pairs of endpoints when shape is known.

## Observation equation and conditioning

Let c = (cₓ, cᵧ) be the unknown center and let Q be the symmetric positive-definite matrix obtained by rotating diag(1/a², 1/b²) into the scan frame. The rim is the set of points p satisfying (p − c)ᵀ Q (p − c) = 1. Substitution of y = 0 yields a quadratic in x. Its roots have midpoint mₓ = cₓ + (Qₓᵧ/Qₓₓ)cᵧ. The vertical scan at x = 0 gives mᵧ = cᵧ + (Qₓᵧ/Qᵧᵧ)cₓ. Writing the two equations as m = Ac defines A with unit diagonal and those two off-diagonal ratios. Its determinant equals det(Q)/(QₓₓQᵧᵧ) and is positive. When both chords exist, their midpoints therefore determine c under the given Q.

The simulated ellipse has semiaxes 7.0 and 3.5 mm and major-axis angle 35°. The cross-axis coefficients are approximately −0.709 and −0.468. A 2 mm vertical translation with zero horizontal translation shifts the horizontal midpoint by −1.42 mm. Solving the system eliminates this deterministic bias under the correct geometry. The matrix has 2-norm condition number 3.81, so measurement perturbations still propagate. For a circle with 5 mm radius, A is the identity.

A general planar conic has five independent parameters up to normalization [4]. The four axis intercepts (−1,0), (3,0), (0,−2), (0,1) give a concrete ambiguity. Every curve x² + λxy + 1.5y² − 2x + 1.5y − 3 = 0 has those intercepts. At λ = 0 the center is (1,−0.5); at λ = 1 the ellipse has center (1.5,−1). Both quadratic forms are positive definite. A fifth point in general position constrains the remaining degree of freedom. Noise and near-degenerate geometry can still make that just-determined estimate unstable.

## Paired simulation and seating rule

The primary experiment drew 2,000 centers uniformly by area in each of four offset disks of radius 0.5, 2.5, 4.5 and 6.5 mm (seed 1707). Each probe searched ±12 mm from its scan origin. A chord counted as observable only when physically present with both endpoints in range. Independent Gaussian endpoint and per-coordinate tracking errors had standard deviations of 0.12 and 0.06 mm, respectively. Policies, friction settings and shapes shared draws within each radius.

The direct policy uses the nominal center. The horizontal policy applies only the first midpoint. Independent midpoints combines two nominal-axis chords. Sequential recentering moves the vertical scan to the measured horizontal midpoint. The remaining policies solve the coupled equations using either the true Q or an angle 15° too high. In this mismatch test the physical peg orientation remains aligned with the actual opening.

The peg section has the same axes and orientation as the opening and is scaled by 0.92. For residual error e, let ρ = √(eᵀQe). The affine map that turns the aperture into a unit disk makes the peg a disk of radius 0.92, so exact geometric containment is equivalent to ρ ≤ 0.08. A separate lead-in assumption permits seating up to ρ = 0.18 when the assigned friction coefficient is below 0.35. Here the behavior attributed to friction is a threshold assumption rather than a fitted physical contact law. The two modeled friction values are 0.12 and 0.55.

Each probe costs 0.22 s. An insertion attempt costs 0.42 s plus correction distance divided by 30 mm/s, under a 1.8 s budget. Missing a required chord ends the trial after the allocated probe time. The peak-load proxy is the maximum of a 0.75 N probe load when probing occurs and a first-approach load, capped at 5 N, of 0.65 N plus 1.4 N/mm of interference beyond the clearance boundary along the correction-error ray. A zero-attempt trial has no first-approach load. These parameters prescribe how the benchmark scores time and force.

## Equal-contact comparisons

At the 4.5 mm offset radius all required chords were available on the ellipse. The four-contact shape-matched solver changed 1,924 failures of the independent-midpoint policy into successes and reversed one success. The paired difference of 96.15 percentage points has an approximate pointwise 95% Monte Carlo interval of 95.30–97.00 points, computed from the sample standard deviation of per-start differences divided by √2,000. The interval reflects variation among starts under this generator. 

On the circular control, independent midpoints and the matched solver made the same decision on every trial. Both seated 1,997 of 2,000 in the corresponding strict-clearance cell. On the ellipse, allowing the low-friction lead-in increased the counts to 234 and 2,000. At a 6.5 mm offset radius under the strict rule, only 1,718 paired fixed-axis scans were observable. The coupled solver seated 1,688 pegs, or 98.3% of attempts and 84.4% of all starts.

| Policy | Touches | Seats / 2,000 | Mean time (s) | Load proxy (N) |
| --- | --- | --- | --- | --- |
| Direct | 0 | 14 | 0.420 | 4.038 |
| Horizontal only | 2 | 207 | 0.938 | 3.097 |
| Independent midpoints | 4 | 39 | 1.410 | 2.626 |
| Recenter second scan | 4 | 333 | 1.396 | 2.128 |
| Matched ellipse | 4 | 1,962 | 1.401 | 0.751 |
| Assumed angle +15° | 4 | 286 | 1.404 | 1.387 |

Table 1. Primary 35° ellipse, 4.5 mm offset radius and strict clearance (μ = 0.55). Cycle times and peak proxy loads are means across all starts.

## Orientation error and endpoint precision

A separate implementation draws a fresh matched sample (seed 2207) and changes the assumed angle and endpoint-noise scale jointly. At the original noise level, the independent midpoints seated 35 of 2,000 and the matched solver seated 1,975. The full grid includes ±30° errors. Table 2 shows the smaller errors most relevant to calibration. The opposite signs at 15° produce very different counts because the scanning axes remain fixed as the assumed shape rotates. The signs therefore need separate tests. Sensitivity to increased endpoint noise is also apparent at the correct angle.

| Assumed minus true angle | 0.06 mm | 0.12 mm | 0.24 mm |
| --- | --- | --- | --- |
| −15° | 893 | 885 | 785 |
| −5° | 1,791 | 1,676 | 1,320 |
| 0° | 2,000 | 1,975 | 1,518 |
| +5° | 1,627 | 1,488 | 1,126 |
| +15° | 307 | 306 | 285 |

Table 2. Seats out of 2,000 fresh synthetic starts, by endpoint standard deviation. The tracked peg is aligned. Its coordinate error stays at 0.06 mm per axis in every cell.

## A matched contact and time budget

In a separate paired sample (seed 21707, 2,000 starts), four fixed-axis contacts provide the two chord midpoints. For known Q, a second estimator expands the conic equation and regresses the centered values of pᵀQp on 2(p − mean(p))ᵀQ to estimate c. It can use unequal numbers of endpoints. For unknown Q, an ellipse-specific least-squares fit minimizes the algebraic residual subject to 4AC − B² = 1 [5]. Center and scale normalization condition the fit; the final center solves the fitted gradient equations. Four-point free fits are excluded by the constructive ambiguity above.

The fifth contact is the first endpoint of a 45° line through the provisional independent midpoint; the sixth is its opposite endpoint. Known-shape and free-ellipse fits use exactly the same observed points. The sequential midpoint policy instead alternates horizontal, vertical, horizontal chords through the latest estimated coordinates. It has complete estimates after four or six touches. All policies share centers, endpoint-noise draws, tracking errors and the per-touch time charge. Geometry-only success checks ignore the clock; the two timed scores charge the same modeled duration to every contact. Extra travel between scan origins is omitted.

With five contacts, free fitting had 1,281 geometric successes and a 19.41 mm root-mean-square center error, indicating extreme estimates on some noisy configurations. Six contacts reduced its RMS error to 0.633 mm and improved geometric seating to 1,758. Under the tighter deadline those same six contacts left little time for the center correction. The original rule permits only 1.8 mm of commanded correction after six touches (30 × (1.8 − 6 × 0.22 − 0.42)).

| Touches | Estimator | Contained¹ | Seats at 1.8 s | Seats at 2.1 s |
| --- | --- | --- | --- | --- |
| 4 | Independent midpoints | 47 | 47 | 47 |
| 4 | Sequential midpoints | 360 | 360 | 360 |
| 4 | Coupled midpoints | 1,973 | 1,973 | 1,973 |
| 4 | Known-shape LS | 1,983 | 1,983 | 1,983 |
| 5 | Known-shape LS | 1,998 | 1,998 | 1,998 |
| 5 | Free ellipse LS | 1,281 | 1,281 | 1,281 |
| 6 | Sequential midpoints | 620 | 249 | 620 |
| 6 | Known-shape LS | 2,000 | 335 | 2,000 |
| 6 | Free ellipse LS | 1,758 | 341 | 1,758 |

Table 3. Counts out of the same 2,000 starts. ¹Peg footprints geometrically contained before the time check, including tracking error. Every scheduled endpoint was observable and every listed estimator returned a finite center in this sample.

## Image-plane check on photographed ring targets

The calibration-pattern collection contains physical-camera images of concentric rings with manually annotated projected contours [6]. The calculation used all 20 ring-board images in the pinned JPEG distribution [7]. An annotation counted as an inner contour when a companion ellipse had a center within 3 pixels and a major semiaxis at least 1.3 times larger (strict inequality in code). This rule admitted 1,455 candidate annotations. The initial scan point was offset from the annotated center by (0.28b, −0.32b), where b is the annotated minor semiaxis. The scan searches for the first light-to-dark threshold crossing along each direction in real, bilinearly sampled grayscale pixels; it never substitutes analytical ellipse intersections. The threshold is the midpoint of the local 10th and 90th intensity percentiles. The annotation supplies localization, search scale, the reference center and, for known-shape methods only, Q.

All five methods returned estimates for the same 1,437 candidate annotations. Taking the median within each image and then the median across images gave 0.460 pixels for independent midpoints, 0.435 for coupled midpoints, 0.443 for four-point known-shape least squares, 0.470 for five-point free fitting and 0.475 for six-point free fitting. For the first two estimators, per-image medians ranged from 0.412 to 0.555 and from 0.404 to 0.495 pixels. The small optical difference shows how little of the large seating contrast necessarily transfers even to another rim-localization problem. The shared annotation can favor the known-shape methods. The repeated views are clustered, and the plotted contours are not metrically surveyed aperture centers.

## Scope and physical test

The independent-midpoint error follows from conic geometry. The number of failed insertions depends on how often that error crosses the chosen clearance. Exact conic intersections, a known aspect ratio and an aligned rigid peg favor the matched solver. Rotation of the physical peg, bevels, compliance, ambiguous rim contacts and non-Gaussian endpoint errors would change the observation or seating law. The capped load proxy cannot test contact peaks or part damage.

A physical touch study needs independent shape calibration on a second artifact, finite probe-radius correction, repeated scans at measured yaw, and a denominator that includes missing contacts. Probe alignment, mechanical filtering and tip compensation can bias a real rim measurement [8]. The optical comparison cannot estimate these effects, and assumed loads and friction thresholds do not validate contact dynamics.

## Data and code availability

The baseline repository contains the original simulation and verifier. The accompanying supplement supplies the independent replay (run.py), contact_budgets.py, photo_rims.py, all resulting CSVs and hash-locked Linux requirements. Obtain the checksum-verified ring-board archive from [7] to repeat the optical analysis. The raw photographs remain with their provider.

[Pinned baseline](https://github.com/VEDANT1602/aperture-contact-localization/tree/71f76e74192e47e6b9f4c19350aa7b4fb924cb4a) · [Revision code and data](https://github.com/VEDANT1602/aperture-contact-localization/tree/main/revision/supplement) · [Preparation record](https://github.com/VEDANT1602/aperture-contact-localization/blob/main/revision/PREPARATION.md)

## Computational verification

The original re-execution matched the 96-row archived results.csv byte for byte. The independent implementation matched the 96 primary condition counts. The budget extension verifies center recovery from five and six generic noise-free points; its CSV records every method and both deadlines. The optical replay checks the image archive SHA-256 before reading measurements. Numeric checks used Python 3.12.14, NumPy 2.3.5 and Pillow 13.0.0.

## Author contribution

Vedant Thaker is the sole author. He designed the original rim-contact localization study, wrote its manuscript, developed its original software, and requested the comparisons and checks reported in this revision.

## Use of computational assistance

OpenAI Codex assisted with the identifiability analysis, numerical contact- and time-budget comparisons, the photographed-rim extraction and replay, and code and citation checks, as well as literature checks and preparation of the revised text. The author set the research question and requested the revision.

## Funding

This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors.

## Competing interests

The author declares no competing interests.

## References

[1] Y. Chen, K. Kimble, H. H. Qian, P. Chanrungmaneekul, R. Seney and K. Hang. Robust Peg-in-Hole Assembly under Uncertainties via Compliant and Interactive Contact-Rich Manipulation. Robotics: Science and Systems XXI, 2025. https://doi.org/10.15607/RSS.2025.XXI.060

[2] S. Kim and A. Rodriguez. Active Extrinsic Contact Sensing: Application to General Peg-in-Hole Insertion. IEEE International Conference on Robotics and Automation, 2022. https://doi.org/10.1109/ICRA46639.2022.9812017

[3] D. E. Whitney. Quasi-Static Assembly of Compliantly Supported Rigid Parts. Journal of Dynamic Systems, Measurement, and Control 104(1), 65–77, 1982. https://doi.org/10.1115/1.3149634

[4] R. Hartley and A. Zisserman. Multiple View Geometry in Computer Vision, 2nd ed., Cambridge University Press, 2004. §2.2.3, “Five points define a conic,” pp. 30–31. https://doi.org/10.1017/CBO9780511811685

[5] A. Fitzgibbon, M. Pilu and R. B. Fisher. Direct Least Square Fitting of Ellipses. IEEE Transactions on Pattern Analysis and Machine Intelligence 21(5), 476–480, 1999. https://doi.org/10.1109/34.765658

[6] V. Pătrăucean, P. Gurdjos and R. Grompone von Gioi. Joint A Contrario Ellipse and Line Detection. IEEE Transactions on Pattern Analysis and Machine Intelligence 39(4), 788–802, 2017. DOI 10.1109/TPAMI.2016.2558150. Project data collection: Dataset2_CalibrationPatterns. https://github.com/viorik/ELSDc

[7] zikai1 (repository maintainer). Awesome Ellipse Detection, Calibration.zip. JPEG mirror of the calibration-pattern collection and contour parameters; version 4003bef, accessed 21 November 2026. https://github.com/zikai1/Awesome-Ellipse-Detection/tree/4003bef55e929db0797a4586cf352a21c64e3ab1

[8] J. A. Stone, B. Muralikrishnan and C. Sahay. Geometric Effects When Measuring Small Holes With Micro Contact Probes. Journal of Research of the National Institute of Standards and Technology 116(2), 573–587, 2011. https://doi.org/10.6028/jres.116.006
