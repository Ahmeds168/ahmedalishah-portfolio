#!/usr/bin/env python3
"""
Generate an Open Graph image.

    python3 scripts/gen-og.py <slug> <kicker> <title> [accent-hex]

e.g.
    python3 scripts/gen-og.py foundry-forge-test-mt "FOUNDRY DEBUGGING SERIES" \
        'Foundry "forge test --m" Not Working? Use --mt'

Writes public/images/og/<slug>.png at 1200x630, matching the rest of the site.
Requires rsvg-convert (apt install librsvg2-bin).
"""
import os
import subprocess
import sys
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "public", "images", "og")
DEFAULT_ACCENT = "#2563EB"


def wrap(text, width=30, max_lines=3):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur + " " + w) <= width:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines[:max_lines]


def build(slug, kicker, title, accent=DEFAULT_ACCENT):
    lines = [escape(l) for l in wrap(title)]
    tspans = "".join(
        f'<text x="90" y="{300 + i * 66}" font-family="Manrope, Inter, sans-serif" '
        f'font-size="48" font-weight="700" fill="#111827">{l}</text>'
        for i, l in enumerate(lines)
    )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630">
<defs>
  <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#FFFFFF"/><stop offset="100%" stop-color="#F6F8FE"/>
  </linearGradient>
  <filter id="b"><feGaussianBlur stdDeviation="90"/></filter>
</defs>
<rect width="1200" height="630" fill="url(#g)"/>
<circle cx="1090" cy="80" r="230" fill="{accent}" opacity="0.10" filter="url(#b)"/>
<rect x="0" y="0" width="1200" height="6" fill="{accent}"/>
<text x="90" y="150" font-family="JetBrains Mono, monospace" font-size="19" fill="{accent}">{escape(kicker)}</text>
{tspans}
<text x="90" y="556" font-family="Inter, sans-serif" font-size="24" fill="#667085">Syed Ahmed Ali Shah · ahmedalishah.vercel.app</text>
</svg>"""

    os.makedirs(OUT_DIR, exist_ok=True)
    svg_path = f"/tmp/og-{slug}.svg"
    png_path = os.path.join(OUT_DIR, f"{slug}.png")
    with open(svg_path, "w") as f:
        f.write(svg)
    subprocess.run(
        ["rsvg-convert", "-w", "1200", "-h", "630", svg_path, "-o", png_path],
        check=True,
    )
    return png_path


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)
    slug, kicker, title = sys.argv[1], sys.argv[2], sys.argv[3]
    accent = sys.argv[4] if len(sys.argv) > 4 else DEFAULT_ACCENT
    print("wrote", build(slug, kicker, title, accent))
