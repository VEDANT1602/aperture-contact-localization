# When is there time for a sixth contact? A worked example in ellipse centering

Vedant Thaker  
Independent Researcher, Jeffersonville, Indiana, USA  
vedant.thaker1602@gmail.com

Worked geometry example · November 24, 2026

### Abstract

A sixth touch can improve an estimated aperture center and still leave too little time for the correction move. For a circular starting region of radius R and a center tolerance ε, an accurate fit can command at most R + ε of travel. This gives a sufficient time budget for any accurate fit. In a numerical illustration with one ellipse and 3,200 translated starts, five touches placed 1,434 centers within 0.25 mm and six placed 2,310 within tolerance. Under one assigned timing model, 200 ms per contact leaves time to reach every accurate six-contact estimate. At 220 ms only 514 of those estimates can be reached.

## The geometric ambiguity

Four axial contacts need not determine an ellipse’s center. The points (−1, 0), (3, 0), (0, −1) and (0, 3) lie on every conic in the family x² + 2bxy + y² − 2x − 2y − 3 = 0, for |b| < 1. Solving its two stationary-point equations gives center (1, 1) at b = 0 and (2/3, 2/3) at b = 1/2. A fifth point in general position determines a noiseless conic up to scale [1]. In a noisy sample, an additional chord endpoint can stabilize the estimate.

The numerical illustration translates a 7 × 3.5 mm semiaxis ellipse, rotated 35°, to centers drawn uniformly in area from a disk of radius 4.5 mm. Each of eight seeds supplies 400 translations. Horizontal and vertical axes through the origin give four contacts. The 45° probe line passes through a point whose x coordinate is the horizontal chord midpoint and whose y coordinate is the vertical chord midpoint. One of its endpoints, chosen equiprobably, supplies contact five. Its other endpoint supplies contact six. An independent Gaussian error with 0.12 mm standard deviation perturbs each range coordinate. Both estimates use the same first five contacts and the same ellipse-constrained least-squares fit [2].

## Accuracy and time are separate conditions

For k measured contacts, let eₖ be center error and rₖ the distance from the probe origin to the fitted center. Assign deadline D, fixed overhead t₀, correction speed v and equal contact duration τ. The estimate meets the accuracy and deadline requirements exactly when eₖ ≤ ε and τ ≤ (D − t₀ − rₖ/v)/k. Sorting these per-fixture critical durations among accurate fits gives the count that finishes on time at any proposed τ.

There is also a bound that can be used before the fitted travel lengths are available. If the true center lies within radius R of the origin, every fit within tolerance obeys rₖ ≤ R + ε by the triangle inequality. Thus τ ≤ [D − t₀ − (R + ε)/v]/k suffices for every accurate fit to finish. It does not ensure an accurate fit. For R = 4.5 mm and ε = 0.25 mm the maximum travel allowance needed by an accurate estimate is 4.75 mm. With D = 1.8 s, t₀ = 0.42 s and v = 30 mm/s, a contact duration at or below 203.6 ms suffices for six touches. All three timing constants are assumptions.

| Contact duration | Five, accurate and on time | Six, accurate and on time | Both | Five only | Six only |
| --- | --- | --- | --- | --- | --- |
| 200 ms | 1,434 | 2,310 | 1,356 | 78 | 954 |
| 210 ms | 1,434 | 1,602 | 1,041 | 393 | 561 |
| 220 ms | 1,434 | 514 | 382 | 1,052 | 132 |

Table 1. Counts refer to the same 3,200 simulated starts in every row. The first row still shows 78 starts where only the five-contact fit succeeded, even though every accurate six-contact fit finished on time.

**Worked check.** At 220 ms per touch, how far can a six-contact probe travel under the assumed deadline? The six touches use 1.32 s. Subtracting 0.42 s of overhead from the remaining 0.48 s leaves 0.06 s for travel, or 1.8 mm at the assigned speed. Raising the deadline to 2.1 s increases the allowance to 10.8 mm, beyond the 4.75 mm bound. All 2,310 accurate six-contact fits then qualify. The nearly balanced counts around 211 ms in the archived sweep depend on the chosen costs and the distribution of fitted travel lengths.

Across all starts the median center errors were 0.294 mm for five contacts and 0.139 mm for six. The five-contact fit yielded 63 errors over 10 mm, including one of 2,458 mm. The six-contact fit yielded two errors over 10 mm. The fit constrains the conic to be an ellipse but leaves its center free to lie far outside the starting disk. A fit that minimizes algebraic residuals can therefore be unusable for placement.

To apply the calculation to a probe, independently survey the aperture centers, time the touch and correction stages, and test the resulting budget on separate parts. Finite tip size and alignment can change recorded rim coordinates [3]. Seating or insertion would require its own measured outcome.

## Data and code availability

The companion files `study/fixtures.csv` and `study/timing_frontier.csv` contain all 3,200 paired simulations and their timing counts. The script `study/verify.py` checks the conic example and the counts against individual fits. [Public study repository](https://github.com/VEDANT1602/aperture-contact-localization)

## Author and disclosures

Vedant Thaker is the sole author. He chose the paired five- and six-contact comparison and requested that the timing assumption be assessed separately from geometric accuracy. OpenAI Codex assisted with the geometric example, simulation analysis, timing thresholds, the travel bound and drafting.

This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors. The author declares no competing interests.

## References

[1] R. Hartley and A. Zisserman. Multiple View Geometry in Computer Vision, 2nd ed. Cambridge University Press, 2004, §2.2.3, p. 31. <https://doi.org/10.1017/CBO9780511811685>

[2] A. Fitzgibbon, M. Pilu and R. B. Fisher. Direct least square fitting of ellipses. IEEE Transactions on Pattern Analysis and Machine Intelligence 21(5), 476–480, 1999. <https://doi.org/10.1109/34.765658>

[3] J. Stone, B. Muralikrishnan and C. Sahay. Geometric effects when measuring small holes with micro contact probes. Journal of Research of the National Institute of Standards and Technology 116(2), 573–587, 2011. <https://doi.org/10.6028/jres.116.006>
