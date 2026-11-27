"""Draws the diagrams of the week 10 lecture (searching, sorting, hashing).

Run with:  python make_figures.py
It saves the PNG files next to this script:
  binary_search_steps.png   slide "Binary Search"
  bubble_sort_pass1.png     slide "Bubble Sort"
  bubble_sort_pass2-4.png   slide "Bubble Sort: All Passes"
  merge_sort_split.png      slide "Merge Sort: Splitting"
  merge_sort_example.png    slide "Merge Sort: Merging"
  merge_steps.png           slide "Merging Two Sorted Lists: Step by Step"
  hash_table_empty.png      slide "Hash Table"
  hash_table_filled.png     slide "The Hash Function"
  hash_table_collision.png  slide "Hash Table Collisions"
  probing_linear.png        slide "Rehashing"
  probing_plus3.png         slide "Rehashing: Other Probing Steps"
  chaining.png              slide "Chaining"
The values follow the examples on the slides; change them in both places.
"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

# Colours of the lecture slides (as in week 9's plot scripts)
GREEN, GREEN_TINT = "#4f6e51", "#e3ede4"
CLAY, CLAY_TINT = "#b0603a", "#f7efe6"
TEXT, SECONDARY, GREY, GREY_TINT, BACKGROUND = "#212121", "#5f5f5f", "#858585", "#eeeeee", "#fafafa"
plt.rcParams.update({"font.family": "sans-serif",
                     "font.sans-serif": ["Helvetica Neue", "Arial", "DejaVu Sans"],
                     "font.size": 13})
HERE = Path(__file__).parent


def new_figure(width, height, xlim, ylim):
    fig, ax = plt.subplots(figsize=(width, height))
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    fig.savefig(HERE / name, dpi=200, bbox_inches="tight", pad_inches=0.08, facecolor=BACKGROUND)
    plt.close(fig)
    print("saved", name)


def cell(ax, x, y, text, face="#FFFFFF", edge=TEXT, color=TEXT, bold=False, lw=1.5, size=15):
    ax.add_patch(Rectangle((x, y), 1, 1, facecolor=face, edgecolor=edge, linewidth=lw, zorder=2))
    ax.text(x + 0.5, y + 0.5, str(text), ha="center", va="center", color=color, fontsize=size,
            fontweight="bold" if bold else "normal", zorder=3)


def arrow(ax, start, end, rad=0.0, dashed=False, color=CLAY):
    ax.add_patch(FancyArrowPatch(start, end, connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>",
                                 mutation_scale=16, color=color, linewidth=2,
                                 linestyle=(0, (4, 3)) if dashed else "-", zorder=4))


# ---------------------------------------------------------------- binary search
def binary_search_steps():
    L = [2, 5, 8, 12, 16, 23, 38, 42, 51, 56, 64, 72, 80, 91, 99]
    e = 23
    steps, low, high = [], 0, len(L) - 1
    while low <= high:
        mid = (low + high) // 2
        steps.append((low, high, mid))
        if L[mid] == e:
            break
        elif L[mid] > e:
            high = mid - 1
        else:
            low = mid + 1
    notes = {"greater": f"{{}} > {e}: left half",
             "smaller": f"{{}} < {e}: right half",
             "found": "{} found"}
    fig, ax = new_figure(11, 3.2, (-2.2, 23.6), (-1.3 * (len(steps) - 1) - 0.15, 1.7))
    for i, v in enumerate(L):
        ax.text(i + 0.5, 1.35, str(i), ha="center", va="center", color=GREY, fontsize=11)
    for r, (low, high, mid) in enumerate(steps):
        y = -1.3 * r
        ax.text(-0.4, y + 0.5, f"Step {r + 1}", ha="right", va="center", color=SECONDARY, fontsize=13)
        for i, v in enumerate(L):
            if i == mid:
                cell(ax, i, y, v, face=CLAY_TINT, edge=CLAY, color=CLAY, bold=True, lw=2.5, size=12)
            elif low <= i <= high:
                cell(ax, i, y, v, size=12)
            else:
                cell(ax, i, y, v, face=GREY_TINT, edge=GREY, color=GREY, size=12)
        kind = "found" if L[mid] == e else ("greater" if L[mid] > e else "smaller")
        ax.text(15.5, y + 0.5, f"mid = {mid}: " + notes[kind].format(L[mid]), ha="left", va="center",
                color=CLAY if kind == "found" else TEXT, fontsize=14,
                fontweight="bold" if kind == "found" else "normal")
    save(fig, "binary_search_steps.png")


# ---------------------------------------------------------------- bubble sort
BUBBLE_START = [3, 5, 4, 1, 2]
BUBBLE_NOTES = {1: "after pass 1: the largest item is at the end",
                2: "after pass 2: 4 and 5 are in place",
                3: "after pass 3: 3, 4, and 5 are in place",
                4: "after pass 4: the list is sorted"}


def bubble_sort_pass(passnum):
    """Draws pass passnum (1 to 4) of bubble sort on BUBBLE_START: one row per comparison, then the result.
    All four figures use the same scale (same x range, figure height proportional to the rows)."""
    L = BUBBLE_START[:]
    n = len(L)
    for p in range(1, passnum):              # the passes before this one
        for i in range(n - p):
            if L[i] > L[i + 1]:
                L[i], L[i + 1] = L[i + 1], L[i]
    done = n - passnum + 1                   # items from this position on are already in place
    rows = []
    for i in range(n - passnum):
        a, b = L[i], L[i + 1]
        rows.append((L[:], i, f"{a} > {b}: swap" if a > b else f"{a} < {b}: no swap"))
        if a > b:
            L[i], L[i + 1] = L[i + 1], L[i]
    rows.append((L[:], None, BUBBLE_NOTES[passnum]))
    ybottom = -1.3 * (len(rows) - 1) - 0.15
    fig, ax = new_figure(9.2, 0.62 * (1.15 - ybottom) + 0.2, (-0.2, 16.6), (ybottom, 1.15))
    # invisible line over the full width: every figure gets the same width, so the same scale on the slides
    ax.plot([-0.2, 16.6], [0, 0], color=BACKGROUND, linewidth=0.1, zorder=0)
    for r, (values, i, note) in enumerate(rows):
        y = -1.3 * r
        for j, v in enumerate(values):
            if i is not None and j in (i, i + 1):
                cell(ax, j, y, v, face=CLAY_TINT, edge=CLAY, color=CLAY, bold=True, lw=2.5, size=18)
            elif i is None and (j >= n - passnum or passnum == n - 1):
                cell(ax, j, y, v, face=GREEN_TINT, edge=GREEN, color=GREEN, bold=True, lw=2.5, size=18)
            elif j >= done:
                cell(ax, j, y, v, face=GREEN_TINT, edge=GREEN, color=GREEN, lw=1.5, size=18)
            else:
                cell(ax, j, y, v, size=18)
        ax.text(5.6, y + 0.5, note, ha="left", va="center", fontsize=17,
                color=GREEN if i is None else TEXT, fontweight="bold" if i is None else "normal")
    save(fig, f"bubble_sort_pass{passnum}.png")


# ---------------------------------------------------------------- merge sort
def merge_sort_example(split_only=False):
    """The whole merge sort (merge_sort_example.png) or only the splitting half (merge_sort_split.png),
    at the same scale."""
    L = [6, 3, 8, 1, 5, 2, 7, 4]
    n = len(L)
    gap = 0.6
    max_width = n + (n - 1) * gap

    def row(ax, values, size, y, face, edge, color, bold):
        groups = n // size
        width = n + (groups - 1) * gap
        x0 = (max_width - width) / 2
        for i, v in enumerate(values):
            x = x0 + i + (i // size) * gap
            cell(ax, x, y, v, face=face, edge=edge, color=color, bold=bold, lw=2 if bold else 1.5)

    split_rows = [(L, 8), ([6, 3, 8, 1, 5, 2, 7, 4], 4), ([6, 3, 8, 1, 5, 2, 7, 4], 2),
                  ([6, 3, 8, 1, 5, 2, 7, 4], 1)]
    merge_rows = [([3, 6, 1, 8, 2, 5, 4, 7], 2), ([1, 3, 6, 8, 2, 4, 5, 7], 4),
                  ([1, 2, 3, 4, 5, 6, 7, 8], 8)]
    dy = 1.45
    last_row = 3 if split_only else 6
    ylim = (-dy * last_row - 0.3, 1.3)
    fig, ax = new_figure(10, 6.2 * (ylim[1] - ylim[0]) / (dy * 6 + 1.6), (-3.6, max_width + 7.6), ylim)
    # invisible line over the full width: both figures get the same width, so the same scale on the slides
    ax.plot([-3.6, max_width + 7.6], [0, 0], color=BACKGROUND, linewidth=0.1, zorder=0)
    for r, (values, size) in enumerate(split_rows):
        y = -dy * r
        row(ax, values, size, y, "#FFFFFF", TEXT, TEXT, False)
    for r, (values, size) in enumerate([] if split_only else merge_rows, start=4):
        y = -dy * r
        last = size == n
        row(ax, values, size, y, GREEN_TINT if last else "#FFFFFF", GREEN if last else TEXT,
            GREEN if last else TEXT, last)
    # labels on the left
    for r in range(1, 4):
        ax.text(-0.5, -dy * r + 0.5, "split", ha="right", va="center", color=SECONDARY, fontsize=13)
    for r in range(4, last_row + 1):
        ax.text(-0.5, -dy * r + 0.5, "merge", ha="right", va="center", color=CLAY, fontsize=13,
                fontweight="bold")
    # labels on the right
    xr = max_width + 0.6
    ax.plot([xr, xr], [-dy * 3, -dy * 1 + 1], color=GREY, linewidth=1.5)
    ax.text(xr + 0.3, -dy * 2 + 0.5, "3 levels\n= log₂ 8", ha="left", va="center", color=SECONDARY,
            fontsize=13)
    for r in range(4, last_row + 1):
        ax.text(xr + 0.3, -dy * r + 0.5, "8 steps", ha="left", va="center", color=CLAY, fontsize=14)
    if not split_only:
        ax.plot([-3.4, max_width + 7.4], [-dy * 3 - 0.22, -dy * 3 - 0.22], color=GREY_TINT, linewidth=2)
    save(fig, "merge_sort_split.png" if split_only else "merge_sort_example.png")


def merge_steps():
    """The merge function step by step: merge([1, 3, 6, 8], [2, 4, 5, 7]), the last merge in merge_sort_example.
    One row per step: left and right (items already moved are grey, the compared first items clay), the result."""
    left, right = [1, 3, 6, 8], [2, 4, 5, 7]
    rows, i, j, result = [], 0, 0, []
    while i < len(left) and j < len(right):        # as in merge() on the slide
        if left[i] < right[j]:
            note = f"{left[i]} < {right[j]}: take {left[i]}"
            rows.append((i, j, result + [left[i]], note, (i, j)))
            result.append(left[i])
            i += 1
        else:
            note = f"{left[i]} > {right[j]}: take {right[j]}"
            rows.append((i, j, result + [right[j]], note, (i, j)))
            result.append(right[j])
            j += 1
    rest = left[i:] + right[j:]
    empty = "right" if j == len(right) else "left"
    other = "left" if empty == "right" else "right"
    rows.append((i, j, result + rest, f"{empty} is empty: add the rest of {other}", None))

    xl, xr, xres, xnote = 0, 5, 10.6, 19.2      # x positions of left, right, result, note
    dy = 1.25
    ybottom = -dy * (len(rows) - 1) - 0.15
    fig, ax = new_figure(11, 5.2, (-0.2, 28.2), (ybottom, 2.0))
    for x, label in [(xl, "left"), (xr, "right"), (xres, "result")]:
        ax.text(x, 1.45, label, ha="left", va="center", color=SECONDARY, fontsize=15, fontweight="bold")
    for r, (i, j, res, note, compared) in enumerate(rows):
        y = -dy * r
        last = compared is None
        for lst, x0, pos in [(left, xl, i), (right, xr, j)]:
            for k, v in enumerate(lst):
                if k < pos:          # already moved to the result
                    cell(ax, x0 + k, y, v, face=GREY_TINT, edge=GREY, color=GREY, size=15)
                elif k == pos and not last:
                    cell(ax, x0 + k, y, v, face=CLAY_TINT, edge=CLAY, color=CLAY, bold=True, lw=2.5, size=15)
                else:
                    cell(ax, x0 + k, y, v, size=15)
        arrow(ax, (xres - 1.0, y + 0.5), (xres - 0.15, y + 0.5), color=GREY)
        for k, v in enumerate(res):
            if last:
                new = k >= len(res) - len(rest)
                cell(ax, xres + k, y, v, face=GREEN_TINT, edge=GREEN, color=GREEN, bold=True,
                     lw=2.5 if new else 1.5, size=15)
            elif k == len(res) - 1:
                cell(ax, xres + k, y, v, face=CLAY_TINT, edge=CLAY, color=CLAY, bold=True, lw=2.5, size=15)
            else:
                cell(ax, xres + k, y, v, size=15)
        ax.text(xnote, y + 0.5, note, ha="left", va="center", fontsize=15,
                color=GREEN if last else TEXT, fontweight="bold" if last else "normal")
    save(fig, "merge_steps.png")


# ---------------------------------------------------------------- hash tables
ITEMS = {0: 20, 2: 22, 4: 34, 5: 45, 7: 117}


def hash_table(ax, items, new=None, y=0):
    """Ten slots; items maps slot -> value; new is the slot of the item that was just added."""
    for slot in range(10):
        if slot == new:
            cell(ax, slot, y, items[slot], face=CLAY_TINT, edge=CLAY, color=CLAY, bold=True, lw=2.5)
        elif slot in items:
            cell(ax, slot, y, items[slot], face=GREEN_TINT)
        else:
            cell(ax, slot, y, "")
        ax.text(slot + 0.5, y - 0.35, str(slot), ha="center", va="center", color=SECONDARY, fontsize=13)


def hash_figures():
    xlim, ylim = (-0.2, 16.4), (-0.7, 2.4)
    size = (10.5, 2.0)

    fig, ax = new_figure(*size, xlim, ylim)
    hash_table(ax, {})
    save(fig, "hash_table_empty.png")

    fig, ax = new_figure(*size, xlim, ylim)
    hash_table(ax, ITEMS)
    save(fig, "hash_table_filled.png")

    # collision: 12 % 10 = 2, but slot 2 holds 22
    fig, ax = new_figure(*size, xlim, ylim)
    hash_table(ax, ITEMS)
    ax.text(2.5, 2.05, "12", ha="center", va="center", color=CLAY, fontsize=15, fontweight="bold")
    arrow(ax, (2.5, 1.8), (2.5, 1.08))
    ax.text(10.4, 1.95, "12 % 10 = 2: slot 2 is taken", ha="left", va="center", color=CLAY, fontsize=14)
    save(fig, "hash_table_collision.png")

    # linear probing: skip = 1, 12 goes to slot 3
    fig, ax = new_figure(*size, xlim, ylim)
    hash_table(ax, {**ITEMS, 3: 12}, new=3)
    ax.text(2.5, 2.05, "12", ha="center", va="center", color=CLAY, fontsize=15, fontweight="bold")
    arrow(ax, (2.85, 2.05), (3.5, 1.08), rad=-0.35)
    ax.text(10.4, 1.95, "slot 2 is taken\n(2 + 1) % 10 = 3", ha="left", va="center", color=CLAY,
            fontsize=13)
    save(fig, "probing_linear.png")

    # plus 3 probing: skip = 3, slot 5 is taken, 12 goes to slot 8
    fig, ax = new_figure(*size, xlim, ylim)
    hash_table(ax, {**ITEMS, 8: 12}, new=8)
    ax.text(2.5, 2.05, "12", ha="center", va="center", color=CLAY, fontsize=15, fontweight="bold")
    arrow(ax, (2.85, 2.05), (5.5, 1.08), rad=-0.3, dashed=True)
    arrow(ax, (5.7, 1.3), (8.5, 1.08), rad=-0.45)
    ax.text(10.4, 1.95, "slot 2 is taken\n(2 + 3) % 10 = 5 is taken\n(5 + 3) % 10 = 8", ha="left",
            va="center", color=CLAY, fontsize=14)
    save(fig, "probing_plus3.png")

    # chaining: slot 2 holds a list [22, 12]
    fig, ax = new_figure(*size, xlim, ylim)
    hash_table(ax, ITEMS)
    cell(ax, 2, 1.0, 12, face=CLAY_TINT, edge=CLAY, color=CLAY, bold=True, lw=2.5)
    ax.text(10.4, 1.95, "slot 2 holds a list: [22, 12]", ha="left", va="center", color=CLAY, fontsize=14)
    save(fig, "chaining.png")


if __name__ == "__main__":
    binary_search_steps()
    for passnum in range(1, 5):
        bubble_sort_pass(passnum)
    merge_sort_example(split_only=True)
    merge_sort_example()
    merge_steps()
    hash_figures()
