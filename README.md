# Making Manim animations

[Manim](https://www.manim.community/) is a Python library for programmatic
animation, originally written by Grant Sanderson (**3Blue1Brown**) to make his
math videos and now maintained by the community as Manim Community Edition.

This repo is a worked example — two short clips explaining **AI Research
Preference Models** — but the point of this README is the method, not the paper.
Here's how to make your own.

## 1. Let a coding agent write the first draft

Don't hand-write Manim from a blank file. Point **Claude Code**, **Codex**, or
**Muse Code** at an empty repo and describe the animation you want.

The catch: **the first demo is a start, not a finish.** You'll get something
moving on screen in a few minutes, and it will look approximately right and
subtly wrong — text overlapping, arrows landing in the wrong place, beats that
run too fast to read. That's normal. Perfecting the animations in this repo took
a full weekend of iteration. Budget for that. The agent gets you to 70% fast,
and the last 30% is you watching a render, describing exactly what's off, and
re-rendering.

Work in small loops: render at low quality, watch it, fix one thing, repeat.

## 2. Give the agent your project background

An agent that doesn't know your subject will invent plausible nonsense. Put the
source material in the repo and tell the agent to read it.

This repo keeps it in `project_background/`:

```
project_background/
  RPM v2.pdf              the paper the animation explains
  RPM.png                 Figure 1 — the diagram being animated
  sample_meta_images/     reference decks for visual style
```

The paper gives the agent the *content* — what the terms mean, what the figure
is claiming, which detail matters. The figure gives it the *structure* to animate.
Without these you will spend your iteration budget correcting facts instead of
polishing motion.

## 3. Give it visual references too

`project_background/sample_meta_images/` holds screenshots of existing branded
decks and figures. Drop in a few images of the look you're targeting and the
agent will sample colors and layout conventions from them instead of defaulting
to Manim's stock blue-on-white.

### Meta styling

If you want the Meta house look, the recipe is: **pure black ground, Meta blue as
the single loud accent, everything else greyscale.**

Fonts — installed system-wide in `/Library/Fonts`:

| Font | Use |
|---|---|
| `Optimistic` | Meta's brand face; body text, labels, captions |
| `Facebook Sans App` | section titles and headers |

Pango silently falls back to a default face if the font isn't installed, and the
type quietly goes off-brand — check your first render for this.

Core colors:

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

The blues carry all the emphasis. Everything that isn't the thing you want
looked at should be grey.

**Put all of this in one file.** This repo uses `components/theme.py` — palette,
type sizes, and timing constants in a single module that every scene imports.
Changing the look becomes a one-file edit instead of a find-and-replace across
every scene.

## 4. Split long videos into act files

A four-minute animation in one file is miserable to iterate on: every tweak to
the ending means re-rendering the beginning.

Split it. Each act is its own file with its own independently renderable scene,
plus a thin orchestrator that plays them back to back:

```
scenes/
  video1_common.py    shared geometry, styling, pacing for all acts
  video1_act1.py      Act 1  -> renders standalone as Video1Act1
  video1_act2.py      Act 2  -> renders standalone as Video1Act2
  video1_act3.py      Act 3  -> renders standalone as Video1Act3
  video1.py           orchestrator -> plays all three as Video1WhyRPM
```

Each act exposes its timeline as a mixin, and the orchestrator inherits all
three and calls them in order. Now you can iterate on Act 3 alone in seconds,
then render the whole thing once when it's right. Anything shared between acts
lives in `video1_common.py`.

## 5. Use the Manim Sideview extension in VS Code

Install [**Manim Sideview**](https://marketplace.visualstudio.com/items?itemName=Rickaym.manim-sideview).
It renders the scene your cursor is in and plays the result in a panel beside
your code, so you're not alt-tabbing to a video player after every change. This
is the single biggest quality-of-life upgrade for the tight iteration loop that
step 1 requires.

## Setup

Manim needs cairo, pango, and ffmpeg — all native libraries. On a locked-down
machine (no writable Homebrew) `pip install manim` fails, because `pycairo` has
no macOS wheel and tries to build from source. **Use conda-forge**, which ships
them prebuilt:

```bash
mamba env create -p ./.venv -f environment.yml
```

That gives you Manim Community 0.20.1, ffmpeg, and Python 3.12 in `./.venv`.

### LaTeX (optional)

You only need LaTeX if you use `Tex` or `MathTex`. The scenes here deliberately
don't — they use Pango `Text` only, so they render with no TeX installed.

Don't install conda-forge's `texlive-core`: it ships an empty texmf tree, no
`dvisvgm`, and a broken `tlmgr`. Use BasicTeX:

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
  video1.py              Video 1 orchestrator — "Why do we need an RPM?"
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

Both videos are built from the same `components/`, so the tree, the RPM box, and
the candidate rail are literally the same objects across the two clips.

## Rendering

```bash
# low quality (480p15) — the iteration loop
.venv/bin/manim render -ql scenes/video1.py Video1WhyRPM
.venv/bin/manim render -ql scenes/video2.py Video2HowRPM

# a single act, while you're working on it
.venv/bin/manim render -ql scenes/video1_act1.py Video1Act1
.venv/bin/manim render -ql scenes/video1_act2.py Video1Act2
.venv/bin/manim render -ql scenes/video1_act3.py Video1Act3

# final 1080p60 — what you post
.venv/bin/manim render -qh scenes/video1.py Video1WhyRPM
.venv/bin/manim render -qh scenes/video2.py Video2HowRPM
```

Output lands in `media/videos/<file>/<resolution>/<Scene>.mp4`.

Useful flags:

- `-p` — open the result when it finishes
- `-s` — render only the last frame, as a PNG
- `--disable_caching` — force a full re-render. **You need this after editing
  anything in `components/`**, because Manim only hashes the scene file and will
  happily serve you a stale cached render otherwise.

## Gotchas worth knowing up front

These cost real time to diagnose:

- Manim **hoists any submobject you animate to the top of the draw order**,
  permanently. Animating `box.panel` leaves the panel painted over its own label.
  Animate the whole group, or re-`add()` the parent afterwards.
- `Mobject.set_opacity()` sets fill *and* stroke opacity absolutely. On a curve
  drawn with `fill_opacity=0` it fills the region between the curve and its
  chord — invisible on white, an obvious grey wedge on black. Scale the existing
  opacities instead; see `dimmed()` in `components/anims.py`.
- `CubicBezier` is not a `TipableVMobject`, so `.add_tip()` doesn't exist. Place
  the arrowhead by hand — see `curved_arrow()` in `components/rpm.py`.
- Fonts fail silently. If the type looks generic, the font name didn't resolve.

## History

The full exploratory history — figure recreations, alternate Video 2 variants,
scratch scenes, and a render shortcut script — lives on the `dev` branch.
