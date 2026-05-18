---
name: arcana-design-to-code
description: >-
  Lightweight design-to-code workflow. Turn product ideas, AI mockups,
  screenshots, or design references into an implementation-ready brief first,
  then optionally implement UI after user confirmation. Use when the user says
  "设计还原", "截图还原", "image2 to code", "mockup to code", "设计转代码",
  "根据这张图实现页面", "把这个 UI 做出来", "生成实现 brief", "素材怎么处理", or when
  another workflow needs design-to-code handoff.
---

# Design-to-Code Skill

This skill turns a design direction, mockup, screenshot, or product idea into an implementation-ready brief first, then optionally into production UI code after user confirmation.

The goal is not pixel-perfect reconstruction. The goal is to preserve design intent while producing usable, maintainable product UI.

## Default stance

AI mockups are directional references, not pixel-perfect specifications.

Default to:
- product intent over image copying
- code over bitmap assets
- implementation clarity over visual overfitting
- brief before code edits
- visible visual calibration before implementation
- visible design translation before implementation
- visible asset scan and manifest before implementation
- light exit checks over heavy QA

## Portable agent guidance

This folder can be used outside Codex by any agent that supports custom instructions, project rules, knowledge files, or tool/script execution.

If the host agent does not have native Skill support:

- Treat this `SKILL.md` as the primary project instruction.
- Keep `references/` available as linked knowledge files and load only the referenced file for the active gate.
- Keep `scripts/` available as optional local utilities. If scripts cannot be run, perform the same pass manually and mark values as estimated/inferred.
- Follow the Step Ledger exactly and show it in the response.
- Stop at Confirmation before editing code, unless the user has already approved the specific Implementation Brief in the same conversation.
- When tool names differ, use the host agent's equivalent for reading files, editing code, running scripts, previewing the app, and capturing screenshots.

Portable entry prompt for generic agents:

```text
Use the arcana-design-to-code workflow strictly.
Follow the Step Ledger in order and do not merge or skip gates.
Read SKILL.md first, then load only the referenced files for the current gate.
Produce an Implementation Brief before code edits.
For numeric fidelity, run Measurement Pass.
For constrained-height screens, run Viewport Budget Pass.
For style-carrying assets, ask Source / Generate / Fallback before implementation.
Never silently choose Fallback for assets that affect fidelity, mood, empty-state quality, card feel, brand-like motifs, or other visible style carriers.
Screenshot crops are not Source assets for embedded mascots, hero objects, illustrations, or irregular silhouettes; classify them as Generate/Image-to-image unless an independent source file exists.
If image generation is unavailable or not approved, ask the user instead of choosing Fallback.
Do not implement until I confirm the brief.
```

## Asset decision gate

Fallback is an option to present, not a default choice, when a missing asset affects fidelity.
Cropping an object out of a supplied screenshot is not a Source decision unless the screenshot is already the intended source media. Treat embedded mascots, hero objects, illustrations, stickers, soft/3D objects, and irregular silhouettes as Generate or Image-to-image candidates when they carry style.

If the user explicitly asks to identify assets that need image-to-image generation, that instruction overrides the conservative "do not generate by default" stance. The agent still must ask before generating, but it must not silently downgrade those assets to crop, clip-path, or CSS fallback.

Before implementation, inspect the Asset Manifest for unresolved style-carrying assets:

- empty-state illustrations
- cover art, album art, product thumbnails, avatars, or placeholders
- mascot, hero object, decorative object, or brand-like motif
- visual motif that makes the reference feel finished
- background artwork that materially affects mood

For each unresolved style-carrying asset, stop and ask:

```md
## Asset Decision Needed

| id | role | why it matters | options | recommended |
|---|---|---|---|---|
| [asset-id] | [placement] | [fidelity impact] | Source / Generate / Fallback | [choice + reason] |
```

Do not proceed to implementation until the user chooses Source, Generate, or Fallback for these assets.
If the host agent cannot generate images, still ask the user to choose Source or Fallback; do not silently pick Fallback.

## Generate candidate scan

When a reference image includes any non-UI visual element, run a Generate Candidate Scan before finalizing the Asset Manifest.
If the host agent does not load references automatically, use this section directly.

Scan every major region for:

- illustration, mascot, hero object, 3D/glass/soft object
- cover art, album art, product image, avatar, thumbnail, poster
- empty-state visual, onboarding visual, badge artwork
- brand-like motif, background artwork, visual texture that defines mood
- complex decorative object that CSS/SVG would make stiff or fake

Classify each candidate:

- Source: official, brand, vendor, or existing product asset
- Generate: needs a new isolated asset
- Image-to-image: generate using the reference image style/crop as guidance
- Code: can be cleanly built with CSS/SVG/icon library
- Ignore: low-value decoration or accidental AI noise

Do not classify embedded screenshot objects as Source unless an independent source asset exists.

Required output:

```md
## Generate Candidate Scan

| candidate | region | role | style impact | decision | generation mode | why not code | fallback |
|---|---|---|---|---|---|---|---|
| [name] | [where] | [what it does] | high/medium/low | Source/Generate/Image-to-image/Code/Ignore | none/text-to-image/image-to-image | [reason] | [fallback] |
```

If no candidates are found, say `No Generate candidates found` and explain why the visible design can be implemented as code/source assets.

## Main workflow

Load references only when needed:

1. For vague requests or missing product context, read `references/01-intake-and-reference-intent.md`.
2. For any supplied mockup, screenshot, or visual reference, read `references/02-visual-reading-checklist.md` and produce Visual Reading Notes.
3. If the user asks for accurate values, exact tokens, "具体数值", "圆角", "边距", "字号", "像素级", "高保真", or the reference is a Fidelity Target, read `references/07-measurement-pass.md` and produce Design Measurements.
4. If the UI is constrained by viewport height, full-screen mobile, player-like, dashboard-like, or intended not to scroll, read `references/08-viewport-budget-pass.md` and produce a Viewport Budget.
5. For any supplied mockup, screenshot, or visual reference, read `references/09-generate-candidate-scan.md` when non-UI visuals may exist, then read `references/04-asset-workflow.md` and produce an Asset Manifest. If there are no fidelity-relevant assets, say so explicitly.
6. Read `references/03-design-translation.md` and produce a Design Translation Summary using the visual reading, measurements, viewport budget, and asset manifest.
7. For every design-to-code request, read `references/05-implementation-handoff.md` and produce an Implementation Brief with visible Visual Reading, Design Translation, and Asset Manifest sections before editing code.
8. Ask for any required Source / Generate / Fallback asset decisions first; after those are settled, ask whether to proceed with implementation.
9. Only after the user confirms implementation, use Implementation Mode.
10. After implementation, use `references/06-exit-check.md` before finishing.

## Sequential gate protocol

Follow the workflow as ordered gates, not as a loose checklist.

At the start of any design-to-code response, create a visible Step Ledger:

```md
## Step Ledger
1. Reference intent - pending/in progress/done
2. Visual reading - pending/in progress/done
3. Measurement pass - skipped/done, with reason
4. Viewport budget - skipped/done, with reason
5. Asset manifest - pending/in progress/done
6. Design translation - pending/in progress/done
7. Implementation brief - pending/in progress/done
8. Confirmation - pending
9. Implementation - blocked until confirmation
10. Exit check - blocked until implementation
```

Gate rules:

- Complete gates in order.
- Do not combine gates into one hidden reasoning pass.
- Do not advance to the next gate until the current gate has a visible output section.
- If a gate is skipped, mark it `skipped` and give the reason.
- If required input is missing, either record a clear assumption or ask one blocking question, then stop at that gate.
- If you notice you skipped a gate, say so briefly, return to the missing gate, and continue from there.
- If the Asset Manifest has unresolved visible style-carrying assets, gate 8 asks for Source / Generate / Fallback first. After the user chooses, update the manifest or brief if needed, then ask for implementation confirmation.
- Do not edit code until gates 1-8 are done and the user explicitly confirms implementation.
- During implementation, follow the approved brief; do not re-run earlier gates silently unless new information changes the brief.

Required visible outputs by gate:

1. Reference intent: role, fidelity, source of truth, binding vs non-binding.
2. Visual reading: viewport, layout blocks, user flow, component inventory, visual tokens, style carriers.
3. Measurement pass: required only for numeric fidelity; source viewport, measured/estimated/inferred values, adaptation targets.
4. Viewport budget: required for constrained-height or no-scroll UIs; available height, section heights, gap/padding totals, remaining/overflow, compression plan.
5. Asset manifest: Generate Candidate Scan, then code/source/generate/fallback/ignore decisions, even if no formal assets are needed.
6. Design translation: source of truth, preserve/adapt/ignore, fidelity decision, implementation priorities.
7. Implementation brief: the full handoff from `references/05-implementation-handoff.md`.
8. Confirmation: ask for blocking asset decisions first, then ask whether to implement; stop.
9. Implementation: code changes only after confirmation.
10. Exit check: use `references/06-exit-check.md`.

## Hard rules

Never:
- use a full mockup screenshot as a page background
- run pixel-level diff against AI mockups as the source of truth
- treat generated decorative details as required product specs
- block the core product flow on image assets
- generate images without user approval unless the runtime explicitly allows it and the user asked for it
- introduce heavy dependencies just to match a mockup
- edit code before producing an Implementation Brief
- hide visual reading as private notes when the user is calibrating or testing the design-to-code workflow
- hide design translation as private reasoning when the user is doing design-to-code work
- skip Asset Workflow because the agent plans to use code or CSS fallback
- replace asset decisions with unreviewed CSS fallbacks
- fake a style-carrying irregular asset with a rectangular screenshot crop, clip-path mask, or border-radius mask
- treat "code-first" as permission to skip an Asset Manifest
- treat screenshot height as usable CSS content height without subtracting shell/header/safe/control budgets
- rely on scrolling to fix overflow in full-screen mobile, player-like, or tool-like screens unless the brief says the page is a content flow
- treat phrases like "build", "implement", "recreate", "restore", "还原", or "做出来" as approval to skip the brief
- continue from brief to implementation until the user explicitly confirms
- skip, merge, or hide required workflow gates when the user is testing or relying on this skill

Always:
- identify platform and primary viewport
- identify the role of each reference image
- translate visual observations into components, states, tokens, and asset decisions
- preserve the primary user task
- preserve information hierarchy
- prefer existing project components and tokens
- separate code decisions from asset decisions
- record assumptions in design metadata
- provide fallback options for missing decorative assets without silently choosing fallback for visible style carriers
- include a concise Visual Reading Summary in the initial brief
- include a concise Design Translation Summary in the initial brief
- include Design Measurements when numeric fidelity is requested or the image is a Fidelity Target
- ask for or infer the reference source viewport before treating measured values as CSS pixels
- adapt measured values into responsive implementation tokens instead of locking layout to the reference bitmap size
- include a Viewport Budget for constrained-height UI before implementation
- identify the style carriers that make the reference feel like itself
- run a Generate Candidate Scan when the reference includes non-UI visuals or style-carrying artwork
- classify embedded mascots, hero objects, illustrations, stickers, soft/3D objects, and irregular silhouettes as Generate/Image-to-image candidates unless a true source asset exists
- include an Asset Manifest in the initial brief for every image-based design-to-code request
- ask for Source / Generate / Fallback when a missing asset is a visible style carrier
- produce an Implementation Brief before implementation
- ask for confirmation before editing code
- show the Step Ledger for image-based design-to-code requests and update it as gates complete

## Modes

### 1. Intake Mode

Use when the user provides a vague request.

Ask only blocking questions. Do not turn intake into a long questionnaire.

### 2. Translation Mode

Use when the user provides a mockup, screenshot, or design direction.

Read `references/02-visual-reading-checklist.md` first when an image is available.
If numeric fidelity is requested, read `references/07-measurement-pass.md` before producing the brief.

Output:
- concise Visual Reading Summary
- concise Design Translation Summary
- Design Measurements when requested or required by fidelity
- source of truth
- what to preserve
- what may change
- what to ignore
- implementation priorities

### 3. Implementation Mode

Use only after an Implementation Brief has been produced and the user explicitly confirms they want to proceed with code changes.

Do not enter Implementation Mode directly from the initial visual request.
Phrases like "build", "implement", "recreate", "restore", "还原", or "做出来" mean "produce the brief now and wait for confirmation", not "edit code immediately".

Process:
- follow the approved Implementation Brief
- preserve the approved Visual Reading Summary, Design Translation Summary, style carriers, and asset decisions
- follow the approved Asset Manifest; treat CSS fallbacks as temporary when the manifest marks an asset as Source or Generate
- implement protruding mascots, stickers, hero objects, and irregular assets as separate layered elements; keep the visual parent `overflow: visible` and put scroll clipping on the inner scroll region
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

Use for every image-based design-to-code request.

If the reference contains no fidelity-relevant assets, output an Asset Manifest that says no formal assets are required and normal UI should be code.

Output:
- asset manifest
- image requests if needed
- generated asset workflow when user approves generation
- code fallbacks
- optional asset cleanup command

### 5. Handoff Mode

Use for every initial design-to-code request, including requests that say to build, implement, recreate, restore, or "make" the UI.

If the user asks only for a brief, spec, plan, or handoff for another coding agent, stop after the brief.
If the user appears to want implementation, still stop after the brief and ask whether to proceed.

Output a concise implementation brief:
- page goal
- platform and viewport
- reference intent
- visual reading summary
- design translation summary
- style carriers
- asset manifest
- component structure
- code-vs-asset decisions
- assumptions
- exit check
- confirmation prompt

### 6. Exit Check Mode

Use after implementation.

Check whether the page is usable, coherent, and visually aligned with the selected reference intent.
Do not perform full QA unless the user explicitly asks.

## Image generation permission

The agent must not generate images by default.

When an image asset is needed, choose one:

1. Ask
   If the asset affects fidelity or is a visible style carrier, ask the user to choose Source, Generate, or Fallback.

2. Generate with approval
   Use Codex/imagegen only if the user explicitly allows it.

3. Fallback
   Implement a code-based placeholder only if the asset is low-value decoration or the user chooses Fallback.

If the approved Asset Manifest marks an item as Generate and the user approves Codex/imagegen, generate or edit the asset before implementation when it materially affects fidelity.
Use the reference image plus the asset row to create a targeted imagegen request.
After generation, verify transparency/background, crop/padding, target size, and visual fit before integrating it.

## Optional asset cleanup

If a generated image has white background, green background, fake transparency, or excess padding, use `scripts/prepare_image_asset.py`.

This script is only for deterministic cleanup. It does not make design decisions.
