"""
Interactive Strategy Viewer for Colonel Blotto
───────────────────────────────────────────────
Browse ranked strategies from an algo file (default: out_algos.txt).

Usage:
    python avg_interactive.py                  # loads out_algos.txt
    python avg_interactive.py wo42_algos.txt    # loads a different file

Controls:
    ◀ / ▶ buttons   — step through strategies
    Left / Right     — keyboard shortcuts
    Slider           — scrub to any rank
"""

import sys
import ast
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
import matplotlib.colors as mcolors

# ── Load data ────────────────────────────────────────────────────────────────

def load_strategies(path: str) -> list[list[int]]:
    strategies = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                strategies.append(ast.literal_eval(line))
    return strategies


# ── Colour helpers ───────────────────────────────────────────────────────────

CMAP = plt.cm.coolwarm  # type: ignore[attr-defined]

def bar_colors(values, vmin=0, vmax=None):
    """Return an array of RGBA colours mapped from *values*."""
    if vmax is None:
        vmax = max(values) if max(values) > 0 else 1
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
    return [CMAP(norm(v)) for v in values]


# ── Build the figure ─────────────────────────────────────────────────────────

def main():
    filepath = sys.argv[1] if len(sys.argv) > 1 else "algos/out_algos.txt"
    strategies = load_strategies(filepath)
    n_strats = len(strategies)
    n_towers = len(strategies[0])

    # prefix sums for cumulative average
    prefix = np.zeros((n_strats + 1, n_towers))
    for i, s in enumerate(strategies):
        prefix[i + 1] = prefix[i] + np.array(s)

    # ── state ────────────────────────────────────────────────────────────
    state = {"idx": 0}   # mutable dict so closures can write to it

    x = np.arange(1, n_towers + 1)
    bar_width = 0.65

    # ── figure / axes ────────────────────────────────────────────────────
    fig = plt.figure(figsize=(11, 7.5))
    fig.canvas.manager.set_window_title(f"Strategy Viewer — {filepath}")
    fig.patch.set_facecolor("#1e1e2e")

    # layout: top‑bar, current‑chart, avg‑chart, slider, buttons
    ax_current = fig.add_axes([0.10, 0.52, 0.85, 0.38])
    ax_avg     = fig.add_axes([0.10, 0.16, 0.85, 0.32])
    ax_slider  = fig.add_axes([0.20, 0.06, 0.60, 0.03])
    ax_prev    = fig.add_axes([0.20, 0.01, 0.12, 0.04])
    ax_next    = fig.add_axes([0.68, 0.01, 0.12, 0.04])

    for ax in (ax_current, ax_avg):
        ax.set_facecolor("#2b2b3d")
        ax.tick_params(colors="white")
        ax.spines[["top", "right"]].set_visible(False)
        ax.spines[["bottom", "left"]].set_edgecolor("#555")
        ax.set_xticks(x)
        ax.set_xticklabels([str(i) for i in x], color="white")

    title_text = fig.text(0.50, 0.96, "", ha="center", va="center",
                          fontsize=16, fontweight="bold", color="white")
    strat_text = fig.text(0.50, 0.92, "", ha="center", va="center",
                          fontsize=11, color="#aaaacc", family="monospace")

    slider = Slider(ax_slider, "", 1, max(n_strats, 2),
                    valinit=1, valstep=1, color="#7f5af0")
    ax_slider.set_facecolor("#2b2b3d")

    btn_prev = Button(ax_prev, "◀  Prev", color="#3a3a5c", hovercolor="#7f5af0")
    btn_next = Button(ax_next, "Next  ▶", color="#3a3a5c", hovercolor="#7f5af0")
    for b in (btn_prev, btn_next):
        b.label.set_color("white")
        b.label.set_fontsize(11)

    # ── drawing ──────────────────────────────────────────────────────────

    def draw(idx: int):
        state["idx"] = idx
        strat = strategies[idx]
        cum_avg = prefix[idx + 1] / (idx + 1)

        # ── current strategy ─────────────────────────────────────────
        ax_current.cla()
        ax_current.set_facecolor("#2b2b3d")
        ax_current.spines[["top", "right"]].set_visible(False)
        ax_current.spines[["bottom", "left"]].set_edgecolor("#555")
        ax_current.tick_params(colors="white")
        ax_current.set_xticks(x)
        ax_current.set_xticklabels([str(i) for i in x], color="white")

        colors_cur = bar_colors(strat, vmax=max(max(strat), 1))
        max_val = max(strat)
        for j, v in enumerate(strat):
            ec = "#ffd700" if v == max_val and v > 0 else "white"
            lw = 2.2 if v == max_val and v > 0 else 0.5
            ax_current.bar(x[j], v, width=bar_width, color=colors_cur[j],
                           edgecolor=ec, linewidth=lw)
            ax_current.text(x[j], v + 0.5, str(v), ha="center", va="bottom",
                            fontsize=9, color="white")

        ax_current.set_ylabel("Soldiers", color="white", fontsize=10)
        ax_current.set_title("")
        top_margin = max(max(strat), 1) * 1.2
        ax_current.set_ylim(0, top_margin)

        # ── cumulative average ───────────────────────────────────────
        ax_avg.cla()
        ax_avg.set_facecolor("#2b2b3d")
        ax_avg.spines[["top", "right"]].set_visible(False)
        ax_avg.spines[["bottom", "left"]].set_edgecolor("#555")
        ax_avg.tick_params(colors="white")
        ax_avg.set_xticks(x)
        ax_avg.set_xticklabels([str(i) for i in x], color="white")

        colors_avg = bar_colors(cum_avg, vmax=max(max(cum_avg), 1))
        for j, v in enumerate(cum_avg):
            ax_avg.bar(x[j], v, width=bar_width, color=colors_avg[j],
                       edgecolor="white", linewidth=0.5)
            ax_avg.text(x[j], v + 0.3, f"{v:.1f}", ha="center", va="bottom",
                        fontsize=8, color="white")

        ax_avg.set_xlabel("Tower", color="white", fontsize=10)
        ax_avg.set_ylabel("Avg Soldiers", color="white", fontsize=10)
        ax_avg.set_title(f"Cumulative Average  (top {idx + 1} strategies)",
                         color="white", fontsize=12, pad=6)
        avg_top = max(max(cum_avg), 1) * 1.2
        ax_avg.set_ylim(0, avg_top)

        # ── header texts ─────────────────────────────────────────────
        title_text.set_text(f"Rank  {idx + 1} / {n_strats}")
        strat_text.set_text(str(strat))

        slider.set_val(idx + 1)
        fig.canvas.draw_idle()

    # ── callbacks ────────────────────────────────────────────────────────

    def go_prev(_event=None):
        if state["idx"] > 0:
            draw(state["idx"] - 1)

    def go_next(_event=None):
        if state["idx"] < n_strats - 1:
            draw(state["idx"] + 1)

    def on_slider(val):
        new_idx = int(val) - 1
        if new_idx != state["idx"]:
            draw(new_idx)

    def on_key(event):
        if event.key == "left":
            go_prev()
        elif event.key == "right":
            go_next()

    btn_prev.on_clicked(go_prev)
    btn_next.on_clicked(go_next)
    slider.on_changed(on_slider)
    fig.canvas.mpl_connect("key_press_event", on_key)

    # ── initial draw ─────────────────────────────────────────────────────
    draw(0)
    plt.show()


if __name__ == "__main__":
    main()
