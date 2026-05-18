# Exit Check

This is not a full QA process.

Use this only to prevent obviously incomplete implementation.

## Must pass

Before finishing, check:

- The primary user task can be completed.
- The main information hierarchy matches the brief.
- The layout works on the target viewport.
- Text is readable.
- Buttons and inputs are usable.
- Required empty/loading/error/success states are not obviously missing.
- Custom assets are either integrated or replaced with acceptable fallbacks.
- Asset fallbacks match the approved Asset Manifest; Source/Generate assets are not silently downgraded.
- Constrained-height screens fit the approved Viewport Budget or explicitly use the approved scroll policy.
- The implementation does not use the mockup as a full-page image.
- Ordinary UI controls are implemented as code, not cropped images.
- The implementation does not introduce unnecessary dependencies.
- The result is coherent enough to continue product work.

## Implementation verification

When code was changed, run the lightest relevant project verification available.

Prefer existing project commands:

- typecheck
- lint
- unit tests for touched logic
- build
- existing app-specific verification scripts

If the project has no obvious command, at least start or inspect the implemented page locally when practical.

Report what was run.
If a check could not be run, explain why.

## Visual check

Open the page in the target viewport and inspect:

- overall layout rhythm
- content density
- typography scale
- major spacing
- viewport budget: fixed sections, gaps, min-heights, safe padding, and overflow behavior
- color mood
- component consistency
- obvious broken styles

When practical, also check:

- the primary target viewport from the brief
- one narrower viewport for responsive risk
- browser or runtime console for obvious errors
- long text or empty data if the page includes dynamic content

Do not run pixel-level comparison against AI-generated mockups.
Do not fail the result for tiny spacing differences unless the image is a confirmed Fidelity Target.

## Screenshot check

When a browser or app preview is available, capture or inspect a screenshot after implementation.

Compare against the selected reference intent:

- IA Reference: module order, hierarchy, actions, and flow should match.
- Visual Style Reference: color mood, typography feel, spacing rhythm, radius, shadow, and density should align.
- Direction Reference: overall character should be recognizable without forcing exact layout.
- Fidelity Target: major layout, content, and visual proportions should be close at the target viewport.

Do not use pixel diff for AI-generated mockups.

## Do not do

- Do not chase tiny spacing differences.
- Do not treat AI mockups as pixel specs.
- Do not start a full regression QA workflow.
- Do not block delivery on decorative assets.
- Do not turn visual refinement into QA.
- Do not claim completion without checking the implemented surface when a local preview is available.

## Stop condition

Stop when the page is:

- usable
- coherent
- aligned with the selected reference intent
- checked in the target viewport when practical
- within the approved height budget when the screen is constrained-height
- implementation-ready

Full QA belongs to a separate UI-QA workflow.
