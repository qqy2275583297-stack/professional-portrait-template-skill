#!/usr/bin/env python3
"""Uniformly normalize a generated 3:4 portrait to the locked 1080x1440 canvas."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


TARGET = (1080, 1440)
TARGET_RATIO = TARGET[0] / TARGET[1]
RATIO_TOLERANCE = 0.002


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    with Image.open(args.input) as image:
        ratio = image.width / image.height
        if abs(ratio - TARGET_RATIO) > RATIO_TOLERANCE:
            raise SystemExit(
                f"Refusing to crop or distort {image.width}x{image.height}; expected a 3:4 model output."
            )
        normalized = image.convert("RGB").resize(TARGET, Image.Resampling.LANCZOS)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        normalized.save(args.output, quality=95, subsampling=0)


if __name__ == "__main__":
    main()
