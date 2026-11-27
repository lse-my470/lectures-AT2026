"""Draws sorting_race.mp4 for the slide "Sorting Algorithms Side by Side".

Bubble, selection, insertion, and merge sort run on the same random list of 20 items. The first frame
shows the unsorted list; after that, one frame is one comparison in each panel, so the panels show how many comparisons each algorithm needs.
The algorithms follow the code on the slides (selection sort moves the largest item to the end).
Visual idea (bars; red for the items being compared, green once sorted) after the sorting visualiser
in AlgorithmVisualizer by Mohammad Tamimul Ehsan (MIT License,
https://github.com/TamimEhsan/AlgorithmVisualizer); no code from that project is used.
Run with:  python make_sorting_animation.py   (needs matplotlib and ffmpeg)
A video (not a GIF) so that it starts only when you press play on the slide and does not loop.
"""
import random
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter, FuncAnimation

GREEN, GREEN_LIGHT, CLAY = "#4f6e51", "#a8cdae", "#b0603a"
TEXT, SECONDARY, GREY, BACKGROUND = "#212121", "#5f5f5f", "#bdbdbd", "#fafafa"
plt.rcParams.update({"font.family": "sans-serif",
                     "font.sans-serif": ["Helvetica Neue", "Arial", "DejaVu Sans"],
                     "font.size": 13})
HERE = Path(__file__).parent
N, SEED = 20, 470
HOLD = 1             # the video stops on its last frame, so no long hold is needed


# Each generator yields one state per comparison: (list, compared positions, final positions, sorted part)
def bubble(L):
    L = L[:]
    final = set()
    for passnum in range(len(L) - 1, 0, -1):
        for i in range(passnum):
            if L[i] > L[i + 1]:
                L[i], L[i + 1] = L[i + 1], L[i]
            yield L[:], {i, i + 1}, set(final), set()
        final.add(passnum)
    final.add(0)
    yield L[:], set(), final, set()


def selection(L):
    L = L[:]
    final = set()
    for pos in range(len(L) - 1, 0, -1):
        max_pos = 0
        for i in range(1, pos + 1):
            yield L[:], {i, max_pos}, set(final), set()
            if L[i] > L[max_pos]:
                max_pos = i
        L[pos], L[max_pos] = L[max_pos], L[pos]
        final.add(pos)
    final.add(0)
    yield L[:], set(), final, set()


def insertion(L):
    L = L[:]
    for i in range(1, len(L)):
        pos = i
        while pos > 0:
            # shown as a swap of neighbours, so that the current item stays visible while it moves left
            yield L[:], {pos - 1, pos}, set(), set(range(i))
            if L[pos - 1] > L[pos]:
                L[pos - 1], L[pos] = L[pos], L[pos - 1]
                pos -= 1
            else:
                break
    yield L[:], set(), set(range(len(L))), set()


def merge_sort(L):
    A = L[:]
    merged = set()

    def sort(lo, hi):                       # sorts A[lo:hi], like merge_sort(L) on the slide
        if hi - lo <= 1:
            return
        mid = lo + (hi - lo) // 2
        yield from sort(lo, mid)
        yield from sort(mid, hi)
        left, right = A[lo:mid], A[mid:hi]
        i, j, k = 0, 0, lo
        while i < len(left) and j < len(right):
            # the result so far sits in A[lo:k], the remaining items of left and right follow it
            A[k:hi] = left[i:] + right[j:]
            yield A[:], {k, k + len(left) - i}, set(), merged | set(range(lo, k))
            if left[i] < right[j]:
                A[k] = left[i]
                i += 1
            else:
                A[k] = right[j]
                j += 1
            k += 1
        A[k:hi] = left[i:] + right[j:]      # one list is empty: add the rest
        merged.update(range(lo, hi))

    yield from sort(0, len(A))
    yield A[:], set(), set(range(len(A))), set()


def main():
    random.seed(SEED)
    data = random.sample(range(5, 100), N)
    algorithms = [("Bubble sort", "$O(n^2)$", bubble), ("Selection sort", "$O(n^2)$", selection),
                  ("Insertion sort", "$O(n^2)$", insertion), ("Merge sort", "$O(n \\log n)$", merge_sort)]
    # frame 0: the unsorted list before any comparison; the last state is the "done" state
    runs = [[(data[:], set(), set(), set())] + list(f(data)) for _, _, f in algorithms]
    counts = [len(r) - 2 for r in runs]     # minus the start frame and the "done" state
    frames = max(len(r) for r in runs) + HOLD

    fig, axes = plt.subplots(2, 2, figsize=(10, 5.4))
    fig.patch.set_facecolor(BACKGROUND)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.9, bottom=0.04, hspace=0.45, wspace=0.08)
    panels = []
    for ax, (name, bigo, _) in zip(axes.flat, algorithms):
        ax.set_facecolor(BACKGROUND)
        ax.set_xlim(-0.7, N - 0.3)
        ax.set_ylim(0, 105)
        ax.axis("off")
        bars = ax.bar(range(N), data, width=0.75, color=GREY)
        ax.text(-0.5, 118, name, ha="left", va="bottom", fontsize=15, fontweight="bold", color=TEXT)
        ax.text(N - 0.5, 118, bigo, ha="right", va="bottom", fontsize=15, color=CLAY)
        counter = ax.text(-0.5, 108, "", ha="left", va="bottom", fontsize=12, color=SECONDARY)
        panels.append((bars, counter))

    def draw(t):
        for (bars, counter), run, count in zip(panels, runs, counts):
            step = min(t, len(run) - 1)
            values, compared, final, part = run[step]
            for idx, (bar, v) in enumerate(zip(bars, values)):
                bar.set_height(v)
                if idx in compared:
                    bar.set_color(CLAY)
                elif idx in final:
                    bar.set_color(GREEN)
                elif idx in part:
                    bar.set_color(GREEN_LIGHT)
                else:
                    bar.set_color(GREY)
            if t >= len(run) - 1:
                counter.set_text(f"sorted after {count} comparisons")
                counter.set_color(GREEN)
                counter.set_fontweight("bold")
            else:
                counter.set_text(f"comparisons: {step}")
                counter.set_color(SECONDARY)
                counter.set_fontweight("normal")
        return []

    anim = FuncAnimation(fig, draw, frames=frames, blit=False)
    writer = FFMpegWriter(fps=12, codec="libx264", extra_args=["-pix_fmt", "yuv420p", "-movflags", "+faststart"])
    anim.save(HERE / "sorting_race.mp4", writer=writer, dpi=100, savefig_kwargs={"facecolor": BACKGROUND})
    plt.close(fig)
    print("saved sorting_race.mp4:", dict(zip([a[0] for a in algorithms], counts)), "comparisons,", frames, "frames")


if __name__ == "__main__":
    main()
