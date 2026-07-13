from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


W, H = 1080, 1440
FONT_CANDIDATES = (
    Path(r"C:\Windows\Fonts\segoeuisl.ttf"),
    Path(r"/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
)


def lerp(a: int, b: int, t: float) -> int:
    return round(a + (b - a) * t)


def mix(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(lerp(x, y, t) for x, y in zip(a, b))


def find_font(size: int) -> ImageFont.FreeTypeFont:
    for font_path in FONT_CANDIDATES:
        if font_path.exists():
            return ImageFont.truetype(str(font_path), size)
    raise FileNotFoundError("Segoe UI Semilight was not found. Install or point this script at an equivalent light sans-serif font.")


def draw_gradient_text(
    layer: Image.Image,
    position: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    stops: tuple[tuple[float, tuple[int, int, int]], ...],
    alpha: int = 252,
) -> None:
    canvas = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = canvas.textbbox(position, text, font=font, anchor="lt")
    width, height = x1 - x0, y1 - y0
    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).text((0, 0), text, font=font, fill=255, anchor="lt")
    gradient = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels = gradient.load()
    for y in range(height):
        vertical = 1 - y / max(1, height - 1)
        for x in range(width):
            t = x / max(1, width - 1)
            for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
                if p0 <= t <= p1:
                    rgb = mix(c0, c1, (t - p0) / max(1e-6, p1 - p0))
                    break
            else:
                rgb = stops[-1][1]
            lift = 0.08 * (1 - t) + 0.035 * vertical
            pixels[x, y] = (*tuple(min(255, round(c * (1 + lift))) for c in rgb), alpha)
    gradient.putalpha(mask.point(lambda value: round(value * alpha / 255)))
    layer.alpha_composite(gradient, (x0, y0))


def overlay_text(src: Path, out: Path) -> None:
    base = Image.open(src).convert("RGBA")
    if base.size != (W, H):
        raise ValueError(f"No-text base must be exactly {W}x{H}; got {base.size}. Approve composition before typography.")
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    title_font = find_font(118)
    subtitle_font = find_font(80)
    blue = ((0.00, (28, 86, 174)), (0.55, (32, 96, 190)), (1.00, (24, 80, 170)))
    orange = ((0.00, (244, 136, 54)), (0.18, (255, 156, 78)), (0.45, (238, 128, 48)), (1.00, (228, 116, 42)))
    draw_gradient_text(layer, (42, 1050), "Gentle Silent Shots", title_font, blue)
    draw_gradient_text(layer, (42, 1174), "Genuine Unscripted", subtitle_font, orange)
    draw_gradient_text(layer, (42, 1266), "Caught in Stillness", subtitle_font, orange)
    out.parent.mkdir(parents=True, exist_ok=True)
    Image.alpha_composite(base, layer).convert("RGB").save(out, quality=97)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add the locked typography without changing the approved base portrait.")
    parser.add_argument("--src", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    overlay_text(args.src, args.out)
    print(args.out)
