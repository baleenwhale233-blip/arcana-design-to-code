# Asset Workflow

## Goal

Decide which visual elements should be code, existing source assets, generated assets, or ignored.

Do not over-extract assets.
Most UI should be rebuilt with code.

Code-first does not mean asset-blind.
If visible assets carry the design's fidelity or brand feel, produce an Asset Manifest before implementation.

## Asset decisions

For each visually distinct element, choose one:

### 1. Ignore

Use when the element is decorative and not worth implementing.

Examples:
- subtle noise
- random background specks
- accidental highlights
- generated ornamental details
- fake tiny logos

### 2. Code

Use when the element can be implemented with HTML/CSS/SVG/icon library.

Examples:
- buttons
- cards
- forms
- simple icons
- tabs
- ordinary gradients
- badges
- charts
- layout frames

### 3. Source

Use when the element should come from an existing official/project asset.

Examples:
- app logo
- brand mark
- vendor logo
- existing icon asset
- product screenshot

Do not redraw official logos with AI unless explicitly requested.

### 4. Generate

Use when the element is visually central and hard to code.

Examples:
- empty-state illustration
- mascot
- hero object
- 3D/glass/soft object
- complex decorative artwork
- brand-like visual motif
- cover art placeholder that defines the card feel

## Default

Start with zero custom image assets.

Only create an image asset when:
- it is visually central
- CSS/SVG would look stiff or fake
- the element is reusable
- the element materially affects the selected design direction
- it is worth the implementation cost

Even when creating zero new assets, still list visible asset decisions in an Asset Manifest when the reference includes:

- empty-state illustrations
- official source logos or platform badges
- cover art, album art, product thumbnails, avatars, or placeholders
- brand-like marks or visual motifs
- artwork that gives the UI its finished feel

## Image generation permission

The agent must not generate images by default.

When an asset is missing:

1. If decorative:
   use a code fallback.

2. If needed but not urgent:
   write an Image Request.

3. If user explicitly allows Codex/imagegen:
   generate or edit the asset directly.

CSS fallback is a temporary implementation decision, not a substitute for asset planning.
If a fallback replaces a visible style carrier, mark it clearly in the Asset Manifest and ask whether it should become a Source or Generate asset before implementation.

## Image Request template

```md
# Image Request

## Purpose
[what this image is for]

## Placement
[page/component/state]

## Required size
[pixel size or aspect ratio]

## Background
transparent / white / green-screen / solid color / no preference

## Style
[visual style]

## Must include
- ...

## Must avoid
- ...

## Prompt
[copy-ready prompt]

## Fallback
[how the UI should work without this asset]
```

## Asset Manifest template

```md
# Asset Manifest

## Page
[page name]

| id | area | decision | output | required for MVP | notes |
|---|---|---|---|---|---|
| app-logo | top nav | Source | existing logo component | yes | do not redraw |
| empty-illustration | empty state | Generate | PNG transparent 1024x1024 | no | use CSS fallback until ready |
| tab-icons | bottom nav | Code | icon library | yes | do not crop from mockup |
| background-noise | page bg | Ignore | none | no | low value |
| source-logo | list/card source mark | Source | official logo asset | yes | do not redraw; ask user if missing |
| cover-placeholder | card cover visual | Source/Generate/Fallback | existing cover image or generated placeholder | no | fallback is temporary if visual fidelity matters |
```

## Transparency rule
Do not assume generated transparent images are truly transparent.

After receiving an asset that claims to be transparent:

- verify it has an alpha channel
- verify the background is actually transparent
- reject visible checkerboard backgrounds
- reject fake matte backgrounds
- reject unwanted white/green spill
- if transparency fails, regenerate on white or green background and clean it with scripts/prepare_image_asset.py

## Asset prep utility

Use scripts/prepare_image_asset.py only after an image asset has already been approved.

Typical use:

```bash
# Trim transparent padding
python scripts/prepare_image_asset.py input.png output.png

# White background to alpha
python scripts/prepare_image_asset.py input.png output.png --alpha

# Green-screen to alpha
python scripts/prepare_image_asset.py input.png output.png --key-color "#00ff00" --despill --edge-contract 1

```

## Hard rules

Never:

- use the full mockup as a background image
- crop low-resolution UI fragments as final assets by default
- mix large illustrations, logos, and tiny icons into one sprite sheet
- block implementation on decorative assets
- generate normal UI controls as images

Always:

- provide a fallback
- produce an Asset Manifest when visible assets affect fidelity
- ask whether Source or Generate assets should be supplied when a fallback would noticeably reduce fidelity
- save assets with clear names
- document target display size
- keep image assets separate and reusable
