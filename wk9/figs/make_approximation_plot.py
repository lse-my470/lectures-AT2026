"""Draws the plot on the slide "Approximation".

Compares T(n) = n^2 + 5n + 8 with its fastest-growing term n^2, for small and for large inputs.
Run with:  python make_approximation_plot.py
It saves approximation.png next to this script.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Colours of the lecture slides
GREEN, CLAY = "#4f6e51", "#b0603a"
TEXT, SECONDARY, GREY, BACKGROUND = "#212121", "#5f5f5f", "#858585", "#fafafa"
plt.rcParams.update({"font.family": "sans-serif",
                     "font.sans-serif": ["Helvetica Neue", "Arial", "DejaVu Sans"],
                     "font.size": 13})

fig, axes = plt.subplots(1, 2, figsize=(9, 3.2))
fig.patch.set_facecolor(BACKGROUND)

for ax, max_n, title in [(axes[0], 10, "Small inputs: n up to 10"),
                         (axes[1], 500, "Large inputs: n up to 500")]:
    n = list(range(1, max_n + 1))
    ax.set_facecolor(BACKGROUND)
    ax.plot(n, [i * i + 5 * i + 8 for i in n], color=GREEN, linewidth=2.5, label="T(n) = n² + 5n + 8")
    ax.plot(n, [i * i for i in n], color=CLAY, linewidth=2.5, linestyle="--", label="n²")
    ax.set_title(title, color=TEXT, fontsize=13)
    ax.set_xlabel("Input size n", color=TEXT, labelpad=6)
    ax.set_xlim(0, max_n)
    ax.set_ylim(0, None)
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
    ax.tick_params(colors=SECONDARY, labelsize=11, length=0, pad=6)
    ax.grid(color="#e3e3e3", linewidth=1)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GREY)

axes[0].set_ylabel("Number of steps", color=TEXT, labelpad=6)
axes[0].legend(loc="upper left", frameon=False, fontsize=12, labelcolor=TEXT)
fig.tight_layout(w_pad=3)

fig.savefig(Path(__file__).parent / "approximation.png", dpi=200, bbox_inches="tight",
            facecolor=BACKGROUND)
