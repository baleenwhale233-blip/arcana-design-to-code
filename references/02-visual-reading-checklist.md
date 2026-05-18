# Visual Reading Checklist

## Goal

Turn a UI image into implementation intent before writing code.

Do not describe the image like an art critique.
Extract structure, components, states, tokens, style carriers, and asset decisions.

The initial Implementation Brief must include a concise Visual Reading Summary.
Do not hide visual reading as private notes when the user is asking for design-to-code work.

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

If the user asks for accurate values, exact tokens, "具体数值", "圆角", "边距", "字号", "像素级", "高保真", or the reference is a Fidelity Target, run the Measurement Pass in `references/07-measurement-pass.md`.
Do not hide measurement uncertainty. Mark values as measured, estimated, inferred, or unknown.

### 7. Style carriers

Identify the few details that carry the design's recognizable flavor.

These are the visual details that should be preserved more carefully than generic decoration.

Common style carriers:

- typography: language-specific weight, size hierarchy, line height, title/body contrast
- whitespace: iOS-like breathing room, compact enterprise density, dense content rhythm
- interaction color: selected state, focus ring, pressed state, active tab
- primary action color: CTA fill, contrast, disabled state
- surface treatment: white card, border strength, divider style, shadow, translucency
- brand/source marks: official logos, platform icons, source badges
- placeholders: cover art, avatar, empty-state illustration, generated artwork
- navigation shape: app bar height, bottom tab style, floating action position

For each style carrier, record:

- what to preserve
- whether it should be code, source asset, generated asset, or fallback
- what may be simplified without losing the design direction

Do not let information architecture crowd out the style carriers.

### 8. Code vs asset decision

For each distinct visual element, decide:

- Code: layout, typography, controls, cards, simple icons, ordinary charts, CSS gradients
- Source: official logos, brand marks, existing product images
- Generate: central illustration, mascot, hero object, complex artwork
- Ignore: noise, accidental highlights, fake tiny logos, impossible AI details

Do not use the full mockup as a page background.
Do not crop normal UI controls from the image.

If the reference includes non-UI visuals, artwork, avatars, thumbnails, cover art, empty-state illustrations, hero objects, or brand-like motifs, run `references/09-generate-candidate-scan.md` before finalizing asset decisions.

### 9. Product gaps and hidden states

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

## Design Measurements
- include when numeric fidelity is requested or required:
- measured values:
- estimated values:
- inferred values:
- unknowns:

## Style Carriers
| carrier | preserve | implementation decision | notes |
|---|---|---|---|

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
Include a concise Visual Reading Summary in the initial brief.
Do not include the full notes after implementation unless the user asked for the design analysis.
