#!/usr/bin/env python
"""Render the AI Research Preference Model animations.

    python main.py preview          # both videos, 480p15
    python main.py final            # both videos, 1080p60
    python main.py preview 1        # just Video 1
    python main.py preview 1a       # just Video 1, Act 1
    python main.py preview 1b       # just Video 1, Act 2
    python main.py preview 1c       # just Video 1, Act 3
    python main.py still 2          # last frame of Video 2 as a PNG

Equivalent raw commands are in README.md; this is just a shortcut.
"""

import argparse
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
MANIM = ROOT / ".venv" / "bin" / "manim"

VIDEOS = {
    "1": ("scenes/video1.py", "Video1WhyRPM"),
    "2": ("scenes/video2.py", "Video2HowRPM"),
}

ACTS = {
    "1a": ("scenes/video1_act1.py", "Video1Act1"),
    "1b": ("scenes/video1_act2.py", "Video1Act2"),
    "1c": ("scenes/video1_act3.py", "Video1Act3"),
}

TARGETS = {**VIDEOS, **ACTS}

QUALITY = {
    "preview": ["-ql"],            # 480p15  — fast iteration
    "medium": ["-qm"],             # 720p30
    "final": ["-qh"],              # 1080p60 — what to post
    "4k": ["-qk"],                 # 2160p60
    "still": ["-qh", "-s"],        # last frame only, as a PNG
}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("quality", choices=sorted(QUALITY), nargs="?", default="preview")
    ap.add_argument(
        "which",
        choices=sorted(TARGETS) + ["all"],
        nargs="?",
        default="all",
    )
    ap.add_argument("--no-cache", action="store_true",
                    help="force a full re-render")
    args = ap.parse_args()

    manim = str(MANIM) if MANIM.exists() else "manim"
    targets = sorted(VIDEOS) if args.which == "all" else [args.which]

    for key in targets:
        path, scene = TARGETS[key]
        cmd = [manim, "render", *QUALITY[args.quality]]
        if args.no_cache:
            cmd.append("--disable_caching")
        cmd += [path, scene]
        print(f"\n$ {' '.join(cmd)}\n", flush=True)
        result = subprocess.run(cmd, cwd=ROOT)
        if result.returncode:
            sys.exit(result.returncode)


if __name__ == "__main__":
    main()
