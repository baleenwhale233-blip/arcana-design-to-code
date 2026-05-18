# Generate Candidate Scan

## Goal

Help the agent notice which visual resources should become Source, Generate, or image-to-image assets instead of being silently rebuilt with CSS or dropped as fallback.

Use this before the Asset Manifest when a reference image includes any non-UI visual, artwork, media placeholder, illustration, avatar, cover, hero object, mascot, texture, or brand-like motif.

## Scan order

Inspect the reference image by region:

1. App shell and navigation
   Look for official logos, source marks, app icons, platform badges.

2. Hero or primary visual area
   Look for hero objects, product renderings, 3D/glass objects, complex illustrations, central decorative artwork.

3. Content cards and list items
   Look for cover art, thumbnails, avatars, album art, posters, product images, generated placeholders.

4. Empty, loading, onboarding, or success states
   Look for illustrations, mascots, badges, confetti, state artwork.

5. Background and surface treatment
   Look for texture, complex background artwork, glass material, glow fields, or visual motifs that carry the mood.

6. Tiny decorations
   Identify low-value noise, accidental AI marks, fake logos, and details to ignore.

## Decision rubric

Choose `Source` when:

- the asset is an official logo, vendor badge, brand mark, real product image, or existing media
- hallucinating or redrawing it would be misleading
- an independent source file, URL, or project asset exists; a crop from a mockup/screenshot is not Source by itself

Choose `Generate` when:

- the asset is visually central and not official/source material
- CSS/SVG would look stiff, generic, or expensive
- the asset is reusable across the UI
- removing it would noticeably reduce fidelity or finished quality
- the asset is a mascot, sticker, hero object, soft/3D object, illustration, or irregular silhouette and no independent source asset exists

Choose `Image-to-image` when:

- the reference image defines the asset's style, material, silhouette, or mood
- the asset should be regenerated as an isolated reusable object
- the agent must not recreate the whole screen, only the selected asset
- the object is embedded in UI, background, shadows, or surrounding content but should behave as a separate transparent asset
- the object protrudes from a container, overlaps UI chrome, or depends on an irregular silhouette

Choose `Code` when:

- the visual is a normal UI control, simple icon, ordinary gradient, card, divider, chart, badge, or layout surface
- the effect can be represented cleanly with CSS, SVG, or an icon library

Choose `Ignore` when:

- the visual is low-value noise, accidental AI texture, fake tiny marks, or decorative clutter
- keeping it would not affect the user's task or design identity

## Screenshot asset trap

If the visual reference contains an object inside a screenshot, do not treat that object as a usable source asset just because pixels are visible.

Classify it as `Image-to-image` or `Generate` when:

- it carries the page's mood, brand-like feel, empty-state quality, or finished quality
- it has a non-rectangular silhouette or needs transparent edges
- it must be layered independently, reused, or allowed to protrude outside a container

Only use a screenshot crop as temporary reference material or image-to-image guidance. A final crop is acceptable only when the user explicitly approves that fidelity tradeoff.

## Must not generate

- official logos or vendor marks
- source-owned content that should come from product data
- normal UI controls
- text-heavy screenshots
- the entire mockup as one background
- illegible AI text or fake chart labels
- screenshot crops of embedded mascots, illustrations, hero objects, stickers, or irregular silhouettes as final assets

## Output template

```md
## Generate Candidate Scan

| candidate | region | role | style impact | decision | generation mode | why not code | fallback |
|---|---|---|---|---|---|---|---|
| empty-state object | empty state center | gives the state a finished feel | high | Generate | image-to-image | CSS would look generic | simple icon + copy |
| app logo | top nav | source identity | high | Source | none | official mark required | text label |
| tab icons | bottom nav | navigation affordance | low | Code | none | icon library is enough | lucide icons |
```

If no Generate candidates are found:

```md
## Generate Candidate Scan

No Generate candidates found.
Reason: all visible elements are normal UI controls, source assets, simple CSS surfaces, or low-value decorations.
```

## User decision rule

For every candidate with decision `Generate` or `Image-to-image`, include it in the Asset Decision prompt unless the user has already approved generation.

If image generation is unavailable, still list the candidate and ask the user to choose Source or Fallback.
