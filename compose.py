#!/usr/bin/env python3
"""
App Store Screenshot Composer
Composites headline text, device frame template, and app screenshot
into a pixel-perfect 1290×2796 App Store Connect image.

The device frame is positioned dynamically based on text height,
matching the proportions seen in professional App Store screenshots.
"""

import argparse
import os
from PIL import Image, ImageDraw, ImageFont, ImageChops

# ── Canvas ──────────────────────────────────────────────────────────
CANVAS_W = 1290
CANVAS_H = 2900

# ── Device template constants ───────────────────────────────────────
BEZEL = 12
SCREEN_W = 1100
SCREEN_CORNER_R = 105

# ── Layout ──────────────────────────────────────────────────────────
DEVICE_Y = 360                       # device top position (minimum)
MIN_TEXT_DEVICE_GAP = 15             # minimum gap between text bottom and device top
BOTTOM_MARGIN = 60                   # margin at the bottom of the canvas for contained look

# ── Typography ──────────────────────────────────────────────────────
VERB_SIZE_MAX = 180
VERB_SIZE_MIN = 140
DESC_SIZE = 95
SUBTITLE_SIZE = 80
VERB_DESC_GAP = 12
DESC_SUBTITLE_GAP = 24
DESC_LINE_GAP = 20
MAX_TEXT_W = int(CANVAS_W * 0.85)
MAX_VERB_W = int(CANVAS_W * 0.75)

FONT_PATH = os.path.join(os.path.dirname(__file__), "assets", "PlusJakartaSans-Bold.ttf")
FONT_MEDIUM_PATH = os.path.join(os.path.dirname(__file__), "assets", "PlusJakartaSans-Medium.ttf")
FRAME_PATH = os.path.join(os.path.dirname(__file__), "assets", "device_frame.png")


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def word_wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = f"{cur} {w}".strip()
        if draw.textlength(test, font=font) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def resolve_font(size, font_path=None):
    """Dynamically search for standard fonts or use custom font path."""
    candidates = []
    
    if font_path and os.path.exists(font_path):
        candidates.append(font_path)
    elif os.path.exists(FONT_PATH):
        candidates.append(FONT_PATH)
        
    import platform
    system = platform.system()
    if system == "Windows":
        win_dir = os.environ.get("SystemRoot", "C:\\Windows")
        fonts_dir = os.path.join(win_dir, "Fonts")
        candidates.extend([
            os.path.join(fonts_dir, "SF-Pro-Display-Black.otf"),
            os.path.join(fonts_dir, "ariblk.ttf"),      # Arial Black (heavy/modern sans-serif)
            os.path.join(fonts_dir, "seguibl.ttf"),     # Segoe UI Black
            os.path.join(fonts_dir, "arialbd.ttf"),     # Arial Bold
            os.path.join(fonts_dir, "impact.ttf")       # Impact
        ])
    elif system == "Darwin": # macOS
        candidates.extend([
            "/Library/Fonts/SF-Pro-Display-Black.otf",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/SFNS.ttf"
        ])
    else: # Linux
        candidates.extend([
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
        ])
        
    candidates.append("SF-Pro-Display-Black.otf")
    
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
                
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def fit_font(text, max_w, size_max, size_min, font_path=None):
    """Return the largest font size where text fits within max_w."""
    dummy = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    for size in range(size_max, size_min - 1, -4):
        font = resolve_font(size, font_path)
        bbox = dummy.textbbox((0, 0), text, font=font)
        if (bbox[2] - bbox[0]) <= max_w:
            return font
    return resolve_font(size_min, font_path)


def draw_centered(draw, y, text, font, fill="white", max_w=None, line_gap=DESC_LINE_GAP):
    lines = word_wrap(draw, text, font, max_w) if max_w else [text]
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        h = bbox[3] - bbox[1]
        # Use anchor="mt" (middle-top) for pixel-perfect horizontal centering
        # Adjust y by bbox[1] offset so text top aligns with intended position
        draw.text((CANVAS_W // 2, y - bbox[1]), line, fill=fill, font=font, anchor="mt")
        y += h + line_gap
    return y


def draw_device_frame(canvas, screen_x, screen_y, screen_w, screen_h, corner_r, bezel_thickness, is_dark_screen=False):
    draw = ImageDraw.Draw(canvas)
    
    # Draw a thin inner black shadow/bezel edge
    draw.rounded_rectangle(
        [screen_x - 2, screen_y - 2, screen_x + screen_w + 2, screen_y + screen_h + 2],
        radius=corner_r + 2,
        outline=(0, 0, 0, 255),
        width=2
    )

    # 2. Draw the Status Bar inside the screen area
    status_color = (255, 255, 255, 255) if is_dark_screen else (0, 0, 0, 255)
    
    # Load font for status bar (try Arial/system default)
    try:
        status_font = ImageFont.truetype("arial.ttf", 44)
    except:
        status_font = ImageFont.load_default()
        
    # Draw Time
    draw.text((screen_x + 75, screen_y + 40), "9:41", fill=status_color, font=status_font, anchor="lm")
    
    # Draw Battery Icon on the right
    bat_x = screen_x + screen_w - 75
    bat_y = screen_y + 40
    # Outer battery shell
    draw.rounded_rectangle([bat_x - 65, bat_y - 18, bat_x, bat_y + 18], radius=6, outline=status_color, width=3)
    # Battery cap
    draw.rectangle([bat_x, bat_y - 7, bat_x + 5, bat_y + 7], fill=status_color)
    # Battery level (100% full)
    draw.rounded_rectangle([bat_x - 60, bat_y - 12, bat_x - 5, bat_y + 12], radius=3, fill=status_color)
    
    # Draw Wifi Icon (3 arcs/lines)
    wifi_x = bat_x - 100
    wifi_y = bat_y
    # Draw Wifi dot
    draw.ellipse([wifi_x - 4, wifi_y + 10, wifi_x + 4, wifi_y + 18], fill=status_color)
    # Draw 2 arcs
    draw.arc([wifi_x - 12, wifi_y - 2, wifi_x + 12, wifi_y + 22], start=210, end=330, fill=status_color, width=3)
    draw.arc([wifi_x - 22, wifi_y - 12, wifi_x + 22, wifi_y + 32], start=210, end=330, fill=status_color, width=3)
    
    # Draw Cellular Signal (4 bars)
    sig_x = wifi_x - 50
    sig_y = wifi_y + 15
    for i in range(4):
        h = (i + 1) * 8
        w = 6
        spacing = 4
        x0 = sig_x - (4 - i) * (w + spacing)
        y0 = sig_y - h
        draw.rounded_rectangle([x0, y0, x0 + w, sig_y], radius=1, fill=status_color)

    # 3. Draw Home Indicator at the bottom of the screen
    home_y = screen_y + screen_h - 40
    draw.rounded_rectangle(
        [canvas.width // 2 - 160, home_y - 4, canvas.width // 2 + 160, home_y + 4],
        radius=4,
        fill=status_color
    )


def draw_radial_glow(canvas, center_x, center_y, radius, start_color):
    """Draw a soft radial glow onto the canvas using alpha blending."""
    size = radius * 2
    glow_mask = Image.new("L", (size, size), 0)
    draw_mask = ImageDraw.Draw(glow_mask)
    
    # Concentric circles with soft quadratic falloff
    for r in range(radius, 0, -2):
        opacity = int(255 * (1 - r / radius) ** 2 * 0.38) # Soft max opacity at center
        draw_mask.ellipse([radius - r, radius - r, radius + r, radius + r], fill=opacity)
        
    glow_color = Image.new("RGBA", (size, size), start_color)
    glow_color.putalpha(glow_mask)
    
    # Paste centered
    x0 = center_x - radius
    y0 = center_y - radius
    canvas.alpha_composite(glow_color, (x0, y0))


def apply_noise(canvas, opacity=0.015):
    """Generate a small noise patch and stretch it to create a soft film grain texture."""
    import random
    patch_size = 300
    noise_patch = Image.new("L", (patch_size, patch_size))
    pixels = noise_patch.load()
    for y in range(patch_size):
        for x in range(patch_size):
            pixels[x, y] = random.randint(110, 145)
            
    noise_grain = noise_patch.resize(canvas.size, Image.BILINEAR)
    noise_rgba = Image.merge("RGBA", [
        noise_grain,
        noise_grain,
        noise_grain,
        Image.new("L", canvas.size, int(255 * opacity))
    ])
    return Image.alpha_composite(canvas, noise_rgba)


def compose(bg_start_hex, bg_end_hex, verb, desc, subtitle, screenshot_path, output_path, verb_size=None, subtitle_size=None, glow_color=None):
    c_start = hex_to_rgb(bg_start_hex)
    c_end = hex_to_rgb(bg_end_hex)

    # ── 1. Create Linear Gradient Background ──────────────────────────
    canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H))
    draw_grad = ImageDraw.Draw(canvas)
    for y_pos in range(CANVAS_H):
        t = y_pos / (CANVAS_H - 1)
        r = int(c_start[0] * (1 - t) + c_end[0] * t)
        g = int(c_start[1] * (1 - t) + c_end[1] * t)
        b = int(c_start[2] * (1 - t) + c_end[2] * t)
        draw_grad.line([(0, y_pos), (CANVAS_W, y_pos)], fill=(r, g, b, 255))

    draw = ImageDraw.Draw(canvas)

    # ── 2. Measure text, then calculate device position dynamically ─
    v_max = verb_size if verb_size else VERB_SIZE_MAX
    verb_font = fit_font(verb.upper(), MAX_VERB_W, v_max, VERB_SIZE_MIN, FONT_PATH)
    
    desc_is_bold = desc.isupper() and len(desc.strip()) > 0
    desc_font = resolve_font(DESC_SIZE, FONT_PATH if desc_is_bold else FONT_MEDIUM_PATH)
    
    s_max = subtitle_size if subtitle_size else SUBTITLE_SIZE
    sub_font = resolve_font(s_max, FONT_MEDIUM_PATH)

    # Measure total text block height dynamically starting at y=120
    dummy = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    text_top = 120
    m_y = text_top
    m_y = draw_centered(dummy, m_y, verb.upper(), verb_font, fill="white", max_w=MAX_VERB_W)
    if desc.strip():
        m_y += VERB_DESC_GAP
        m_y = draw_centered(dummy, m_y, desc, desc_font, fill="white", max_w=MAX_TEXT_W)
    m_y += DESC_SUBTITLE_GAP
    text_bottom = draw_centered(dummy, m_y, subtitle, sub_font, fill="white", max_w=MAX_TEXT_W)

    # Position device dynamically to avoid overlapping the text
    device_y = max(DEVICE_Y, text_bottom + MIN_TEXT_DEVICE_GAP)

    # Draw text at centered position on main canvas
    y = text_top
    y = draw_centered(draw, y, verb.upper(), verb_font, fill="white", max_w=MAX_VERB_W)
    if desc.strip():
        y += VERB_DESC_GAP
        y = draw_centered(draw, y, desc, desc_font, fill="white", max_w=MAX_TEXT_W)
    y += DESC_SUBTITLE_GAP
    draw_centered(draw, y, subtitle, sub_font, fill=(255, 255, 255, 230), max_w=MAX_TEXT_W)
    
    device_x = (CANVAS_W - (SCREEN_W + 2 * BEZEL)) // 2
    screen_x = device_x + BEZEL
    screen_y = device_y + BEZEL
    
    # Calculate screen height to fit complete frame on the canvas with BOTTOM_MARGIN
    screen_h = CANVAS_H - BOTTOM_MARGIN - screen_y - BEZEL


    # ── 4. Screenshot into screen area ──────────────────────────────
    shot = Image.open(screenshot_path).convert("RGBA")

    # Measure brightness to determine dark or light screen
    gray_shot = shot.convert("L")
    pixels = list(gray_shot.getdata())
    avg_brightness = sum(pixels) / len(pixels)
    is_dark_screen = avg_brightness <= 127

    # Scale to fill screen width
    scale = SCREEN_W / shot.width
    sc_w = SCREEN_W
    sc_h = int(shot.height * scale)
    shot = shot.resize((sc_w, sc_h), Image.LANCZOS)

    # Crop or pad shot to fit screen_h dynamically
    if sc_h > screen_h:
        shot = shot.crop((0, 0, SCREEN_W, screen_h))
    else:
        new_shot = Image.new("RGBA", (SCREEN_W, screen_h), (255, 255, 255, 255))
        new_shot.paste(shot, (0, 0))
        shot = new_shot

    # Screen mask (rounded rect)
    scr_mask = Image.new("L", canvas.size, 0)
    ImageDraw.Draw(scr_mask).rounded_rectangle(
        [screen_x, screen_y, screen_x + SCREEN_W, screen_y + screen_h],
        radius=SCREEN_CORNER_R,
        fill=255,
    )

    # ── 5. Draw the outer bezel of the device on canvas ─────────────
    outer_x0 = screen_x - BEZEL
    outer_y0 = screen_y - BEZEL
    outer_x1 = screen_x + SCREEN_W + BEZEL
    outer_y1 = screen_y + screen_h + BEZEL
    outer_r = SCREEN_CORNER_R + BEZEL
    
    # Draw a soft radial glow centered behind the device before rendering bezel
    glow_rgb = hex_to_rgb(glow_color) if glow_color else (255, 255, 255)
    draw_radial_glow(canvas, CANVAS_W // 2, device_y + screen_h // 2, 720, (*glow_rgb, 255))
    
    # Draw the main silver bezel body
    draw.rounded_rectangle(
        [outer_x0, outer_y0, outer_x1, outer_y1],
        radius=outer_r,
        fill=(235, 238, 243, 255) # Sleek platinum silver
    )
    
    # Draw a thin dark inner separation outline right at the screen edge
    # This separates the screen glass from the silver bezel body
    draw.rounded_rectangle(
        [screen_x - 1, screen_y - 1, screen_x + SCREEN_W + 1, screen_y + screen_h + 1],
        radius=SCREEN_CORNER_R + 1,
        outline=(50, 52, 55, 255),
        width=2
    )

    # Draw the highlight outer border of the silver bezel
    draw.rounded_rectangle(
        [outer_x0, outer_y0, outer_x1, outer_y1],
        radius=outer_r,
        outline=(255, 255, 255, 255), # Premium white shine
        width=2
    )

    # ── 6. Paste screenshot inside screen area ──────────────────────
    scr_layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    scr_layer.paste(shot, (screen_x, screen_y))
    scr_layer.putalpha(scr_mask)

    canvas = Image.alpha_composite(canvas, scr_layer)

    # ── 7. Draw Programmatic Status Bar, Home Indicator, and Inner Shadow ─
    draw_device_frame(canvas, screen_x, screen_y, SCREEN_W, screen_h, SCREEN_CORNER_R, BEZEL, is_dark_screen=is_dark_screen)

    # Apply soft monochrome noise grain overlay to the entire canvas
    canvas = apply_noise(canvas, opacity=0.015)

    # ── 8. Save ────────────────────────────────────────────────────
    canvas.convert("RGB").save(output_path, "PNG")
    print(f"OK: {output_path} ({CANVAS_W}x{CANVAS_H})")


def main():
    p = argparse.ArgumentParser(description="Compose App Store screenshot")
    p.add_argument("--bg", help="Background hex colour (used for both start and end if gradient is not specified)")
    p.add_argument("--bg_start", help="Gradient start hex colour (#06C974)")
    p.add_argument("--bg_end", help="Gradient end hex colour (#04874E)")
    p.add_argument("--verb", required=True, help="Action verb (TRACK)")
    p.add_argument("--desc", required=True, help="Benefit descriptor (TRADING CARD PRICES)")
    p.add_argument("--subtitle", required=True, help="Benefit subtitle (Up to 90% Smaller)")
    p.add_argument("--screenshot", required=True, help="Simulator screenshot path")
    p.add_argument("--output", required=True, help="Output file path")
    p.add_argument("--verb_size", type=int, help="Override maximum verb font size")
    p.add_argument("--subtitle_size", type=int, help="Override maximum subtitle font size")
    p.add_argument("--glow_color", help="Glow hex colour behind phone (#FFFFFF)")
    args = p.parse_args()

    bg_start = args.bg_start or args.bg or "#06C974"
    bg_end = args.bg_end or args.bg or bg_start

    compose(
        bg_start, bg_end, 
        args.verb, args.desc, args.subtitle, 
        args.screenshot, args.output, 
        verb_size=args.verb_size, 
        subtitle_size=args.subtitle_size, 
        glow_color=args.glow_color
    )


if __name__ == "__main__":
    main()
