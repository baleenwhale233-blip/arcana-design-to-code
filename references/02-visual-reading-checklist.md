# Visual Reading Checklist

## Goal

Turn a UI image into implementation intent before writing code.

Do not describe the image like an art critique.
Extract structure, components, states, tokens, and asset decisions.

## When to use

Use this when the user provides:

- GPT image2 output
- AI-generated UI mockup
- screenshot
- product reference image
- design direction image

## Reading order

Analyze the image in this order.

### 1. Reference role

Classify the image using `references/01-intake-and-reference-intent.md`.

Record:

- role: Direction Reference / IA Reference / Visual Style Reference / Fidelity Target
- fidelity level: Low / Medium / High
- source: AI-generated / screenshot / Figma / existing app / unknown
- what is binding vs non-binding

Default AI-generated UI to Direction Reference + Visual Style Reference unless the user explicitly asks for high fidelity.

### 2. Viewport and surface

Infer the target surface:

- platform: mobile app / mobile web / desktop web / mini program / responsive web
- primary viewport: width x height if known or inferred
- safe areas, browser chrome, app bars, tab bars, or mini-program constraints
- density: compact / standard / spacious

If viewport is unknown but not blocking, assume one and record it.

### 3. Layout blocks

Break the page into large blocks before styling.

Common blocks:

- app shell
- top navigation
- sidebar
- hero or summary area
- toolbar or filters
- content list
- cards
- form
- chart or data panel
- bottom navigation
- floating action
- modal or drawer
- footer

For each block, record:

- purpose
- content
- actions
- states
- approximate order and hierarchy

### 4. User flow

Identify what the user is meant to do.

Record:

- primary task
- primary action
- secondary actions
- required inputs or selections
- navigation path
- expected success outcome

If the image contains decorative CTAs or illegible generated labels, infer the product task from context instead of copying fake text.

### 5. Component inventory

Map visual elements to code components.

Prefer existing project components when available.

Use this table:

```md
| component | role | reuse/new | required states | notes |
|---|---|---|---|---|
| Header | navigation | reuse | default, active route | keep existing app shell if present |
| SearchInput | query entry | reuse/new | default, focused, empty | do not crop from image |
```

### 6. Visual tokens

Convert visual style into implementable tokens.

Record:

- typography: scale, weight, hierarchy, line height
- spacing: page padding, section gap, card gap, control gap
- color: background, surface, text, muted text, border, accent, danger/success
- shape: radius sizes, pill vs card vs square
- elevation: shadow strength, border usage, layer depth
- density: compact / standard / spacious
- motion: only if implied by interaction, not decorative speculation

Avoid vague instructions like "make it premium" unless translated into concrete tokens.

### 7. Code vs asset decision

For each distinct visual element, decide:

- Code: layout, typography, controls, cards, simple icons, ordinary charts, CSS gradients
- Source: official logos, brand marks, existing product images
- Generate: central illustration, mascot, hero object, complex artwork
- Ignore: noise, accidental highlights, fake tiny logos, impossible AI details

Do not use the full mockup as a page background.
Do not crop normal UI controls from the image.

### 8. Product gaps and hidden states

List details not visible in the image but required for implementation:

- real copy
- real data fields
- loading state
- empty state
- error state
- success state
- disabled state
- long text behavior
- responsive behavior
- accessibility concerns

## Output template

```md
# Visual Reading Notes

## Reference
- image:
- role:
- fidelity:
- binding:
- non-binding:

## Viewport
- platform:
- primary viewport:
- responsive assumptions:
- density:

## Layout Blocks
- block:
  - purpose:
  - content:
  - actions:
  - states:

## User Flow
1. ...

## Component Inventory
| component | role | reuse/new | required states | notes |
|---|---|---|---|---|

## Visual Tokens
- typography:
- spacing:
- color:
- radius:
- shadow:
- density:

## Code vs Asset
| element | decision | reason |
|---|---|---|

## Product Gaps
- states:
- data:
- interactions:
- responsive:
- accessibility:

## Implementation Guidance
- preserve:
- adapt:
- ignore:
```

## Implementation rule

When implementing after brief approval, use these notes as the bridge between the image and code.
Do not include the full notes in the final answer unless the user asked for the design analysis.
