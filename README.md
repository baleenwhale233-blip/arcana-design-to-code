# arcana-design-to-code

A lightweight design-to-code skill for turning product ideas, AI mockups, screenshots, or design references into implementation-ready briefs, with optional UI implementation after confirmation.

This skill does not try to fully automate design generation. It focuses on:

- understanding the product goal
- identifying the role of reference images
- producing a visible visual reading summary before implementation
- producing a visible design translation summary before implementation
- translating design intent into implementation instructions
- deciding what should be code vs image asset
- asking for image assets only when needed
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
- generate images by default
- block implementation on decorative details
- replace a separate UI QA / regression workflow

## Core workflow

1. Intake
   Understand the page, product goal, platform, viewport, and existing project constraints.

2. Reference Intent
   Identify whether each reference image is for IA, visual style, general direction, or high-fidelity reconstruction.

3. Visual Reading
   Extract viewport, layout blocks, user flow, component inventory, visual tokens, style carriers, asset decisions, and hidden states.

4. Design Translation
   Convert the reference into explicit source-of-truth, preserve/adapt/ignore, fidelity, and implementation-priority decisions.

5. Asset Workflow
   Decide what should be code, source asset, generated asset, or ignored.

6. Implementation or Handoff
   Always produce an Implementation Brief first, including concise Visual Reading and Design Translation summaries.
   If the user approves the brief, inspect the codebase and implement.
   If the user asks for a handoff only, stop after the brief.

7. Exit Check
   Confirm the implementation is usable, coherent, visually aligned with the selected reference intent, and ready for deeper QA if needed.

## Optional script

`scripts/prepare_image_asset.py` can be used to trim padding, convert white backgrounds to alpha, or chroma-key green-screen assets.

Use it only after an image asset has already been approved.
Do not use asset cleanup as a reason to delay the core product flow.

The script requires Pillow:

```bash
python3 -m pip install Pillow
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
