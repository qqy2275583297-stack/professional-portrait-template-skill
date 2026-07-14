from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1440
FONT_PATH = Path(r"C:\Windows\Fonts\segoeuisl.ttf")


def lerp(a: int, b: int, t: float) -> int:
    return round(a + (b - a) * t)


def mix(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(lerp(x, y, t) for x, y in zip(a, b))


def draw_gradient_text(layer: Image.Image, pos: tuple[int, int], text: str, size: int, stops: tuple[tuple[float, tuple[int, int, int]], ...]) -> None:
    font = ImageFont.truetype(str(FONT_PATH), size)
    draw = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = draw.textbbox(pos, text, font=font, anchor="lt")
    mask = Image.new("L", (x1 - x0, y1 - y0), 0)
    ImageDraw.Draw(mask).text((0, 0), text, font=font, fill=255, anchor="lt")
    gradient = Image.new("RGBA", mask.size)
    pixels = gradient.load()
    for y in range(mask.height):
        vertical = 1 - y / max(1, mask.height - 1)
        for x in range(mask.width):
            t = x / max(1, mask.width - 1)
            for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
                if p0 <= t <= p1:
                    color = mix(c0, c1, (t - p0) / max(1e-6, p1 - p0))
                    break
            else:
                color = stops[-1][1]
            lift = 0.08 * (1 - t) + 0.035 * vertical
            pixels[x, y] = (*tuple(min(255, round(c * (1 + lift))) for c in color), 252)
    gradient.putalpha(mask.point(lambda value: round(value * 252 / 255)))
    layer.alpha_composite(gradient, (x0, y0))


def main() -> None:
    parser = argparse.ArgumentParser(description="Create the locked transparent typography placement reference.")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--background", type=Path)
    args = parser.parse_args()
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    blue = ((0.00, (28, 86, 174)), (0.55, (32, 96, 190)), (1.00, (24, 80, 170)))
    orange = ((0.00, (244, 136, 54)), (0.18, (255, 156, 78)), (0.45, (238, 128, 48)), (1.00, (228, 116, 42)))
    draw_gradient_text(overlay, (42, 1050), "Gentle Silent Shots", 118, blue)
    draw_gradient_text(overlay, (42, 1174), "Genuine Unscripted", 80, orange)
    draw_gradient_text(overlay, (42, 1266), "Caught in Stillness", 80, orange)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.background:
        base = Image.open(args.background).convert("RGBA")
        # The bundled V3 asset is an exact 3:4 master (currently 1086×1448).
        # This preview normalizes it to the locked 1080×1440 delivery canvas;
        # it never writes back to or alters the master background asset.
        if base.size != (W, H):
            if abs(base.width / base.height - W / H) > 0.0001:
                raise ValueError(f"Background must be 3:4; got {base.size}.")
            base = base.resize((W, H), Image.Resampling.LANCZOS)
        Image.alpha_composite(base, overlay).convert("RGB").save(args.out, quality=97)
    else:
        overlay.save(args.out)
    print(args.out)


if __name__ == "__main__":
    main()
