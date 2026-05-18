# arcana-design-to-code

A lightweight design-to-code skill for turning product ideas, AI mockups, screenshots, or design references into implementation-ready briefs, with optional UI implementation after confirmation.

This skill does not try to fully automate design generation. It focuses on:

- understanding the product goal
- identifying the role of reference images
- producing a visible visual reading summary before implementation
- producing a visible design translation summary before implementation
- extracting measured/estimated design tokens when numeric fidelity matters
- producing an Asset Manifest for image-based requests
- translating design intent into implementation instructions
- deciding what should be code vs image asset
- asking for image assets only when needed
- generating or editing approved image assets with imagegen when fidelity depends on them
- implementing UI after the brief is approved
- performing a light visual exit check before finishing

## What this skill is for

Use this skill when you want to:

- turn an AI-generated mockup into a real app page
- reconstruct a screenshot into product UI without pixel-chasing
- convert design references into a coding-agent handoff
- generate a brief before implementing UI from a reference image
- implement the approved brief in a codebase
- decide which visual elements should become code and which should become assets
- ask the user/GPT/Codex imagegen for missing image assets
- clean up generated assets for implementation

## What this skill is not for

This is not a full visual QA system.

It does not:

- run pixel-level diff against AI mockups
- treat AI mockups as Figma-level design specs
- invent exact numbers from low-resolution or compressed images
- generate images by default
- block implementation on decorative details
- replace a separate UI QA / regression workflow

## Portable use

This bundle can be used in Codex or in generic agents such as WorkBuddy, Cursor, Claude, or other tools with custom project rules.

For native Codex skill use, install the folder as:

```text
~/.codex/skills/arcana-design-to-code/
```

For generic agents:

1. Add `SKILL.md` as the main project rule or custom instruction.
2. Add `references/` as knowledge files.
3. Add `scripts/` as optional local utilities if the agent can run scripts.
4. Tell the agent to follow the Step Ledger and stop for confirmation before code edits.

Portable entry prompt:

```text
Use the arcana-design-to-code workflow strictly.
Follow the Step Ledger in order and do not merge or skip gates.
Read SKILL.md first, then load only the referenced files for the current gate.
Produce an Implementation Brief before code edits.
For numeric fidelity, run Measurement Pass.
For constrained-height screens, run Viewport Budget Pass.
For non-UI visuals or style-carrying artwork, run Generate Candidate Scan before Asset Manifest.
For style-carrying assets, ask Source / Generate / Fallback before implementation.
Never silently choose Fallback for assets that affect fidelity, mood, empty-state quality, card feel, brand-like motifs, or other visible style carriers.
Screenshot crops are not Source assets for embedded mascots, hero objects, illustrations, or irregular silhouettes; classify them as Generate/Image-to-image unless an independent source file exists.
If image generation is unavailable or not approved, ask the user instead of choosing Fallback.
Do not implement until I confirm the brief.
```

If the agent cannot run scripts, it should still complete the matching pass manually and mark values as `estimated`, `inferred`, or `unknown`.

## Core workflow

1. Intake
   Understand the page, product goal, platform, viewport, and existing project constraints.

2. Reference Intent
   Identify whether each reference image is for IA, visual style, general direction, or high-fidelity reconstruction.

3. Visual Reading
   Extract viewport, layout blocks, user flow, component inventory, visual tokens, style carriers, asset decisions, and hidden states.

4. Measurement Pass
   When the user asks for concrete values such as radius, margins, padding, or font sizes, calibrate the image to the source reference viewport, then adapt measured tokens to the implementation target range.

5. Viewport Budget
   For constrained-height, full-screen mobile, player-like, tool-like, or no-scroll screens, sum the planned CSS height of shell padding, fixed sections, controls, gaps, and bottom tools before implementation.

6. Generate Candidate Scan
   For non-UI visuals, artwork, avatars, thumbnails, cover art, empty-state illustrations, hero objects, or brand-like motifs, classify candidates as Source / Generate / Image-to-image / Code / Ignore.

7. Asset Workflow
   Decide what should be code, source asset, generated asset, fallback, or ignored.
   Produce an Asset Manifest for image-based requests, even when no formal assets are required.
   If the user approves Generate assets, create isolated reusable assets with imagegen/image-to-image instead of recreating the whole screen.

8. Design Translation
   Convert the reference into explicit source-of-truth, preserve/adapt/ignore, fidelity, and implementation-priority decisions using the visual reading, measurements, viewport budget, and asset manifest.

9. Implementation Brief and Confirmation
   Always produce an Implementation Brief first, including concise Visual Reading and Design Translation summaries and an Asset Manifest for image-based requests.
   If the Asset Manifest has unresolved visible style-carrying assets, ask for Source / Generate / Fallback before asking for implementation approval.
   If the user approves the brief, inspect the codebase and implement.
   If the user asks for a handoff only, stop after the brief.

10. Exit Check
   Confirm the implementation is usable, coherent, visually aligned with the selected reference intent, and ready for deeper QA if needed.

The workflow is sequential. Agents should show a Step Ledger, complete one gate at a time, and stop for confirmation before code edits.

## Optional script

`scripts/prepare_image_asset.py` can be used to trim padding, convert white backgrounds to alpha, or chroma-key green-screen assets.

Use it only after an image asset has already been approved.
Do not use asset cleanup as a reason to delay the core product flow.

The script requires Pillow:

```bash
python3 -m pip install Pillow
```

`scripts/measure_ui_image.py` can be used during the Measurement Pass to convert explicit screenshot coordinates into CSS-pixel measurements and token candidates.

Example:

```bash
python3 scripts/measure_ui_image.py screenshot.png \
  --source-viewport 390x844 \
  --target-viewport compact:360x800 \
  --target-viewport large-phone:430x932 \
  --rect card:16,132,358,180 \
  --distance card-gap:16,312,16,328 \
  --text title:24,54,220,34 \
  --radius-probe card:16,132,358,180
```

Use the output as measurement evidence, then normalize it into responsive rules in the Implementation Brief.

`scripts/viewport_budget.py` can be used before implementation to check that a constrained-height screen fits its target viewport.

Example:

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

## License

MIT

## Example prompts

Brief first, then optional implementation:

```text
根据这张 GPT image2 生成的移动端 UI 图，先生成 implementation brief。主视口 390x844，允许产品化调整，不要把整张图当背景。等我确认后再实现。
```

Implementation brief only:

```text
只生成 implementation brief，不要改代码。这张图同时参考信息架构和视觉风格，目标桌面端 1440x900。
```

Asset decision pass:

```text
先帮我判断这张 UI 图里哪些应该用代码实现，哪些需要现有素材或 imagegen，哪些可以忽略。
```

High-fidelity target:

```text
这是一张已批准的 UI 截图，请按 Fidelity Target 处理，目标视口 375x812，尽量贴近主要布局、内容和视觉比例。
```

Numeric token extraction:

```text
这张图我要高保真还原。参考图适配 iPhone 15 / 390x844，请先读出具体数值：页面边距、卡片间距、圆角、按钮高度、字号和行高。实现需要适配 360x800 到 430x932，无法确定的值请标注 estimated/unknown。
```
