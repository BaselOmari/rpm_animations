# RPM animations

Two short Manim clips for a Twitter/X thread on **AI Research Preference Models**
(Foster, Al Omari, Fu et al.). Both are animated readings of Figure 1 and
Sections 2.2 / 3 / 3.1 / 3.2 / 3.3.

| Scene | File | Length | Question it answers |
|---|---|---|---|
| `Video1WhyRPM` | `scenes/video1.py` | ~37 s | Why do we need an RPM? |
| `Video2HowRPM` | `scenes/video2.py` | ~28 s | How does the RPM decide? |

Video 2 follows by opening the black-box preference decision introduced in
Video 1 and comparing two ways an RPM can make that choice.

## Rendering

```bash
# low-quality previews (480p15) — fast iteration
.venv/bin/manim render -ql scenes/video1.py Video1WhyRPM
.venv/bin/manim render -ql scenes/video2.py Video2HowRPM

# individual Video 1 acts
.venv/bin/manim render -ql scenes/video1_act1.py Video1Act1
.venv/bin/manim render -ql scenes/video1_act2.py Video1Act2
.venv/bin/manim render -ql scenes/video1_act3.py Video1Act3

# final 1080p60 — what to post
.venv/bin/manim render -qh scenes/video1.py Video1WhyRPM
.venv/bin/manim render -qh scenes/video2.py Video2HowRPM

# 4K, if you want headroom for cropping
.venv/bin/manim render -qk scenes/video1.py Video1WhyRPM
```

Useful flags: `-p` opens the result, `-s` renders only the last frame as a PNG,
`--disable_caching` forces a full re-render (needed after editing `components/`,
since Manim only hashes the scene file).

Or via the shortcut runner:

```bash
python main.py preview        # both, 480p15
python main.py final          # both, 1080p60
python main.py final 1        # just Video 1
python main.py preview 1a     # just Video 1, Act 1
python main.py preview 1b     # just Video 1, Act 2
python main.py preview 1c     # just Video 1, Act 3
python main.py still 2        # last frame of Video 2 as a PNG
```

Output lands in `media/videos/<file>/<resolution>/<Scene>.mp4`.

## Structure

```
main.py                  render shortcut
scenes/
  video1.py              combined Video 1 orchestrator
  video1_common.py       shared Video 1 components and pacing
  video1_act1.py         compute-allocation problem
  video1_act2.py         RPM solution
  video1_act3.py         research-agent integration
  video2.py              "How does the RPM decide?"   — 5 beats
components/
  theme.py               palette, type, timing  ← change the look here
  base.py                RPMScene / RPMMovingScene (black ground)
  node.py                SolutionNode + the four Figure 1 states
  tree.py                SearchTree, edges, Figure 1 layout, retarget_tree
  figure1.py             the shared "Select Child Using RPM" composition
  candidate.py           CandidateCard (plan + code), candidate rails
  rpm.py                 RPMBox, funnel/fan/curved arrows, tournament ladder
  gpu.py                 GPUBox (expensive), SandboxBox (cheap pilot), Clock
  agent.py               AgentBox
  labels.py              captions, step badges, Figure 1 stage strip, pills
  anims.py               dimmed(), travel()
project_background/      the paper, Figure 1, and Meta style references
```

Both scenes are built from the same components, so the tree, the RPM box and the
candidate rail are literally the same objects across the two videos.

## Visual language

Dark Meta house style: pure black ground, **Optimistic** type, Meta blue as the
single loud accent. Colours are sampled from
`project_background/sample_meta_images/`; the node *semantics* come from Figure 1
of the paper.

| Element | Meaning | Colour |
|---|---|---|
| Green circle with a score | executed solution, has a validation score | `#0D2A20` / `#3ED598` |
| Red circle, no score | executed, buggy / failed | `#2C1418` / `#FA8282` |
| Grey circle, letter label | candidate mutation, **not** executed | `#14181C` / `#67788A` |
| Blue circle | the candidate the RPM selected | `#0064E0` / `#47A5FA` |
| Warm plate behind a node | parent currently being mutated | `#FABE82` |
| White arrow | tree edge (a mutation) | `#FFFFFF` |
| Blue arrow | RPM-selected flow | `#47A5FA` |
| Peach | compute cost / GPU time | `#FABE82` |

Everything routes through `components/theme.py` — swapping the palette or the
typeface is a one-file change.

## What the videos say

**Video 1.** Three distinct acts establish the compute-allocation problem,
introduce an RPM as a black-box selector, and show where it plugs into the
research-agent search loop. It stops after the RPM selects a child, before that
child is executed or added back to the tree.

**Video 2.** A fixed split-screen comparison contrasts an inference-only RPM,
which reasons from existing evidence, with an agentic RPM, which first gathers
evidence from small pilot experiments. It explains the decision mechanisms that
Video 1 intentionally leaves inside the black box.

Figure 1 selects candidate **A**. Video 1 uses **C**; Video 2 uses **C** for the
inference-only side and **D** for the agentic side.

## Environment

The env lives in `./.venv` and was built with **micromamba + conda-forge**, not pip.
Homebrew is not writable on this machine and `pycairo` has no macOS wheel, so
`pip install manim` fails to build; conda-forge ships cairo/pango/ffmpeg prebuilt.

```bash
mamba env create -p ./.venv -f environment.yml
```

Installed: Manim Community 0.20.1, ffmpeg 9.0.1, Python 3.12.

**LaTeX is not installed**, so these scenes use Pango `Text` only — no `Tex` or
`MathTex` anywhere. Keep it that way unless you install BasicTeX:

```bash
brew install --cask basictex
eval "$(/usr/libexec/path_helper)"
sudo tlmgr update --self
sudo tlmgr install standalone preview doublestroke relsize fundus-calligra \
  wasysym physics dvisvgm jknapltx wasy cm-super babel-english gnu-freefont \
  mathastext cbfonts-fd
```

**Optimistic** must be installed system-wide (it is, in `/Library/Fonts`). Without
it Pango silently falls back and the type goes off-brand.

## Gotchas hit while building this

- Manim hoists any **submobject** you animate to the top of the scene's draw
  order, permanently. Animating `box.panel` leaves the panel painted over its own
  label. Animate the whole group, or re-`add()` the parent afterwards.
- `Mobject.set_opacity()` sets fill *and* stroke opacity absolutely, so on a curve
  drawn with `fill_opacity=0` it paints in the region between the curve and its
  chord — invisible on white, a grey wedge on black. Use `dimmed()` from
  `components/anims.py`, which scales existing opacities instead.
- `CubicBezier` is not a `TipableVMobject`, so `.add_tip()` does not exist. Use
  `curved_arrow()` in `components/rpm.py`, which places the head by hand.
- PyPI needs `--cert /etc/ssl/cert.pem` here; the corp proxy's CA is not in
  certifi's bundle. Don't `pip install` cairo/pango-backed packages into `.venv`;
  use `mamba`.

`project_background/` is reference material — leave it as is.
