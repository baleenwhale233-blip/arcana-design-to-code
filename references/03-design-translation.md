# Design Translation

## Goal

Translate a reference image or design direction into implementation intent.

Do not ask "how do I copy this image?"
Ask:

1. What is the source of truth?
2. What must be preserved?
3. What may be adapted?
4. What should be ignored?
5. What should become code?
6. What should become image asset?

The initial Implementation Brief must include a concise Design Translation Summary.
Do not hide this as private reasoning when the user is doing design-to-code work.

## Priority order

P0 — Product function
- primary user task
- required user actions
- required data
- empty/loading/error/success states
- navigation and flow

P1 — Information architecture
- module order
- hierarchy
- primary vs secondary actions
- content grouping
- scanning path

P2 — Visual system
- typography scale
- spacing rhythm
- color mood
- component density
- radius and shadow language

P3 — Decorative details
- texture
- illustration fidelity
- complex gradients
- background ornaments
- AI-generated visual flourishes

Do not optimize P3 before P0–P2 are working.

## What to preserve

Preserve:
- page goal
- user flow
- information hierarchy
- main layout rhythm
- visual mood when explicitly requested
- existing project conventions unless user asks to change them

## What may change

May change:
- exact spacing
- exact icon choice
- generated fake text
- decorative details
- card shapes when needed for usability
- layout when adapting from mobile to desktop or desktop to mobile

Do not loosen exact spacing, radius, or type sizes when the user explicitly asks for numeric values or the reference is a Fidelity Target.
In that case, preserve measured values where possible and record uncertainty using `references/07-measurement-pass.md`.

## What to ignore

Usually ignore:
- random AI-generated logos
- illegible tiny labels
- fake charts with no data meaning
- background noise
- accidental gradients
- impossible overlaps
- visual details that would be expensive and low-value

## Code-first rule

Default to code.

Build with code:
- layout
- typography
- text
- buttons
- inputs
- forms
- cards
- lists
- tabs
- navigation
- simple icons
- ordinary charts
- gradients that CSS can express cleanly
- shadows and radius

Use assets only when code would look stiff, fake, or too expensive.

## Productization rule

If the mockup conflicts with product logic, usability, or existing implementation constraints, preserve the design intent rather than copying the image.

## Output format

```md
# Design Translation Summary

## Source of truth
[what matters most: product task / IA / visual style / fidelity]

## User task
[primary action]

## Information structure
- [section 1]
- [section 2]
- [section 3]

## Visual direction
- mood:
- density:
- typography:
- color:
- radius/shadow:
- material:

## Fidelity decision
- target:
- reason:

## Preserve
- ...

## Adapt
- ...

## Ignore
- ...

## Implementation priorities
P0:
P1:
P2:
P3:
```

## Brief rule

Include this summary in the initial Implementation Brief.
Do not proceed to implementation until the user has had a chance to confirm or correct the translation.
