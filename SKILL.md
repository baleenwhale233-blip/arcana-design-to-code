---
name: arcana-design-to-code
description: >-
  Lightweight design-to-code workflow. Turn product ideas, AI mockups,
  screenshots, or design references into implementation-ready UI. Use when the
  user says "设计还原", "截图还原", "image2 to code", "mockup to code", "设计转代码",
  "根据这张图实现页面", "把这个 UI 做出来", "生成实现 brief", "素材怎么处理", or when
  another workflow needs design-to-code handoff.
---

# Design-to-Code Skill

This skill turns a design direction, mockup, screenshot, or product idea into practical implementation guidance or production UI code.

The goal is not pixel-perfect reconstruction. The goal is to preserve design intent while producing usable, maintainable product UI.

## Default stance

AI mockups are directional references, not pixel-perfect specifications.

Default to:
- product intent over image copying
- code over bitmap assets
- implementation clarity over visual overfitting
- light exit checks over heavy QA

## Main workflow

Load references only when needed:

1. For vague requests or missing product context, read `references/01-intake-and-reference-intent.md`.
2. For any supplied mockup, screenshot, or visual reference, read `references/02-visual-reading-checklist.md` and `references/03-design-translation.md`.
3. When the visual design contains complex illustrations, logos, 3D/glass objects, textures, or backgrounds, read `references/04-asset-workflow.md`.
4. When producing a brief for another coding agent, read `references/05-implementation-handoff.md`.
5. When implementing UI in a codebase, use Implementation Mode and then use `references/06-exit-check.md` before finishing.

## Hard rules

Never:
- use a full mockup screenshot as a page background
- run pixel-level diff against AI mockups as the source of truth
- treat generated decorative details as required product specs
- block the core product flow on image assets
- generate images without user approval unless the runtime explicitly allows it and the user asked for it
- introduce heavy dependencies just to match a mockup
- stop at a brief when the user asked to build, implement, recreate, or restore the UI

Always:
- identify platform and primary viewport
- identify the role of each reference image
- translate visual observations into components, states, tokens, and asset decisions
- preserve the primary user task
- preserve information hierarchy
- prefer existing project components and tokens
- separate code decisions from asset decisions
- record assumptions in design metadata
- provide fallbacks for missing decorative assets

## Modes

### 1. Intake Mode

Use when the user provides a vague request.

Ask only blocking questions. Do not turn intake into a long questionnaire.

### 2. Translation Mode

Use when the user provides a mockup, screenshot, or design direction.

Read `references/02-visual-reading-checklist.md` first when an image is available.

Output:
- source of truth
- what to preserve
- what may change
- what to ignore
- implementation priorities

### 3. Implementation Mode

Use when the user asks to build, implement, recreate, restore, or "make" the UI from a reference image or design direction.

Do not stop at an implementation brief.

Process:
- inspect the existing codebase before choosing components or routes
- identify reusable components, styles, tokens, data models, and routing conventions
- translate the visual reference into component structure and implementation tasks
- implement the UI in the codebase using existing project conventions
- keep ordinary UI as code, not image assets
- add only focused dependencies when the project already supports that pattern or the user explicitly approves
- run the relevant local checks or dev server when available
- perform the exit check in `references/06-exit-check.md`

Output:
- changed files
- assumptions made
- verification performed
- any follow-up asset requests or product questions

### 4. Asset Mode

Use when the visual design contains complex illustrations, logos, 3D/glass objects, textures, or backgrounds.

Output:
- asset manifest
- image requests if needed
- code fallbacks
- optional asset cleanup command

### 5. Handoff Mode

Use only when the user explicitly asks for a brief, spec, plan, or handoff for another coding agent, or says not to change code.

Do not use Handoff Mode when the user asks to build, implement, recreate, restore, or "make" the UI now. Use Implementation Mode instead.

Output a concise implementation brief:
- page goal
- platform and viewport
- reference intent
- component structure
- code-vs-asset decisions
- assumptions
- exit check

### 6. Exit Check Mode

Use after implementation.

Check whether the page is usable, coherent, and visually aligned with the selected reference intent.
Do not perform full QA unless the user explicitly asks.

## Image generation permission

The agent must not generate images by default.

When an image asset is needed, choose one:

1. Ask
   Write an Image Request for the user/GPT to generate.

2. Generate with approval
   Use Codex/imagegen only if the user explicitly allows it.

3. Fallback
   Implement a code-based placeholder if the asset is not required for MVP.

## Optional asset cleanup

If a generated image has white background, green background, fake transparency, or excess padding, use `scripts/prepare_image_asset.py`.

This script is only for deterministic cleanup. It does not make design decisions.
