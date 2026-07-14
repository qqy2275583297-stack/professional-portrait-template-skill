# Locked one image-generation pass

## Intent

Prevent accumulated resampling, noise, and dirty artifacts. Permit exactly **one** image-generation call per source portrait. That call must create the final clean no-text portrait: fixed person, exposure recovery, final studio relight, and natural integration with the locked V3 background. Typography is added later by deterministic code and is not an image-generation pass.

## Fixed inputs

- Source lifestyle image: identity, face, hair, clothing, accessories, pose, hands, and gesture reference.
- `../assets/locked-template-background-v3.png`: the only final background reference.
- `../typography-placement-overlay.png`: placement guide only. Do not render its letters during generation.
- `../scripts/apply_fixed_portrait_layout.py`: the only typography renderer.

## The single model pass

Give the model the source image and locked V3 background together. Generate a clean, text-free 3:4 portrait in one call. The following are internal requirements of this same generation, not separate images or later model edits:

1. Preserve the source person's facial geometry, head-to-shoulder ratio, hairstyle silhouette, clothing, accessories, body angle, pose, and every visible hand/finger placement.
2. Diagnose source exposure. Internally recover clipped highlights or blocked shadows to neutral, even working exposure before applying the target lighting; do not preserve the source scene's lighting direction.
3. Recalculate and apply the locked studio lighting from `locked-spec.md` to the preserved person.
4. Integrate the person naturally into the locked V3 background in this same image: continuous edge transitions, matching contact/ambient light, no cut-out halo, no oval mask, no pasted-looking outline, and no new scene elements.
5. Output a clean text-free image only. The typography guide is coordinate reference only and must not be drawn, approximated, or generated.

### Hard generation instruction

`Create one final, text-free 3:4 professional portrait from the supplied lifestyle photo and the supplied locked V3 background. In this same single generation, preserve the exact person and all visible pose details; internally normalize source exposure; then apply the locked 45-degree studio relight and naturally integrate the person into the supplied V3 background. Do not create or imply a separate subject-master, relighting, or background-fusion pass. Do not add text, logos, watermarks, lashes, double-eyelid creases, makeup, accessories, altered hair, altered clothing, altered hands, or altered pose. No collage, oval mask, halo, pasted cut-out edge, extra objects, noise, grain, dirt, or film texture.`

## Non-generative finishing only

After the one model output:

1. Use `normalize_canvas.py` to uniformly resample the exact 3:4 result to 1080×1440. Reject outputs that are not 3:4 rather than cropping or recomposing them.
2. Run only the locked non-generative cleanup limits in `locked-spec.md`.
3. Export the clean no-text portrait.
4. Run `apply_fixed_portrait_layout.py` on that exact no-text file to add the fixed typography. Do not resize, crop, regenerate, relight, or otherwise change the base portrait after text is applied.

## Required deliverables

- `professional-portrait-<source>-no-text.png`
- `professional-portrait-<source>-with-text.png`

The two outputs must have identical pixels outside the typography glyph areas.
