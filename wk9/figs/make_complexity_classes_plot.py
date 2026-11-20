"""Draws the plot on the slide "Comparison of Complexity Classes".

One curve per complexity class, for input sizes n from 1 to 20.
Run with:  python make_complexity_classes_plot.py
It saves complexity_classes.png next to this script.
"""
import math
from pathlib import Path

import matplotlib.pyplot as plt

# Colours of the lecture slides: from green (grows slowly) to clay (grows fast)
TEXT, SECONDARY, GREY, BACKGROUND = "#212121", "#5f5f5f", "#858585", "#fafafa"
plt.rcParams.update({"font.family": "sans-serif",
                     "font.sans-serif": ["Helvetica Neue", "Arial", "DejaVu Sans"],
                     "font.size": 13})

n = [1 + i / 20 for i in range(381)]     # input sizes from 1 to 20, in small steps for smooth curves

# (label, number of steps for each n, colour), from the fastest-growing class to the slowest,
# so that the legend lists them in the same order as the curves appear from top to bottom
classes = [
    ("$O(2^n)$  exponential",       [2 ** i for i in n],           "#7a3a1c"),
    ("$O(n^2)$  polynomial",        [i ** 2 for i in n],           "#b0603a"),
    ("$O(n \\log n)$  log-linear",  [i * math.log(i) for i in n],  "#d9a784"),
    ("$O(n)$  linear",              n,                             GREY),
    ("$O(\\log n)$  logarithmic",   [math.log(i) for i in n],      "#7cb083"),
    ("$O(1)$  constant",            [10 for i in n],               "#4f6e51"),
]

fig, ax = plt.subplots(figsize=(6.6, 3.4))
fig.patch.set_facecolor(BACKGROUND)
ax.set_facecolor(BACKGROUND)
for label, steps, colour in classes:
    ax.plot(n, steps, color=colour, linewidth=2.8, label=label, solid_capstyle="round")

# Axes: labels, ranges, a light grid
ax.set_xlabel("Input size n", color=TEXT, labelpad=8)
ax.set_ylabel("Number of steps", color=TEXT, labelpad=8)
ax.set_xlim(1, 20)
ax.set_ylim(0, 200)
ax.set_xticks([1, 5, 10, 15, 20])
ax.tick_params(colors=SECONDARY, labelsize=12, length=0, pad=6)
ax.grid(color="#e3e3e3", linewidth=1)
ax.set_axisbelow(True)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_color(GREY)

# Legend to the right of the plot, in the order of the curves
ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False, fontsize=12,
          labelcolor=TEXT, handlelength=1.6)

fig.savefig(Path(__file__).parent / "complexity_classes.png", dpi=200, bbox_inches="tight",
            facecolor=BACKGROUND)
