"""Recreate Figure 3 and the leftmost panel of Figure 5 in video style.

The values and panel structure are taken from ``project_background/RPM v2.pdf``.
The visual treatment mirrors the dark Meta palette used by the Manim videos and
the existing Figure 2 recreation in this directory.

Run from anywhere with::

    .venv/bin/python graphs/figures3_and_5_recreation.py

Control the gap in the combined export with::

    .venv/bin/python graphs/figures3_and_5_recreation.py --combined-gap 0.75
"""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.patches import Patch
from PIL import Image
from pypdf import PageObject, PdfReader, PdfWriter
from pypdf.generic import DecodedStreamObject, NameObject


def find_project_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in (here.parent.parent, Path.cwd(), Path.cwd().parent):
        if (candidate / "project_background" / "RPM v2.pdf").exists():
            return candidate.resolve()
    raise FileNotFoundError("Could not locate project_background/RPM v2.pdf")


ROOT = find_project_root()
OUTPUT_DIR = ROOT / "graphs"
OUTPUT_DIR.mkdir(exist_ok=True)

OPTIMISTIC_REGULAR = Path("/Library/Fonts/OptimisticV5_Regular.ttf")
OPTIMISTIC_BOLD = Path("/Library/Fonts/OptimisticV5_Bold.ttf")
for font_path in (OPTIMISTIC_REGULAR, OPTIMISTIC_BOLD):
    if font_path.exists():
        font_manager.fontManager.addfont(font_path)

VIDEO_FONT = (
    font_manager.FontProperties(fname=OPTIMISTIC_REGULAR).get_name()
    if OPTIMISTIC_REGULAR.exists()
    else "DejaVu Sans"
)

# Shared animation palette (components/theme.py), plus the neutral extensions
# already used by graphs/figure2_recreation.ipynb.
BG = "#000000"
INK = "#FFFFFF"
INK_FAINT = "#67788A"
RULE = "#32383E"
SURFACE = "#0E1114"
PANEL_STROKE = "#3A424A"
BLUE = "#0064E0"
BLUE_LIGHT = "#47A5FA"
INFERENCE_ORANGE = "#F29040"

CONTEXT_COLORS = ("#FFD9B8", "#FBC18C", "#F7A45F", INFERENCE_ORANGE)
REASONING_COLORS = ("#FBC18C", INFERENCE_ORANGE)
SUGGESTION_COLORS = ("#FFD0A6", "#FBB77A", "#F69F57", INFERENCE_ORANGE)
TIME_COLORS = ("#86C9FC", BLUE_LIGHT, BLUE)

EXPORT_DPI = 240
DEFAULT_COMBINED_GAP = 0.75  # inches between the Figure 3 and Figure 5 blocks


def style_axes(ax, *, grid=True):
    """Apply the project-standard dark chart treatment."""
    ax.set_facecolor(BG)
    ax.tick_params(axis="both", colors=INK, labelsize=10.5, width=1.1)
    ax.xaxis.label.set_color(INK)
    ax.yaxis.label.set_color(INK)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(INK_FAINT)
        ax.spines[side].set_linewidth(1.25)
    if grid:
        ax.set_axisbelow(True)
        ax.grid(
            axis="y",
            color=RULE,
            linewidth=0.8,
            alpha=0.55,
            linestyle=(0, (1.0, 1.65)),
        )


def style_legend(legend):
    frame = legend.get_frame()
    frame.set_facecolor(SURFACE)
    frame.set_edgecolor(PANEL_STROKE)
    frame.set_alpha(0.94)
    for label in legend.get_texts():
        label.set_color(INK)


def label_bars(ax, bars, values, *, decimals=1, pad=0.22, size=10.2):
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + pad,
            f"{value:.{decimals}f}",
            ha="center",
            va="bottom",
            color=INK,
            fontsize=size,
            fontweight="bold",
            zorder=5,
        )


def make_figure3():
    """Figure 3: context, reasoning, and suggestion-count scaling."""
    context_labels = ("0", "1", "10", "100")
    context_accuracy = np.array([60.7, 60.9, 62.7, 65.0])

    reasoning_labels = ("low", "high")
    reasoning_accuracy = np.array([61.3, 63.4])

    suggestion_labels = ("n=2", "n=5", "n=10", "n=15")
    rpm_advantage = np.array([0.017, 0.030, 0.038, 0.045])
    oracle_advantage = np.array([0.073, 0.141, 0.188, 0.212])

    rc = {
        "font.family": VIDEO_FONT,
        "font.size": 10.5,
        "axes.labelsize": 12.5,
        "axes.labelweight": "normal",
        "xtick.color": INK,
        "ytick.color": INK,
        "text.color": INK,
        "hatch.linewidth": 1.0,
    }
    with plt.rc_context(rc):
        fig, axes = plt.subplots(1, 3, figsize=(14.2, 5.25))
        fig.patch.set_facecolor(BG)

        context_ax, reasoning_ax, suggestion_ax = axes
        for ax in axes:
            style_axes(ax)

        context_x = np.arange(len(context_labels))
        context_bars = context_ax.bar(
            context_x,
            context_accuracy,
            width=0.78,
            color=CONTEXT_COLORS,
            edgecolor=INK_FAINT,
            linewidth=1.25,
            zorder=3,
        )
        context_ax.set_ylim(50, 70)
        context_ax.set_yticks(np.arange(50, 71, 5))
        context_ax.set_xticks(context_x, context_labels)
        context_ax.set_xlabel("Context Nodes Presented")
        context_ax.set_ylabel("Accuracy (%)")
        label_bars(context_ax, context_bars, context_accuracy)

        reasoning_x = np.arange(len(reasoning_labels))
        reasoning_bars = reasoning_ax.bar(
            reasoning_x,
            reasoning_accuracy,
            width=0.80,
            color=REASONING_COLORS,
            edgecolor=INK_FAINT,
            linewidth=1.25,
            zorder=3,
        )
        reasoning_ax.set_ylim(50, 70)
        reasoning_ax.set_yticks(np.arange(50, 71, 5))
        reasoning_ax.set_xticks(reasoning_x, reasoning_labels)
        reasoning_ax.set_xlabel("Reasoning Effort")
        label_bars(reasoning_ax, reasoning_bars, reasoning_accuracy)

        suggestion_x = np.arange(len(suggestion_labels))
        width = 0.34
        rpm_bars = suggestion_ax.bar(
            suggestion_x - width / 2,
            rpm_advantage,
            width=width,
            color=SUGGESTION_COLORS,
            edgecolor=INK_FAINT,
            linewidth=1.25,
            zorder=3,
        )
        oracle_bars = suggestion_ax.bar(
            suggestion_x + width / 2,
            oracle_advantage,
            width=width,
            color=SUGGESTION_COLORS,
            edgecolor=INK,
            linewidth=0.65,
            hatch="//",
            zorder=3,
        )
        suggestion_ax.set_ylim(0.0, 0.28)
        suggestion_ax.set_yticks(np.arange(0.0, 0.251, 0.05))
        suggestion_ax.set_xticks(suggestion_x, suggestion_labels)
        suggestion_ax.set_xlabel("Suggestion Count")
        suggestion_ax.set_ylabel("Advantage over Average")
        label_bars(
            suggestion_ax,
            rpm_bars,
            rpm_advantage,
            decimals=3,
            pad=0.0035,
            size=7.8,
        )
        label_bars(
            suggestion_ax,
            oracle_bars,
            oracle_advantage,
            decimals=3,
            pad=0.0035,
            size=7.8,
        )
        legend_handles = (
            Patch(
                facecolor=SUGGESTION_COLORS[2],
                edgecolor=INK_FAINT,
                linewidth=1.0,
                label="RPM-selected",
            ),
            Patch(
                facecolor=SUGGESTION_COLORS[2],
                edgecolor=INK,
                linewidth=0.65,
                hatch="//",
                label="Oracle",
            ),
        )
        legend = suggestion_ax.legend(
            handles=legend_handles,
            loc="upper left",
            fontsize=9.5,
            borderpad=0.55,
            labelspacing=0.35,
            handlelength=2.2,
            handletextpad=0.65,
        )
        style_legend(legend)

        fig.subplots_adjust(
            left=0.058,
            right=0.992,
            bottom=0.175,
            top=0.885,
            wspace=0.27,
        )
        reasoning_bounds = reasoning_ax.get_position()
        fig.suptitle(
            "Inference-only RPM",
            x=(reasoning_bounds.x0 + reasoning_bounds.x1) / 2,
            y=0.985,
            color=INK,
            fontsize=17,
            fontweight="bold",
        )
        return fig


def make_figure5_left():
    """Figure 5, leftmost: selection accuracy by pilot time budget."""
    labels = ("5min", "30min", "4hour")
    accuracy = np.array([78.52, 82.78, 84.02])

    rc = {
        "font.family": VIDEO_FONT,
        "font.size": 10.5,
        "axes.labelsize": 12.5,
        "axes.labelweight": "normal",
        "xtick.color": INK,
        "ytick.color": INK,
        "text.color": INK,
    }
    with plt.rc_context(rc):
        fig, ax = plt.subplots(figsize=(6.0, 5.25))
        fig.patch.set_facecolor(BG)
        style_axes(ax)

        x = np.arange(len(labels))
        bars = ax.bar(
            x,
            accuracy,
            width=0.58,
            color=TIME_COLORS,
            edgecolor=INK_FAINT,
            linewidth=1.25,
            zorder=3,
        )

        ax.set_xlim(-0.46, 2.46)
        ax.set_ylim(60, 95)
        ax.set_yticks(np.arange(60, 96, 5))
        ax.set_xticks(x, labels)
        ax.set_xlabel("Time-budget")
        ax.set_ylabel("Accuracy (%)")
        label_bars(ax, bars, accuracy, decimals=2, pad=0.34, size=10.4)

        fig.subplots_adjust(left=0.15, right=0.985, bottom=0.18, top=0.885)
        axis_bounds = ax.get_position()
        fig.suptitle(
            "Agentic RPM",
            x=(axis_bounds.x0 + axis_bounds.x1) / 2,
            y=0.985,
            color=INK,
            fontsize=17,
            fontweight="bold",
        )
        return fig


def save_figure(fig, stem):
    png = OUTPUT_DIR / f"{stem}.png"
    pdf = OUTPUT_DIR / f"{stem}.pdf"
    save_options = {"facecolor": BG, "bbox_inches": "tight", "pad_inches": 0.06}
    fig.savefig(png, dpi=EXPORT_DPI, **save_options)
    fig.savefig(pdf, **save_options)
    plt.close(fig)
    return png, pdf


def combine_png(left_path, right_path, output_path, gap_inches):
    """Combine two raster exports with a physical-size gap on a black canvas."""
    left = Image.open(left_path).convert("RGB")
    right = Image.open(right_path).convert("RGB")
    gap_px = round(gap_inches * EXPORT_DPI)
    height = max(left.height, right.height)
    canvas = Image.new("RGB", (left.width + gap_px + right.width, height), BG)
    canvas.paste(left, (0, (height - left.height) // 2))
    canvas.paste(right, (left.width + gap_px, (height - right.height) // 2))
    canvas.save(output_path, dpi=(EXPORT_DPI, EXPORT_DPI))


def combine_pdf(left_path, right_path, output_path, gap_inches):
    """Combine two vector PDF pages while filling the adjustable gap black."""
    left_page = PdfReader(left_path).pages[0]
    right_page = PdfReader(right_path).pages[0]
    left_width = float(left_page.mediabox.width)
    left_height = float(left_page.mediabox.height)
    right_width = float(right_page.mediabox.width)
    right_height = float(right_page.mediabox.height)
    gap_points = gap_inches * 72.0
    width = left_width + gap_points + right_width
    height = max(left_height, right_height)

    page = PageObject.create_blank_page(width=width, height=height)
    background = DecodedStreamObject()
    background.set_data(f"0 0 0 rg 0 0 {width} {height} re f\n".encode("ascii"))
    page[NameObject("/Contents")] = background
    page.merge_translated_page(left_page, 0, (height - left_height) / 2)
    page.merge_translated_page(
        right_page,
        left_width + gap_points,
        (height - right_height) / 2,
    )

    writer = PdfWriter()
    writer.add_page(page)
    with output_path.open("wb") as output_file:
        writer.write(output_file)


def combine_figure_exports(figure3_outputs, figure5_outputs, gap_inches):
    """Create matching PNG and vector-PDF side-by-side compositions."""
    combined_png = OUTPUT_DIR / "figure3_and_figure5_combined_dark.png"
    combined_pdf = OUTPUT_DIR / "figure3_and_figure5_combined_dark.pdf"
    combine_png(
        figure3_outputs[0],
        figure5_outputs[0],
        combined_png,
        gap_inches,
    )
    combine_pdf(
        figure3_outputs[1],
        figure5_outputs[1],
        combined_pdf,
        gap_inches,
    )
    return combined_png, combined_pdf


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--combined-gap",
        type=float,
        default=DEFAULT_COMBINED_GAP,
        metavar="INCHES",
        help=(
            "horizontal gap between Figure 3 and Figure 5 in the combined "
            f"export (default: {DEFAULT_COMBINED_GAP})"
        ),
    )
    args = parser.parse_args()
    if args.combined_gap < 0:
        parser.error("--combined-gap must be non-negative")
    return args


def main():
    args = parse_args()
    outputs = []
    figure3_outputs = save_figure(make_figure3(), "figure3_recreated_dark")
    figure5_outputs = save_figure(
        make_figure5_left(),
        "figure5_left_recreated_dark",
    )
    combined_outputs = combine_figure_exports(
        figure3_outputs,
        figure5_outputs,
        args.combined_gap,
    )
    outputs.extend(figure3_outputs)
    outputs.extend(figure5_outputs)
    outputs.extend(combined_outputs)
    print("Saved:")
    for output in outputs:
        print(f"  {output}")


if __name__ == "__main__":
    main()
