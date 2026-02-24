import json
import os
import sys

COUNTER_FILE = "counter.json"
OUTPUT_SVG = "assets/nixie-counter.svg"

DIGIT_WIDTH = 56
DIGIT_HEIGHT = 90
PADDING = 8
TUBE_GAP = 6


def get_count():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "r") as f:
            data = json.load(f)
            return data.get("count", 0)
    return 0


def save_count(count):
    with open(COUNTER_FILE, "w") as f:
        json.dump({"count": count}, f)


def generate_svg(count):
    digits = str(count).zfill(6)
    num_digits = len(digits)
    total_w = num_digits * (DIGIT_WIDTH + TUBE_GAP) - TUBE_GAP + PADDING * 2
    total_h = DIGIT_HEIGHT + PADDING * 2

    # SVG header + defs with glow filter
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="{total_h}" viewBox="0 0 {total_w} {total_h}">
  <defs>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="blur1"/>
      <feGaussianBlur in="SourceGraphic" stdDeviation="6" result="blur2"/>
      <feMerge>
        <feMergeNode in="blur2"/>
        <feMergeNode in="blur1"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <radialGradient id="tubeBg" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#1a1008"/>
      <stop offset="100%" stop-color="#0a0a0a"/>
    </radialGradient>
<!-- PLACEHOLDER_1 -->"""

    # Add gradient for each digit
    for i, d in enumerate(digits):
        svg += f"""
    <radialGradient id="digitGlow{i}" cx="50%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#ffaa33" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#ffaa33" stop-opacity="0"/>
    </radialGradient>"""

    svg += """
  </defs>"""

    # Background
    svg += f"""
  <rect width="{total_w}" height="{total_h}" rx="8" fill="#0d0d0d"/>"""

    # Draw each tube
    for i, d in enumerate(digits):
        x = PADDING + i * (DIGIT_WIDTH + TUBE_GAP)
        cx = x + DIGIT_WIDTH / 2
        cy = PADDING + DIGIT_HEIGHT / 2

        svg += f"""
  <!-- Tube {i} -->
  <rect x="{x}" y="{PADDING}" width="{DIGIT_WIDTH}" height="{DIGIT_HEIGHT}" rx="6" fill="url(#tubeBg)" stroke="#222" stroke-width="1"/>
  <rect x="{x}" y="{PADDING}" width="{DIGIT_WIDTH}" height="{DIGIT_HEIGHT}" rx="6" fill="url(#digitGlow{i})"/>
  <text x="{cx}" y="{cy + 4}" text-anchor="middle" dominant-baseline="middle" font-family="'Courier New', monospace" font-size="52" font-weight="bold" fill="#ff8c00" filter="url(#glow)" opacity="0.95">{d}</text>
  <text x="{cx}" y="{cy + 4}" text-anchor="middle" dominant-baseline="middle" font-family="'Courier New', monospace" font-size="52" font-weight="bold" fill="#ffb347" opacity="0.3">{d}</text>"""

    # Glass reflection
    for i in range(num_digits):
        x = PADDING + i * (DIGIT_WIDTH + TUBE_GAP)
        svg += f"""
  <rect x="{x + 4}" y="{PADDING + 2}" width="{DIGIT_WIDTH - 8}" height="{DIGIT_HEIGHT * 0.35}" rx="4" fill="white" opacity="0.04"/>"""

    svg += """
</svg>"""
    return svg


def main():
    count = get_count()
    count += 1
    save_count(count)

    os.makedirs("assets", exist_ok=True)
    svg = generate_svg(count)
    with open(OUTPUT_SVG, "w") as f:
        f.write(svg)

    print(f"Counter updated to {count}")


if __name__ == "__main__":
    main()
