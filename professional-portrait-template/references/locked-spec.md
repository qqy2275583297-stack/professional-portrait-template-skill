# Locked specification

## Priority and invariants

Use this priority order: (1) source identity and eyelids, (2) source hair, clothing, accessories, pose and all visible hands, (3) chest-up composition, (4) relighting/exposure, (5) fixed background, (6) text. Never solve a later rule by changing an earlier one.

Do not add lashes, eyeliner, mascara, eye enlargement, beauty contact lenses, eye makeup, face slimming, a new eyelid fold, or a double eyelid. If the source eyelid is uncertain, blur-obscured, under bangs/glasses, or low-resolution, render **no visible double-eyelid crease**. Keep the original hairstyle exactly: parting, bangs, width, length, density, volume, direction, flyaways and accessories. Keep original garment color, neckline/collar, sleeves, fabric, pattern, glasses, jewelry, straps and accessories. Keep head angle, body turn, shoulder tilt, expression, gesture, arms and every visible hand. Do not remove source glasses/hats or invent objects.

## Canvas and composition gate

- Canvas: 1080×1440 px, vertical 3:4.
- Subject: close chest-up portrait. No waist, hips, thighs, pants, large leg area or loose half-body/full-body framing.
- Highest visible hair pixel: target y=79 px; permitted y=58–101 px. Reject y>101. Do not create large empty headroom.
- Subject height, highest hair to bottom crop: 88–94% of canvas height. Bottom is chest/upper-chest/shoulder region, y=82–90%.
- Full silhouette visual centre: x=48.5–51.5%; face centre x=52–58%, y=34–40%.
- Chest-up size overrides side margins. Enlarge and centre the person rather than zooming out to create symmetric side gaps. Narrow/asymmetric side margins are allowed, but do not clip essential face, hair, clothing, or preserved hands.
- Do not change the no-text composition when text is added.

## Single image-generation pass — subject, relight and V3 integration

There is exactly one image-generation call. It must use the source portrait and `assets/locked-template-background-v3.png` together, and return the final no-text composition. Internally, within that one call only, first neutralize all source illumination and color cast to a flat diffuse-albedo working state, then apply the target light, then naturally integrate the result into the fixed V3 background. Do not create a temporary neutral-background image, a relight-only image, or a later background-fusion image.

### Exposure recovery inside the single pass

Inspect for night, flash, direct sun, backlight, dappled light, screen light, tungsten cast, underexposure, clipping, screenshots, watermarks and source crop. Remove source illumination and source color cast internally while preserving pores, hair strands, clothing weave, glasses and jewelry edges. Flat-light working targets before the final key: face left/right luma difference 8–14; neck 8–16; large clothing plane 12–20; remaining directional shadow ≤12 luma; cast-shadow residue ≤10 luma. Do not output this working state.

For all sources, including night/flash/overexposed/underexposed images, recover exposure internally before relight. Final no-text gate: P50 170–190, P90 218–235, P95 226–242, P99 236–250; luma >235 ≤1.8%; RGB channel >248 ≤0.35%; face highlight ≤218 except tiny peaks; hands ≤220; broad white/pale clothing 190–232 with visible texture. Reject and redo the one model pass if face, hands or white clothing are clipped.

### Locked relight inside the single pass

Main light: one large diffused softbox from camera-right/front-right at 45° horizontal azimuth, 30–40° above eye level, aimed down across face and right shoulder. 5200–5600 K. Weak camera-left/front-left ambient bounce = 0.25–0.35 of key; overall fill = 0.32–0.46; lighting ratio = 1.8–2.6:1. Add negative fill on camera-left and below chin.

Result must visibly show smooth controlled highlights on the subject's right cheekbone, nose bridge/tip and right shoulder, plus a fine right-facing hair-edge lift. Left cheek/jaw and lateral neck must carry a shallow readable soft shadow. Facial shadow area: 18–32% of visible face. Under-chin/lateral-neck shadow: 12–24% of visible neck, feathering 35–60 px. Do not make the face flat or universally soft.

Metering: face key luma 188–210, tiny controlled micro-peaks 215–225 only; shadow-side cheek/jaw 135–170; neck hollow 70–120; key-to-shadow delta 26–48; key-to-neck delta 55–95. Hair roots 12–32, hair body 18–46, lit strands 48–88. Keep transparent satin-matte native skin: healthy, subtle water-glow only on highlight planes, visible fine pores/microtexture, never oily or plastic. Use: `high commercial portrait lighting, Canon 5D Mark IV + 85mm F1.4 look, 8K, restrained realistic color, clean editorial portrait`.

### Locked V3 integration inside the same single pass

Use `assets/locked-template-background-v3.png` as the final immutable visual reference. Integrate naturally rather than cutting out, masking or pasting with local code. Use continuous hair/shoulder edge transitions and matching contact/ambient light; no cut-out halo, oval mask, pasted-looking outline, scene elements, texture, stains or grain. Do not reinterpret, recolor, white-balance, denoise, sharpen, blur, vignette, contrast-adjust or otherwise alter the background reference.

Validation only: overall RGB about (219,229,241); bright center RGB (232–242,238–246,247–251), luma 238–247; edge RGB (184–205,199–218,218–234), luma 198–225; no edge below (180,195,215). The bundled bitmap is authoritative over these validation ranges.

## Cleanup — non-generative, before text

Perform after the single image pass, before text. Remove random noise, dirty speckles, compression grit, muddy particles, color dirt and background smudges. Targets: background noise std 0–5; skin 1–7; clothing/hair 1–10; remove isolated dirty speckles under 3 px unless they are real moles/freckles. Preserve pores, lip texture, skin color variation, individual hair, glasses/jewelry edges, seams and weave. Skin smoothing strength 0.18–0.32 while texture preservation is 0.68–0.82. The image must read clean, smooth, breathable and realistic, never waxy.

## Fixed typography — code only

Generate no text with the model. Normalize the accepted 3:4 no-text output uniformly to 1080×1440, then create the text version only by running `scripts/apply_fixed_portrait_layout.py` on that exact base. Font: Segoe UI Semilight (not hairline/regular/bold/condensed). Exact strings:

1. `Gentle Silent Shots`
2. `Genuine Unscripted`
3. `Caught in Stillness`

Use x=42. Title: y=1050, 118 px, saturated blue in-glyph gradient `(28,86,174) → (32,96,190) → (24,80,170)`, alpha 252. Subtitles: y=1174 and y=1266, 80 px, saturated orange in-glyph gradient `(244,136,54) → (255,156,78) → (238,128,48) → (228,116,42)`, alpha 252. Keep it a large lower-third layout, never a small caption. The text stage may add only glyph pixels; it must never resize, crop, regenerate, relight, recolor or modify the no-text base.

## Mandatory quality gate

Before delivery, reject and redo the one generation if any applies: face/eyelids/hair/clothes/pose/hands changed; full/half-body framing; excessive headroom; person not visually centred; incorrect V3 background; source light survived; right-side key light/left neck shadow not visible; clipped highlights; noise/grit; background contamination; model-generated/misspelled text; or no-text/text composition mismatch. Deliver both files only after all gates pass.
