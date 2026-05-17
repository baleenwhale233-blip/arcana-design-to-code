# Measurement Pass

## Goal

Extract implementation-ready numeric tokens from a UI image when fidelity matters.

Use this when the user asks for accurate values, exact tokens, "具体数值", "圆角", "边距", "字号", "像素级", "高保真", or when the reference role is Fidelity Target.

Do not treat this as private reasoning. Include a concise Design Measurements section in the brief.

## Accuracy rule

Be explicit about confidence:

- measured: directly measured from the source image after viewport calibration
- estimated: visually estimated from image evidence
- inferred: chosen from a design-system scale because the image is ambiguous
- unknown: cannot be determined from the available image

Never present estimated or inferred values as exact.
If exactness is required and the source is only a compressed chat image, ask for a higher-resolution screenshot, Figma link, source file, or known viewport size.

## Required viewport inputs

Do not use the reference image's bitmap size as the implementation target.

Before measuring, identify:

- source viewport: the CSS viewport or device size the reference image was designed for, such as 390x844
- implementation targets: the device or viewport range the UI must adapt to, such as 360x800, 390x844, 430x932, tablet, or desktop

If the user only provides a device name, infer the likely CSS viewport only when you are confident and record the assumption.
If the user only provides a bitmap image with no source viewport or device, ask for the intended source device/viewport when numeric fidelity matters.

## Process

1. Calibrate the image.
   Record source image pixel size and source viewport CSS size.
   Compute scale: image pixels / source CSS pixels.
   If source viewport is unknown, infer it from common device sizes and mark values estimated.

   When a local image file is available, prefer `scripts/measure_ui_image.py` for calibration and repeatable measurements:

   ```bash
   python3 scripts/measure_ui_image.py screenshot.png --source-viewport 390x844
   ```

2. Measure layout anchors first.
   Capture page padding, safe areas, navigation height, tab bar height, primary content width, major section gaps, card widths, card heights, and list row heights.

   Use explicit coordinate measurements when precision matters:

   ```bash
   python3 scripts/measure_ui_image.py screenshot.png \
     --source-viewport 390x844 \
     --rect card:16,132,358,180 \
     --distance page-padding:0,0,16,0 \
     --sample-box surface:20,136,20,20
   ```

3. Measure component tokens.
   Capture card padding, control padding, icon box size, avatar/image size, button height, input height, chip height, divider thickness, border thickness, and common gaps.

4. Measure typography.
   Estimate font size from text bounding-box height and line-height rhythm.
   Record weight, line height, and hierarchy.
   Use likely CSS values such as 12, 13, 14, 15, 16, 18, 20, 24, 28, 32 when the screenshot is ambiguous.

5. Measure shape and elevation.
   Capture corner radius for cards, buttons, chips, inputs, modals, images, and app containers.
   Capture shadow direction, blur, opacity, and border color if visible.

   For radius, use `--radius-probe name:x,y,w,h` only as an estimate. If the source image is anti-aliased, shadowed, or compressed, manually inspect the corner and pass `--manual-radius name:px`.

6. Normalize into implementable tokens.
   Prefer consistent scales over one-off noisy values.
   Example: if measured gaps are 15, 16, and 17 px, output 16 px with confidence measured/normalized.

7. Adapt tokens to implementation targets.
   Do not proportionally scale the entire screenshot.
   Keep the measured source values as evidence, then generate responsive rules and target-specific token suggestions.

   Use:

   ```bash
   python3 scripts/measure_ui_image.py screenshot.png \
     --source-viewport 390x844 \
     --target-viewport compact:360x800 \
     --target-viewport large-phone:430x932
   ```

   Prefer responsive CSS such as `clamp(...)`, fluid containers, and max-widths over fixed screenshot widths.

## Script workflow

The measurement script is deliberately semi-automatic:

- the agent decides which points, boxes, distances, text bounds, and radius probes matter
- the script converts image pixels to CSS pixels and returns JSON or Markdown
- the agent normalizes the output into design tokens and marks uncertainty

Useful options:

```bash
python3 scripts/measure_ui_image.py screenshot.png \
  --source-viewport 390x844 \
  --target-viewport compact:360x800 \
  --target-viewport large-phone:430x932 \
  --rect header:0,0,390,88 \
  --rect card:16,132,358,180 \
  --distance card-gap:16,312,16,328 \
  --text title:24,54,220,34 \
  --radius-probe card:16,132,358,180 \
  --sample-box background:0,0,20,20 \
  --format json
```

The script output is raw evidence. Do not paste it blindly into implementation. Convert it into the brief's Design Measurements tables and token recommendations.

## Output template

```md
## Design Measurements

### Calibration
- source image:
- image pixels:
- source viewport:
- scale:
- accuracy notes:

### Layout
| item | value | confidence | notes |
|---|---:|---|---|
| page padding | 16px | measured | left/right content inset |

### Typography
| role | size | line-height | weight | confidence | notes |
|---|---:|---:|---|---|---|
| page title | 28px | 34px | 700 | estimated | based on text box height |

### Components
| component | width/height | padding/gap | radius | confidence | notes |
|---|---|---|---:|---|---|
| primary button | h 48px | 16px horizontal | 24px | measured | pill button |

### Tokens To Use
- spacing: 4, 8, 12, 16, 20, 24, 32
- radius: 8, 12, 16, 24
- typography:
- borders/shadows:

### Adaptation Targets
| target | viewport | spacing | radius | typography | layout guidance |
|---|---:|---|---|---|---|
| compact phone | 360x800 | 4, 8, 12, 16, 20 | 8, 12, 16 | 13, 16, 20, 24 | use fluid width, not screenshot lock |

### Unknowns
- [value that cannot be read accurately and what source would resolve it]
```

## Brief integration

When measurements are requested, include:

- the Design Measurements table
- which values are measured vs estimated vs inferred
- any source-quality limitations
- which numeric tokens should be used during implementation
