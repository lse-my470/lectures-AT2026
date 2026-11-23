"""Draws the plot on the slide "A Logarithmic Function of the Input".

For every x from 1 to 10,000, it counts the guesses that bisec_search(x, 0.01) from the
slide "Logarithmic Complexity: Bisection Search" needs, and draws the worst case up to x
(the most guesses any input up to x needs) as a staircase: the number of guesses is a
whole number. (Single values jump around: perfect squares such as 16 are found after very
few guesses.)
The staircase follows 1.5 * log2(x) + log2(2 / 0.01) closely: each guess halves the interval
[0, x], and the search stops once the interval is narrower than about epsilon / (2 * sqrt(x)).
Big-O keeps only the shape: O(log x). (The curve itself is not drawn.)
Run with:  python make_bisection_plot.py
It saves steps_bisection.png next to this script.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Colours of the lecture slides (as in make_steps_plot.py)
GREEN, CLAY = "#4f6e51", "#b0603a"
TEXT, SECONDARY, GREY, BACKGROUND = "#212121", "#5f5f5f", "#858585", "#fafafa"
plt.rcParams.update({"font.family": "sans-serif",
                     "font.sans-serif": ["Helvetica Neue", "Arial", "DejaVu Sans"],
                     "font.size": 13})


def bisec_search(x, epsilon):
    """As on the slide: returns the approximation and the number of guesses."""
    low, high = 0, max(1, x)
    guess = (low + high) / 2
    num_guess = 1
    while abs(guess**2 - x) >= epsilon:
        if guess**2 < x:
            low = guess
        else:
            high = guess
        guess = (low + high) / 2
        num_guess += 1
    return guess, num_guess


xs = list(range(1, 10001))
guesses = [bisec_search(x, 0.01)[1] for x in xs]

fig, ax = plt.subplots(figsize=(7.2, 2.9))
fig.patch.set_facecolor(BACKGROUND)
ax.set_facecolor(BACKGROUND)
# worst case up to x: a staircase, because the number of guesses is a whole number
worst, most = [], 0
for g in guesses:
    most = max(most, g)
    worst.append(most)
ax.plot(xs, worst, color=GREEN, linewidth=2.5, drawstyle="steps-post", zorder=2)


# Two calls: the example on the slide before, and a 400 times larger input
g25, g10000 = guesses[25 - 1], guesses[10000 - 1]
ax.scatter([25, 10000], [g25, g10000], s=70, color=CLAY, edgecolor=BACKGROUND, linewidth=2, zorder=3)
ax.annotate(f"bisec_search(25, 0.01): {g25} guesses", xy=(25, g25), xytext=(1200, 8), va="center",
            color=SECONDARY, fontsize=12, arrowprops=dict(arrowstyle="-", color=GREY, linewidth=1))
ax.annotate(f"x = 10,000: {g10000} guesses", xy=(10000, g10000), xytext=(9750, g10000 + 1.2),
            ha="right", va="bottom", color=SECONDARY, fontsize=12)

# Axes: labels, ranges, ticks with thousands separators, a light grid
ax.set_xlabel("Input x (the number whose square root we search)", color=TEXT, labelpad=8)
ax.set_ylabel("Guesses (worst case)", color=TEXT, labelpad=8)
ax.set_xlim(0, 10500)
ax.set_ylim(0, 32)
ax.set_xticks(range(0, 10001, 2000))
ax.set_yticks(range(0, 31, 10))
ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
ax.tick_params(colors=SECONDARY, labelsize=12, length=0, pad=6)
ax.grid(color="#e3e3e3", linewidth=1)
ax.set_axisbelow(True)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_color(GREY)

fig.savefig(Path(__file__).parent / "steps_bisection.png", dpi=200, bbox_inches="tight",
            facecolor=BACKGROUND)
