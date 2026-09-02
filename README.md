# Making Manim animations

[Manim](https://www.manim.community/) is a Python library for programmatic
animation, written by Grant Sanderson ([**3Blue1Brown**](https://www.youtube.com/@3blue1brown)) for his math videos.

This repo is a worked example including two short clips explaining **AI Research
Preference Models**.

<table>
<tr>
<td width="50%" align="center">
<video src="assets/Video1WhyRPM.mp4" controls muted loop width="100%"></video>
<br><sub><b>Video 1</b> — RPM Motivation</sub>
</td>
<td width="50%" align="center">
<video src="assets/Video2RPMVariants.mp4" controls muted loop width="100%"></video>
<br><sub><b>Video 2</b> — RPM Variants</sub>
</td>
</tr>
</table>

## 1. Let a coding agent write the first draft

Point **Claude Code**, **Codex**, or **Muse Code** at an empty repo and describe
the animation you want.

The first demo is a start, not a finish. You'll have something moving in
minutes, and it will be approximately right and subtly wrong — overlapping text,
arrows landing off-target, beats too fast to read. The animations here took a
weekend to get right. Budget for that: the agent gets you to 70%, and the rest
is you watching a render, describing what's off, and going again.

Work in small loops. Render low quality, watch, fix one thing, repeat.

## 2. Use Manim Sideview in VS Code

Install [**Manim Sideview**](https://marketplace.visualstudio.com/items?itemName=Rickaym.manim-sideview).
It renders the scene under your cursor and plays it in a panel next to your
code, so you're not alt-tabbing to a video player after every change. Given how
much iteration step 1 implies, this is the biggest quality-of-life win
available.

## 3. Give the agent your project background

An agent that doesn't know your subject will invent plausible nonsense. Put the
source material in the repo and tell it to read it:

```
project_background/
  RPM v2.pdf              the paper being explained
  RPM.png                 Figure 1 — the diagram being animated
  sample_meta_images/     reference decks for visual style
```

The paper supplies the content — what terms mean, which details matter. The
figure supplies the structure to animate. Skip this and you'll spend your
iteration budget correcting facts instead of polishing motion.

## 4. Give it visual references

Drop screenshots of the look you're targeting into the repo and the agent will
sample colors and layout from them rather than defaulting to stock blue-on-white.

### Meta styling

The house look: **pure black ground, Meta blue as the only loud accent,
everything else greyscale.**

Fonts (installed in `/Library/Fonts`):

| Font | Use |
|---|---|
| `Optimistic` | body text, labels, captions |
| `Facebook Sans App` | section titles and headers |

| Role | Hex |
|---|---|
| Ground | `#000000` |
| Primary text | `#FFFFFF` |
| Secondary text | `#A7B3BF` |
| Tertiary text / faint arrows | `#67788A` |
| Hairlines, dividers | `#32383E` |
| **Meta blue (primary)** | `#0064E0` |
| **Meta blue (light accent)** | `#47A5FA` |
| Meta blue (deep) | `#003270` |
| Peach callout | `#FABE82` |
| Panel fill | `#0E1114` |
| Inset fill | `#171C21` |

The blues carry the emphasis; anything you don't want looked at stays grey.

Keep all of it in one file — this repo uses `components/theme.py` for palette,
type sizes, and timing. Changing the look stays a one-file edit.

## 5. Split long videos into act files

Re-rendering a four-minute scene to tweak its ending gets old fast. Give each
act its own file and standalone scene, with a thin orchestrator on top:

```
scenes/
  video1_common.py    shared geometry, styling, pacing
  video1_act1.py      Act 1  -> Video1Act1
  video1_act2.py      Act 2  -> Video1Act2
  video1_act3.py      Act 3  -> Video1Act3
  video1.py           orchestrator -> Video1WhyRPM
```

Each act exposes its timeline as a mixin; the orchestrator inherits all three
and plays them in order. Iterate on Act 3 in seconds, render the whole thing
once when it's right.

## Setup

Manim needs cairo, pango, and ffmpeg. Use conda-forge, which ships them prebuilt:

```bash
mamba env create -p ./.venv -f environment.yml
```

You get Manim Community 0.20.1, ffmpeg, and Python 3.12 in `./.venv`.

### LaTeX (optional)

Only needed for `Tex` / `MathTex`. The scenes here use Pango `Text` only, so
they render without it.

Use BasicTeX:

```bash
brew install --cask basictex
eval "$(/usr/libexec/path_helper)"
sudo tlmgr update --self
sudo tlmgr install standalone preview doublestroke relsize fundus-calligra \
  wasysym physics dvisvgm jknapltx wasy cm-super babel-english gnu-freefont \
  mathastext cbfonts-fd
```

## What's in this repo

```
scenes/
  video1.py              Video 1 — "Why do we need an RPM?"
  video1_common.py       shared geometry, styling, pacing for the acts
  video1_act1.py         Act 1 — the compute-allocation problem
  video1_act2.py         Act 2 — the RPM solution
  video1_act3.py         Act 3 — research-agent integration
  video2.py              Video 2 — "How does the RPM decide?"
components/
  theme.py               palette, type, timing  <- change the look here
  base.py                RPMScene / RPMMovingScene (black ground)
  node.py                the four node states from Figure 1
  tree.py                SearchTree, edges, Figure 1 layout
  candidate.py           CandidateCard (plan + code), candidate rails
  candidate_diagrams.py  small architecture icons for candidate cards
  rpm.py                 RPMBox, funnel/fan/curved arrows, tournament ladder
  gpu.py                 GPUBox (expensive), SandboxBox (cheap pilot), Clock
  agent.py               AgentBox
  labels.py              captions, step badges, stage strips, pills
  anims.py               dimmed(), travel()
project_background/      the paper, Figure 1, and style references
manim.cfg                project-wide render defaults
```

Both videos are built from the same `components/`, so the tree, RPM box, and
candidate rail are literally the same objects across the two clips.

## Rendering

```bash
# low quality (480p15) — the iteration loop
.venv/bin/manim render -ql scenes/video1.py Video1WhyRPM
.venv/bin/manim render -ql scenes/video2.py Video2HowRPM

# a single act
.venv/bin/manim render -ql scenes/video1_act1.py Video1Act1
.venv/bin/manim render -ql scenes/video1_act2.py Video1Act2
.venv/bin/manim render -ql scenes/video1_act3.py Video1Act3

# final 1080p60
.venv/bin/manim render -qh scenes/video1.py Video1WhyRPM
.venv/bin/manim render -qh scenes/video2.py Video2HowRPM
```

Output lands in `media/videos/<file>/<resolution>/<Scene>.mp4`.
