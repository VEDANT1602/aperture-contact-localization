"""Recompute the timing crossover directly from fixture-level errors and travel lengths."""
import csv
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parent
DEADLINE, OVERHEAD, SPEED, TOLERANCE = 1.8, 0.42, 30., 0.25

def main():
    with (ROOT/'fixtures.csv').open() as data:
        rows = list(csv.DictReader(data))
    groups = {}
    for count in (5, 6):
        errors = [float(r[f'error_{count}']) for r in rows]
        groups[count] = sorted(((DEADLINE - OVERHEAD - float(r[f'travel_{count}']) / SPEED) / count
                               for r in rows if float(r[f'error_{count}']) <= TOLERANCE), reverse=True)
        print(f'{count} contacts: {len(errors)} fits, median error {median(errors):.6f} mm,'
              f' maximum {max(errors):.6f} mm, {sum(v > 10 for v in errors)} over 10 mm.')
    five, six = groups[5], groups[6]
    exact = dict(deadline_s=DEADLINE, overhead_s=OVERHEAD, speed_mm_s=SPEED, tolerance_mm=TOLERANCE,
                 pairs=len(rows), five_geometric=len(five), six_geometric=len(six),
                 five_last_all_passing_tau_s=min(five), six_tie_lower_open_s=six[len(five)],
                 six_tie_upper_closed_s=six[len(five)-1])
    assert len(set(six)) == len(six) and six[0] < min(five)
    with (ROOT/'critical_duration.csv').open('w', newline='') as target:
        writer = csv.DictWriter(target, fieldnames=list(exact))
        writer.writeheader()
        writer.writerow(exact)
    for tau in (.18, .21, .211, .212, .22):
        print(f'{tau}s: five {sum(x >= tau for x in five)}, six {sum(x >= tau for x in six)}')

if __name__ == '__main__':
    main()
