import json
import os

COUNTER_FILE = "counter.json"
OUTPUT_SVG = "assets/nixie-counter.svg"

DIGIT_WIDTH = 64
DIGIT_HEIGHT = 100
PADDING = 16
TUBE_GAP = 10
NUM_DIGITS = 8


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
    digits = str(count).zfill(NUM_DIGITS)
    num_digits = len(digits)
    total_w = num_digits * (DIGIT_WIDTH + TUBE_GAP) - TUBE_GAP + PADDING * 2
    total_h = DIGIT_HEIGHT + PADDING * 2 + 30

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="{total_h}" viewBox="0 0 {total_w} {total_h}">
  <defs>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur1"/>
      <feGaussianBlur in="SourceGraphic" stdDeviation="8" result="blur2"/>
      <feMerge>
        <feMergeNode in="blur2"/>
        <feMergeNode in="blur1"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="transparent"/>
      <stop offset="100%" stop-color="transparent"/>
    </linearGradient>
    <radialGradient id="tubeBg" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#2a1a1a"/>
      <stop offset="100%" stop-color="#1e1018"/>
    </radialGradient>"""

    # PLACEHOLDER_APPEND
    for i in range(num_digits):
        svg += f"""
    <radialGradient id="digitGlow{i}" cx="50%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#ff6b8a" stop-opacity="0.25"/>
      <stop offset="60%" stop-color="#e8622c" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#e8622c" stop-opacity="0"/>
    </radialGradient>"""

    svg += """
  </defs>"""

    svg += f"""
  <rect width="{total_w}" height="{total_h}" rx="12" fill="none"/>"""

    # Label
    svg += f"""
  <text x="{total_w / 2}" y="{PADDING + DIGIT_HEIGHT + 24}" text-anchor="middle" font-family="'Segoe UI', sans-serif" font-size="13" fill="#d4756a" letter-spacing="4">V I S I T O R S</text>"""

    # Tubes
    for i, d in enumerate(digits):
        x = PADDING + i * (DIGIT_WIDTH + TUBE_GAP)
        cx = x + DIGIT_WIDTH / 2
        cy = PADDING + DIGIT_HEIGHT / 2

        svg += f"""
  <rect x="{x}" y="{PADDING}" width="{DIGIT_WIDTH}" height="{DIGIT_HEIGHT}" rx="8" fill="url(#tubeBg)" stroke="#5a3030" stroke-width="1"/>
  <rect x="{x}" y="{PADDING}" width="{DIGIT_WIDTH}" height="{DIGIT_HEIGHT}" rx="8" fill="url(#digitGlow{i})"/>
  <text x="{cx}" y="{cy + 4}" text-anchor="middle" dominant-baseline="middle" font-family="'Courier New', monospace" font-size="54" font-weight="bold" fill="#e8622c" filter="url(#glow)" opacity="0.95">{d}</text>
  <text x="{cx}" y="{cy + 4}" text-anchor="middle" dominant-baseline="middle" font-family="'Courier New', monospace" font-size="54" font-weight="bold" fill="#ff6b8a" opacity="0.25">{d}</text>"""

    # Glass reflection
    for i in range(num_digits):
        x = PADDING + i * (DIGIT_WIDTH + TUBE_GAP)
        svg += f"""
  <rect x="{x + 5}" y="{PADDING + 3}" width="{DIGIT_WIDTH - 10}" height="{DIGIT_HEIGHT * 0.3}" rx="4" fill="white" opacity="0.03"/>"""

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
