"""Draws the plot on the slide "Lower and Upper Bound".

linear_search(L, x) makes between 1 comparison (x is the first element: best case)
and n comparisons (x is not in L: worst case) for a list L of length n.
Run with:  python make_bounds_plot.py
It saves bounds_linear_search.png next to this script.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Colours of the lecture slides
GREEN, GREEN_LIGHT, CLAY = "#4f6e51", "#a8cdae", "#b0603a"
TEXT, SECONDARY, GREY, BACKGROUND = "#212121", "#5f5f5f", "#858585", "#fafafa"
plt.rcParams.update({"font.family": "sans-serif",
                     "font.sans-serif": ["Helvetica Neue", "Arial", "DejaVu Sans"],
                     "font.size": 13})

n = list(range(1, 1001))                 # input sizes from 1 to 1,000
upper = n                                # worst case: n comparisons
lower = [1 for i in n]                   # best case: 1 comparison

fig, ax = plt.subplots(figsize=(7.2, 3.1))
fig.patch.set_facecolor(BACKGROUND)
ax.set_facecolor(BACKGROUND)

# Every input of size n takes a number of comparisons in the shaded area
ax.fill_between(n, lower, upper, color=GREEN_LIGHT, alpha=0.35, linewidth=0, zorder=1)
ax.plot(n, upper, color=GREEN, linewidth=2.5, zorder=2)
ax.plot(n, lower, color=CLAY, linewidth=2.5, zorder=2)

# Labels in the colour of their line, running parallel to it
# (rotation=45 is the angle of the line y = x in data coordinates; matplotlib turns it into the
# angle on screen)
ax.text(230, 290, "Upper bound (worst case): n comparisons", ha="left", va="bottom",
        rotation=45, transform_rotates_text=True, rotation_mode="anchor", color=GREEN, fontsize=12)
ax.text(130, 25, "Lower bound (best case): 1 comparison", ha="left", va="bottom",
        color=CLAY, fontsize=12)

# Two calls with 1,000 elements: -1 is not in the list (worst case), 0 is the first element (best case)
ax.scatter([1000, 1000], [1000, 1], s=80, color=TEXT, edgecolor=BACKGROUND, linewidth=2, zorder=3)
ax.annotate("linear_search(range(1000), -1)\n1,000 comparisons", xy=(1000, 1000), xytext=(940, 1140),
            ha="right", va="center", multialignment="left", color=TEXT, fontsize=11, family="monospace",
            arrowprops=dict(arrowstyle="-", color=GREY, linewidth=1))
ax.annotate("linear_search(range(1000), 0)\n1 comparison", xy=(1000, 1), xytext=(940, 255),
            ha="right", va="center", multialignment="left", color=TEXT, fontsize=11, family="monospace",
            arrowprops=dict(arrowstyle="-", color=GREY, linewidth=1))

# Axes: labels, ranges, ticks with thousands separators, a light grid
ax.set_xlabel("Input size n (number of elements in L)", color=TEXT, labelpad=8)
ax.set_ylabel("Number of comparisons", color=TEXT, labelpad=8)
ax.set_xlim(0, 1050)
ax.set_ylim(-60, 1260)   # a little room below 0 so the lower bound stays visible
ax.set_xticks(range(0, 1001, 200))
ax.set_yticks(range(0, 1001, 250))
ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
ax.tick_params(colors=SECONDARY, labelsize=12, length=0, pad=6)
ax.grid(color="#e3e3e3", linewidth=1)
ax.set_axisbelow(True)
for side in ("top", "right", "bottom"):
    ax.spines[side].set_visible(False)
ax.spines["left"].set_color(GREY)

fig.savefig(Path(__file__).parent / "bounds_linear_search.png", dpi=200, bbox_inches="tight",
            facecolor=BACKGROUND)
