# Asset Workflow

## Goal

Decide which visual elements should be code, existing source assets, generated assets, or ignored.

Do not over-extract assets.
Most UI should be rebuilt with code.

Code-first does not mean asset-blind.
Produce an Asset Manifest for every image-based design-to-code request.
If no formal assets are required, say that explicitly in the manifest.

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

Even when creating zero new assets, still list visible asset decisions in an Asset Manifest.

Pay special attention when the reference includes:

- empty-state illustrations
- official source logos or platform badges
- cover art, album art, product thumbnails, avatars, or placeholders
- brand-like marks or visual motifs
- artwork that gives the UI its finished feel

## Image generation permission

The agent must not generate images by default.

When an asset is missing, do not silently choose fallback for style-carrying assets.

1. If it is low-value decorative noise:
   use a code fallback.

2. If it affects fidelity, mood, empty-state quality, card feel, brand-like motif, or another visible style carrier:
   ask the user to choose Source, Generate, or Fallback before implementation.

3. If it is needed but not urgent:
   write an Image Request and mark the fallback as temporary.

4. If user explicitly allows Codex/imagegen:
   generate or edit the asset directly.

CSS fallback is a temporary implementation decision, not a substitute for asset planning.
If a fallback replaces a visible style carrier, mark it clearly in the Asset Manifest and ask whether it should become a Source or Generate asset before implementation.

## Asset decision prompt

Use this prompt whenever a missing asset would noticeably affect visual fidelity:

```md
## Asset Decision Needed

The reference includes these style-carrying assets:

| id | role | why it matters | options | recommended |
|---|---|---|---|---|
| [asset-id] | [placement] | [fidelity impact] | Source / Generate / Fallback | [choice + reason] |

Please choose:
- Source: you will provide or point me to the real asset
- Generate: I may use imagegen to create an isolated reusable asset
- Fallback: I will use the listed code/CSS fallback and mark the fidelity tradeoff
```

If there are multiple minor Generate candidates, batch them into one decision prompt instead of asking one question per asset.

## Generate Asset Workflow

Use this only after the user approves generation or the current runtime explicitly allows Codex/imagegen for the requested asset.

Generate is appropriate when the approved Asset Manifest marks an asset as Generate and the asset materially affects fidelity, such as:

- empty-state illustration
- cover placeholder
- mascot or hero object
- brand-like visual motif
- complex background artwork

Do not generate:

- official logos
- vendor/source marks
- normal UI controls
- text-heavy UI screenshots
- anything the project should load from source data

### Before generation

For each Generate row, prepare:

- asset id
- placement and display size
- required aspect ratio or pixel size
- background requirement: transparent / white / green-screen / solid color
- style carriers to preserve from the reference
- must include
- must avoid
- fallback if generation fails

If the reference image should guide the asset style, use image-to-image editing/generation with the reference image plus a targeted prompt.
Do not ask imagegen to recreate the whole screen.
Ask it to create only the isolated reusable asset.

### Prompt shape

```md
Create an isolated [asset type] for [placement].
Match the reference UI's [style carriers: color, material, line weight, mood].
Size/aspect: [target].
Background: [transparent / white / green-screen / solid].
Must include: [...]
Must avoid: text, UI controls, logos, full-screen mockup, unwanted background.
Output should be reusable in the app UI.
```

### After generation

Verify:

- the asset matches the requested role and placement
- text is absent unless explicitly requested
- no official logo has been hallucinated
- transparent assets really have alpha
- no checkerboard, fake matte, white spill, or green spill remains
- crop and padding match intended display size
- the asset still works if the fallback is used instead

If transparency or padding is wrong, use `scripts/prepare_image_asset.py`.
If the generated concept is wrong, regenerate with a narrower prompt.

### Generated asset output

Save generated assets with stable names:

```text
assets/generated/[page-or-feature]/[asset-id].png
```

If the host project has an existing asset convention, follow that convention instead.
Record the final file path in the Asset Manifest before implementation.

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

## Summary
[formal assets required / no formal assets required]

| id | area | decision | output | required for MVP | fallback | needs user decision | notes |
|---|---|---|---|---|---|---|---|
| app-logo | top nav | Source | existing logo component | yes | text label | yes if missing | do not redraw |
| empty-illustration | empty state | Generate | PNG transparent 1024x1024 | no | simple CSS empty state | yes | use fallback until approved |
| tab-icons | bottom nav | Code | icon library | yes | icon library | no | do not crop from mockup |
| background-noise | page bg | Ignore | none | no | none | no | low value |
| source-logo | list/card source mark | Source | official logo asset | yes | text/source initials | yes if missing | do not redraw; ask user if missing |
| cover-placeholder | card cover visual | Source/Generate/Fallback | existing cover image or generated placeholder | no | gradient placeholder | yes if fidelity matters | fallback is temporary if visual fidelity matters |
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
- produce an Asset Manifest for every image-based design-to-code request
- ask whether Source or Generate assets should be supplied when a fallback would noticeably reduce fidelity
- ask the user to choose Source, Generate, or Fallback before implementation when a missing asset is a visible style carrier
- save assets with clear names
- document target display size
- keep image assets separate and reusable
