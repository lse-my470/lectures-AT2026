"""Draws the plot on the slide "A Linear Function of the Input Size".

The function total(L) takes T(n) = 3n + 2 steps for a list L of length n.
Run with:  python make_steps_plot.py
It saves steps_linear.png next to this script.
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

n = list(range(1001))                    # input sizes from 0 to 1,000
steps = [3 * i + 2 for i in n]           # T(n) = 3n + 2

fig, ax = plt.subplots(figsize=(7.2, 3.3))
fig.patch.set_facecolor(BACKGROUND)
ax.set_facecolor(BACKGROUND)
ax.plot(n, steps, color=GREEN, linewidth=2.5, zorder=2)

# The two calls of total() on the slide before
ax.scatter([3, 1000], [11, 3002], s=70, color=CLAY, edgecolor=BACKGROUND, linewidth=2, zorder=3)
ax.annotate("total([4, 8, 15]): 11 steps", xy=(3, 11), xytext=(250, 330), va="center",
            color=SECONDARY, fontsize=12, arrowprops=dict(arrowstyle="-", color=GREY, linewidth=1))
ax.annotate("1,000 elements: 3,002 steps", xy=(1000, 3002), xytext=(975, 3080),
            ha="right", va="bottom", color=SECONDARY, fontsize=12)

# Axes: labels, ranges, ticks with thousands separators, a light grid
ax.set_xlabel("Input size n (number of elements in L)", color=TEXT, labelpad=8)
ax.set_ylabel("Number of steps T(n)", color=TEXT, labelpad=8)
ax.set_xlim(0, 1050)
ax.set_ylim(0, 3500)
ax.set_xticks(range(0, 1001, 200))
ax.set_yticks(range(0, 3001, 1000))
ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
ax.tick_params(colors=SECONDARY, labelsize=12, length=0, pad=6)
ax.grid(color="#e3e3e3", linewidth=1)
ax.set_axisbelow(True)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_color(GREY)

fig.savefig(Path(__file__).parent / "steps_linear.png", dpi=200, bbox_inches="tight",
            facecolor=BACKGROUND)
