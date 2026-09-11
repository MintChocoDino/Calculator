"""Generate the app icon (assets/calculator.ico) from the app's own palette.

Run:  python build/make_icon.py
"""

from pathlib import Path

from PIL import Image, ImageDraw

BG = "#16181d"
DISPLAY = "#0f1115"
KEY = "#2f3440"
ACCENT = "#f0a04b"

SIZE = 1024  # drawn large, then downsampled for crisp small sizes
OUT = Path(__file__).resolve().parent.parent / "assets" / "calculator.ico"


def draw() -> Image.Image:
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = SIZE / 100.0  # work in percentage units

    # rounded body
    d.rounded_rectangle([4 * s, 4 * s, 96 * s, 96 * s], radius=18 * s, fill=BG)

    # display panel
    d.rounded_rectangle([16 * s, 14 * s, 84 * s, 34 * s], radius=5 * s, fill=DISPLAY)
    d.rounded_rectangle([60 * s, 21 * s, 78 * s, 27 * s], radius=3 * s, fill=ACCENT)

    # keypad, sized to exactly fill its area so nothing spills past the body
    cols, rows, gap = 4, 3, 5 * s
    x0, y0, x1, y1 = 16 * s, 40 * s, 84 * s, 88 * s
    kw = (x1 - x0 - gap * (cols - 1)) / cols
    kh = (y1 - y0 - gap * (rows - 1)) / rows
    for row in range(rows):
        for col in range(cols):
            kx = x0 + col * (kw + gap)
            ky = y0 + row * (kh + gap)
            accent = row == rows - 1 and col == cols - 1
            d.rounded_rectangle(
                [kx, ky, kx + kw, ky + kh],
                radius=3.5 * s,
                fill=ACCENT if accent else KEY,
            )
    return img


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img = draw()
    sizes = [(n, n) for n in (256, 128, 64, 48, 32, 24, 16)]
    img.save(OUT, format="ICO", sizes=sizes)
    img.resize((256, 256), Image.LANCZOS).save(OUT.with_suffix(".png"))
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes) and {OUT.with_suffix('.png').name}")


if __name__ == "__main__":
    main()
