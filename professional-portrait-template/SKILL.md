---
name: professional-portrait-template
description: Transform an uploaded lifestyle photo into a locked 3:4 editorial professional portrait. Use exactly one image-generation pass for the fixed person, exposure recovery, studio relighting, and natural fixed-background integration; add deterministic typography only afterward. Preserve identity, eyelids, hairstyle, clothing, pose and hands, and deliver no-text and with-text versions.
---

# Professional Portrait Template

Read [references/locked-spec.md](references/locked-spec.md) and [references/one-pass-draft.md](references/one-pass-draft.md) completely before generating anything. The one-pass workflow is the locked generation order. All identity, composition, lighting, background, typography, cleanup values and quality gates are mandatory.

## Required resources

- Final immutable background: [assets/locked-template-background-v3.png](assets/locked-template-background-v3.png)
- Exact final typography renderer: [scripts/apply_fixed_portrait_layout.py](scripts/apply_fixed_portrait_layout.py)
- Transparent text-placement reference: [scripts/render_typography_overlay.py](scripts/render_typography_overlay.py)
- Fixed canvas normalizer: [scripts/normalize_canvas.py](scripts/normalize_canvas.py)
- Numeric invariant rules: [references/locked-spec.md](references/locked-spec.md)
- Single-pass prompt and controls: [references/one-pass-draft.md](references/one-pass-draft.md)

Resolve paths from this `SKILL.md`; never use the creator's machine-specific paths.

## Mandatory workflow

1. Audit identity, eyelids, hair, clothing/accessories, pose, visible hands, crop, screenshots/watermarks, and exposure issues.
2. Generate the **final no-text portrait once**. The one model call must combine: identity/geometry locking, source-light neutralization, exposure recovery, fixed 45° studio relight, and natural fusion with the fixed V3 background. Do not produce a subject master, relight-only image, background-fusion image, or any other intermediate generated image.
3. Uniformly normalize the accepted 3:4 result to 1080×1440 with `normalize_canvas.py`. This is non-generative resizing only; do not crop, reframe, relight, or composite.
4. Apply locked cleanup without another image-generation pass. Reject and redo the single generation only if any quality gate fails.
5. Save the accepted no-text image. Render the text image only with the deterministic script. The text version must never resize, crop, relight, retouch, regenerate, or otherwise alter the no-text base.

## Text command

```powershell
$skill = '<directory-containing-SKILL.md>'
python "$skill/scripts/apply_fixed_portrait_layout.py" --src '<approved-no-text.png>' --out '<approved-with-text.png>'
```

## Deliverables

Always deliver exactly these two files:

1. `professional-portrait-<slug>-no-text.png`
2. `professional-portrait-<slug>-with-text.png`

Show both when the client supports local image previews. Outside the three text glyph layers, the two files must be pixel-identical.
