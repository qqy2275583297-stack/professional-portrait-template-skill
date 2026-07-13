---
name: professional-portrait-template
description: Transform an uploaded lifestyle photo into a locked 3:4 editorial professional portrait. Use when the user asks for a professional headshot, lifestyle-photo-to-professional-portrait transformation, or this fixed "Gentle Silent Shots" portrait template. Preserve identity, eyelids, hairstyle, clothing, pose and hands; use the bundled v3 background, staged studio relighting, deterministic typography, and deliver both no-text and text versions.
---

# Professional Portrait Template

Use this as a low-freedom workflow. Read [references/locked-spec.md](references/locked-spec.md) in full before generating anything. Its requirements are immutable unless the user explicitly says to replace a named fixed module. A new request adds a constraint; it does not silently alter composition, background, lighting, identity, or typography.

## Required resources

- Fixed final background: [assets/locked-template-background-v3.png](assets/locked-template-background-v3.png)
- Deterministic text overlay: [scripts/apply_fixed_portrait_layout.py](scripts/apply_fixed_portrait_layout.py)
- All numeric checks and exact generation prompts: [references/locked-spec.md](references/locked-spec.md)

Resolve paths from the directory containing this `SKILL.md`; never use the creator's machine-specific paths.

## Mandatory staged process

1. Inspect the source and record identity, eyelids, hair silhouette, clothing/accessories, pose, hands, crop, and exposure problems.
2. Generate **Pass 1**, a 1080×1440 chest-up, no-text identity/geometry master on a temporary neutral background. Preserve the source; remove its environment and normalize source light to flat diffuse light.
3. Generate **Pass 2** from the accepted Pass 1 only. Freeze all geometry and apply the numeric subject-only studio relight in the specification. Do not include the final background in this pass.
4. Generate **Pass 3** from the accepted Pass 2 with the bundled v3 background reference. Integrate naturally with the image model, not a local cutout; freeze subject pixels except a 1–2 px hair/shoulder edge blend.
5. Apply cleanup and pass every composition, lighting, exposure, background, and identity gate. If a gate fails, redo only the failed pass.
6. Save the accepted no-text base. Then use the bundled script to create the text version. Never regenerate, resize, crop, relight, or retouch after the no-text base is accepted.

## Text command

```powershell
$skill = '<directory-containing-SKILL.md>'
python "$skill/scripts/apply_fixed_portrait_layout.py" --src '<approved-no-text.png>' --out '<approved-with-text.png>'
```

If `python` is unavailable, use the environment's configured Python executable. The script rejects a non-1080×1440 base by design.

## Deliverables

Always deliver two files:

1. `professional-portrait-<slug>-no-text.png`
2. `professional-portrait-<slug>-with-text.png`

Show both images when the client supports local image previews. The with-text version must be pixel-identical to the no-text file outside the three text glyph layers.
