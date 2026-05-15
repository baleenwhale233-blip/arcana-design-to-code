# Implementation Handoff

## Goal

Produce a concise brief that a coding agent can implement without guessing.

The handoff should translate design intent into product implementation.

Use this for every initial design-to-code request.

Even if the user asks to build, implement, recreate, restore, or make the UI now, produce the brief first and stop for confirmation.

Only use Implementation Mode from `SKILL.md` after the user approves the brief and explicitly asks to proceed.

## Before writing the handoff

Make sure these are known or assumed:

- visual reading notes
- design translation summary
- style carriers
- product/page goal
- platform
- primary viewport
- reference intent
- fidelity level
- existing project constraints
- code vs asset decisions
- required states
- fallback strategy

## Handoff template

```md
# Implementation Brief

## Page
[page name]

## Goal
[what the user should accomplish]

## Platform and viewport
- platform:
- primary viewport:
- responsive requirement:

## Reference intent
- image:
- intent:
- fidelity level:

## Visual reading summary
- layout blocks:
- visual tokens:
- style carriers:
- code-vs-asset summary:

## Design translation summary
- source of truth:
- user task:
- information structure:
- visual direction:
- fidelity decision:
- preserve:
- adapt:
- ignore:
- implementation priorities:

## Style carriers to preserve
| carrier | preserve | implementation decision | notes |
|---|---|---|---|

## Existing constraints
- reuse existing components:
- reuse existing routes/data models:
- avoid new dependencies:
- design tokens:

## User flow
1. ...
2. ...
3. ...

## Information structure
- section:
  - content:
  - actions:
  - states:

## Components to build/reuse
- component:
  - source: existing / new
  - notes:

## Visual direction
- mood:
- typography:
- color:
- spacing:
- radius/shadow:
- density:

## Code vs asset decisions
[insert Asset Manifest or summary]

## Required states
- default
- empty
- loading
- error
- success
- disabled where relevant
- long text where relevant

## Implementation rules
- Build structure first.
- Use `references/02-visual-reading-checklist.md` to translate image details into code decisions.
- Use `references/03-design-translation.md` to make source-of-truth, preserve/adapt/ignore, fidelity, and priority decisions explicit.
- Preserve the listed style carriers; do not only recreate the information architecture.
- Follow the approved Design Translation Summary; do not replace it with private reinterpretation during implementation.
- Match information hierarchy before visual decoration.
- Prefer code for layout and normal UI.
- Use image assets only where listed.
- Do not use the mockup as a background image.
- Do not chase pixel-perfect differences.
- Preserve product usability over mockup details.

## Fallbacks
- [asset fallback]
- [data fallback]
- [interaction fallback]

## Assumptions
- ...

## Exit check
Use `references/06-exit-check.md`.

## Confirmation
Ask: "确认按这个 brief 开始实现吗？"

## Handoff style

Keep it practical.

Avoid:

long design essays
pixel-level instructions
excessive style adjectives
vague instructions like "make it modern"

Prefer:

concrete components
concrete states
real example data
implementation priorities
explicit tradeoffs
```
