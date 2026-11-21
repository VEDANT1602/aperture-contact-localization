"""Plot the paired time budgets from the released contingency tables."""

from pathlib import Path
import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

root = Path(__file__).resolve().parent
with (root / "timing_frontier.csv").open() as f:
    rows = [
        r for r in csv.DictReader(f) if r["block"] == "0" and float(r["tolerance_mm"]) == 0.25
    ]
fig, axes = plt.subplots(1, 2, figsize=(8, 2.75), sharey=True, layout="constrained")
for ax, deadline in zip(axes, [1.8, 2.1]):
    selected = [r for r in rows if float(r["deadline_s"]) == deadline]
    for key, name, color, marker in [
        ("pass5", "Five contacts", "#a34e33", "o"),
        ("pass6", "Six contacts", "#226f71", "s"),
    ]:
        ax.plot(
            [float(r["contact_s"]) for r in selected],
            [int(r[key]) / int(r["fixtures"]) for r in selected],
            lw=2,
            marker=marker,
            ms=3,
            label=name,
            color=color,
        )
    ax.set_title(f"{deadline:.2f} s deadline", loc="left", fontsize=11)
    ax.set_xlabel("Assigned time per contact (s)")
    ax.set_xlim(0.097, 0.263)
    ax.set_ylim(-0.025, 0.81)
    ax.set_xticks([0.10, 0.14, 0.18, 0.22, 0.26])
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8])
    ax.yaxis.set_major_formatter(PercentFormatter(1, decimals=0))
    ax.grid(axis="y", alpha=0.22)
    ax.spines[["top", "right"]].set_visible(False)
axes[0].set_ylabel("Accurate and on time")
axes[1].legend(loc="lower left", frameon=False, fontsize=9)
fig.savefig(root / "timing-curve.png", dpi=220)
