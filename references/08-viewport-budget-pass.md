# Viewport Budget Pass

## Goal

Prevent measured UI values from producing an implementation that overflows the target viewport.

Use this for full-screen mobile, player-like, dashboard-like, tool-like, kiosk-like, modal-like, or no-scroll screens.
Also use it whenever the user says the implementation has layout overflow, page height problems, or the reference must fit a target viewport such as 390x844.

## Core rule

Measurement is not layout budgeting.

Do not treat screenshot height as usable CSS content height.
The screenshot may include status bars, home indicators, visual whitespace, browser chrome, or mockup-only safe areas.
The implementation may add shell padding, headers, default button hit areas, line-height, min-height, margins, framework defaults, and runtime controls.

Before implementation, sum the planned CSS height budget.

## Required inputs

- target viewport: width x height
- scroll policy: no-scroll / content-scroll / panel-scroll
- shell and safe padding: top, bottom, page padding
- fixed sections: header, media, title, metadata, progress, controls, toolbars, bottom actions
- gaps and margins between sections
- min-heights and hit areas from real controls
- responsive targets if more than one viewport must fit

If scroll policy is unknown:

- use no-scroll for player-like, tool-like, or single-screen mobile experiences
- use content-scroll only for document/feed/content-flow pages

## Process

1. Decide the scroll policy.
   If the screen is a player, editor, control surface, dashboard panel, or compact mobile tool, default to no-scroll.

2. Compute available height.
   Start with target viewport height.
   Subtract app shell, mobile shell, safe-area padding, header chrome, bottom chrome, and required outer padding.

3. List every vertical section.
   Include header, media, title, metadata, progress, controls, secondary tools, bottom actions, and hidden default min-heights.

4. List every vertical gap.
   Include margins, row gaps, panel gaps, padding top/bottom, default line-height overflow, and button hit-area padding.

5. Add the budget.
   If total exceeds available height, revise before implementation.

6. Compress intentionally.
   Prefer reducing gaps, min-heights, hit areas, and redundant shell padding before shrinking primary content.
   Do not shrink tap targets below platform usability unless the user approves a dense mode.

7. Record CSS constraints.
   Note max-heights, clamp values, flex behavior, overflow policy, and which elements may shrink.

## Script workflow

Use `scripts/viewport_budget.py` for explicit budget math:

```bash
python3 scripts/viewport_budget.py \
  --viewport 390x844 \
  --scroll-policy no-scroll \
  --reserve shell-top:16 \
  --reserve shell-bottom:20 \
  --item header:48 \
  --item cover:320 \
  --item title:54 \
  --item progress:34 \
  --item controls:72 \
  --item tools:56 \
  --gap header-cover:10 \
  --gap cover-title:14 \
  --gap title-progress:14 \
  --gap progress-controls:16 \
  --gap controls-tools:18
```

The script only checks arithmetic. The agent must decide which sections exist and how to compress them.

## Output template

```md
## Viewport Budget

- target viewport:
- scroll policy:
- available height:
- reserved shell/safe height:

| section | planned height | can shrink | notes |
|---|---:|---|---|
| header | 48px | yes | avoid copying status bar height |

| gap/padding | planned height | notes |
|---|---:|---|
| controls margin top | 16px | measured 28px was too loose |

- total planned height:
- remaining/overflow:
- pass/fail:
- compression plan:
- CSS constraints:
```

## Common failure points

- copying status-bar whitespace into mobile web
- header `min-height` plus margin that double-counts top space
- SVG visual size plus button min-height plus row gap
- control panels with large `gap`, `margin-top`, and `margin-bottom`
- bottom tool items with large min-height and padding
- media/cover size chosen without summing the rest of the page
- framework or browser default styles adding hidden height
