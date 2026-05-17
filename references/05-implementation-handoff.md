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
- design measurements when numeric fidelity is requested
- design translation summary
- style carriers
- product/page goal
- platform
- primary viewport
- reference intent
- fidelity level
- existing project constraints
- code vs asset decisions
- asset manifest
- required states
- fallback strategy

## Handoff template

```md
# Implementation Brief

## Step Ledger
1. Reference intent - done
2. Visual reading - done
3. Measurement pass - skipped/done: [reason]
4. Asset manifest - done
5. Implementation brief - done
6. Confirmation - pending
7. Implementation - blocked until confirmation
8. Exit check - blocked until implementation

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
- design measurements:
- style carriers:
- code-vs-asset summary:

## Design measurements
Include this section when numeric fidelity is requested or the reference is a Fidelity Target.

- calibration:
- measured values:
- estimated values:
- inferred values:
- adaptation targets:
- responsive token recommendations:
- unknowns:
- tokens to use:

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

## Asset manifest
Use this for every image-based design-to-code request, even if the result is "no formal assets required".

| id | area | decision | output | required for MVP | fallback | needs user decision | generation plan / source path | notes |
|---|---|---|---|---|---|---|---|---|

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
[insert Asset Manifest or summary; do not omit for image-based requests]

## Image generation requests
Use this when any Asset Manifest row is marked Generate.
If a visible style-carrying asset is missing and the user has not chosen Source, Generate, or Fallback yet, stop here and ask for that asset decision before implementation.

- asset id:
- imagegen mode: generate / image-to-image edit
- reference image:
- target size/aspect:
- background:
- prompt:
- fallback:
- acceptance checks:

## Required states
- default
- empty
- loading
- error
- success
- disabled where relevant
- long text where relevant

## Implementation rules
- Respect the Step Ledger. If an earlier gate is missing, stop and complete that gate before implementation.
- Build structure first.
- Use `references/02-visual-reading-checklist.md` to translate image details into code decisions.
- Use `references/03-design-translation.md` to make source-of-truth, preserve/adapt/ignore, fidelity, and priority decisions explicit.
- Use `references/04-asset-workflow.md` for every image-based request.
- Preserve the listed style carriers; do not only recreate the information architecture.
- Do not silently downgrade visible style-carrying assets to CSS fallbacks; mark fallbacks and ask for confirmation.
- If the user approves Generate assets, run the Generate Asset Workflow before implementation and record generated file paths.
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
