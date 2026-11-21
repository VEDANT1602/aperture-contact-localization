# Elliptical-aperture center estimation

Run with Python 3.12.14 and NumPy 2.3.5. The geometry routines are adapted from the author's MIT-licensed [public implementation](https://github.com/VEDANT1602/aperture-contact-localization/tree/564b3879d618f6053d90dfd42009a98d37b4ad89). The supplement uses no photographs or hardware data.

```sh
python -m pip install -r requirements.txt
OPENBLAS_NUM_THREADS=1 python contact_frontier.py
python verify.py
```

- `fixtures.csv` stores all 3,200 paired center errors and travel distances in mm. The fifth-contact side is drawn per fixture. Block 1 corresponds to seed 21770, block 8 to seed 21777.
- `timing_frontier.csv` contains paired accuracy/deadline contingency tables over all tolerances, contact durations, and deadlines. Block 0 comprises the entire panel and is repeated as eight disjoint block summaries. Columns `geom` and `timely` count each condition separately. `pass` requires both. The total of `both`, `only5`, `only6` and `neither` equals the fixture count.
- `verify.py` evaluates the four-point counterexample, noiseless estimator translation, and decision tables using critical durations computed independently from travel distance.
- `references.md` records source locations and what can be inferred from them.

### Physical replication still needed

Use printed elliptic apertures with varied axis ratio and orientation and hold out complete parts. Independently survey centers, axes and alignment on a calibrated coordinate measuring machine. With a timed contact sensor, randomize probing order and record each command, first trigger, completed retraction and arrival at the estimated center. Fit travel and touch time on calibration parts, retain misses and repeat contacts, then freeze coefficients and compare predicted versus observed deadline decisions on held-out parts. Assess center error against the surveyed centers. Report seating separately only if measured with an independently defined depth/force criterion. The archived NIST registration/insertion tables do not supply these trigger histories for paired five-/six-contact runs.

To regenerate the manuscript figure, install Matplotlib 3.10.8 and run `python plot.py`.

### Exact crossover in the worked example

Run `python critical_duration.py` with the supplied `fixtures.csv`. The script ranks the largest permissible contact duration for each geometrically accurate estimate and recreates `critical_duration.csv` and Table 1. At the reported settings every accurate five-contact fit is on time through 245.1 ms per contact. All six-contact critical durations are below that value, so while the six-contact count is passing through 1,434, the five-contact count is constant. The sample equality interval is open on its lower endpoint and closed on its upper endpoint because the deadline permits equality. Its narrow width reflects the individual travel lengths in this finite simulation.
