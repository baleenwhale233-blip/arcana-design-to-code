# Intake and Reference Intent

## Goal

Before implementation, understand what the user is trying to build and what each reference image means.

Do not assume a screenshot is a design spec.
Do not assume an AI mockup should be copied literally.

## Blocking intake questions

Ask only what is missing and blocking.

Required if unknown:

1. Platform
   Is this for mobile app, mobile web, desktop web, mini program, or responsive web?

2. Primary viewport
   What viewport should be treated as primary?
   Examples: iPhone 390×844, desktop 1440×900, mini program 375×812.

3. Page goal
   What is the main user task on this page?

4. Reference intent
   What role does the image play?

5. Existing constraints
   Should the implementation reuse existing components, routes, data models, and design tokens?

If the user has already answered these, do not ask again.

If missing information does not block implementation, make a reasonable assumption and record it in Design Metadata.

## Reference intent types

Each reference image must be assigned one or more roles.

### 1. Direction Reference

The image expresses mood, visual direction, or design taste.

Use it for:
- overall feeling
- density
- mood
- broad layout rhythm
- component character

Do not:
- copy pixels
- preserve every decorative detail
- treat generated text/icons as product requirements

Default for AI-generated mockups.

### 2. IA Reference

The image expresses information architecture.

Preserve:
- modules
- hierarchy
- user path
- form order
- navigation structure
- primary and secondary actions

May change:
- color
- card style
- icon style
- spacing details
- decorative visuals

### 3. Visual Style Reference

The image expresses visual style.

Preserve:
- color mood
- material quality
- typography feel
- spacing rhythm
- radius/shadow language
- visual density

May change:
- exact layout
- generated content
- component placement
- decorative details

### 4. Fidelity Target

The image is a confirmed design target and should be recreated as closely as practical.

Use only when:
- the image comes from Figma, design spec, or approved UI
- the target viewport is known
- content is known
- the user explicitly requests high-fidelity reconstruction

Do not default AI-generated mockups to Fidelity Target.

## Default rule

If unclear, treat AI-generated mockups as:

Direction Reference + Visual Style Reference

not Fidelity Target.

## Quick user-facing question

When needed, ask:

"这张图你希望我主要参考哪一层？
A. 信息架构 / 流程
B. 视觉风格
C. 两者都参考，但允许产品化调整
D. 尽量高保真还原"

Default to C.

## Design Metadata template

Use this format in handoff output.

```md
# Design Metadata

## Page
[page name]

## Product
[product name / product purpose]

## Platform
[mobile web / desktop web / mini program / app / responsive]

## Primary Viewport
[width × height]

## Reference Images
- `[file name]`
  - intent: Direction Reference / IA Reference / Visual Style Reference / Fidelity Target
  - source: user-provided / AI-generated / existing app / Figma / unknown
  - notes: [what matters in this image]

## Fidelity Level
Low / Medium / High

## Preserve
- [what must stay]

## May Change
- [what can be adapted]

## Ignore
- [what should not be implemented]

## Assumptions
- [assumptions made because user did not specify]
```
